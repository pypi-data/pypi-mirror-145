# This file is part of Build Your Own CI
#
# Copyright 2018 Vincent Ladeuil
# Copyright 2016, 2017 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 3, as published by the
# Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranties of MERCHANTABILITY,
# SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

from launchpadlib import (
    credentials,
    launchpad,
)


class DontAuthorizeRequestToken(credentials.RequestTokenAuthorizationEngine):
    """No user can interact to authorize a new token."""

    def make_end_user_authorize_token(self, credentials, request_token):
        # FIXME: We need a specific exception to ensure it propagates freely
        # without being caught -- vila 2016-11-24
        raise NotImplementedError('Launchpad token is invalid')


class NoBrowserLaunchpad(launchpad.Launchpad):
    """Override to avoid hanging when the OAuth token is invalid."""

    @classmethod
    def authorization_engine_factory(cls, *args):
        return DontAuthorizeRequestToken(*args)


class Launchpad(object):

    def __init__(self, conf):
        self.service_root = conf.get('launchpad.service_root')
        # version='devel' won't remove used entry points so it's safe to use it
        # here especially if tests are run on a regular basis
        self.lp = NoBrowserLaunchpad.login_with(
            # FIXME: lp doesn't seem to care about matching login name and
            # credentials. A test would help ensure that's true
            # -- vila 2018-01-18
            'brz-byoci', self.service_root,
            credentials_file=conf.get('launchpad.credentials'),
            version='devel')

    def get_project(self, name):
        return self.lp.projects[name]

    def get_bzr_branch(self, url):
        if url.startswith('lp:'):
            if self.service_root == 'qastaging':
                # Prefix with qastaging or we get the production one
                url = 'lp://qastaging/{}'.format(url[len('lp:'):])
        return self.lp.branches.getByUrl(url=url)

    def get_git_repo(self, url):
        if not url.startswith('lp:'):
            raise ValueError('{} does not start with lp:'.format(url))
        # FIXME: cjwatson said getByUrl could be exposed, file a bug if needed
        # -- vila 2016-11-25
        return self.lp.git_repositories.getByPath(path=url[len('lp:'):])


class Votes(dict):
    """Count votes by category."""

    def __missing__(self, key):
        """Autovivify as-yet-unknown keys.

        This allows writing: v = Votes() ; v['Approved'] += 1.
        """
        # If the key is missing, pretend it exists and that its value is 0.
        return 0


def is_approved(proposal, target):
    """Check whether a proposal is approved by the summary of the votes."""
    votes = Votes()
    for vote in proposal.votes:
        if not target.isPersonTrustedReviewer(reviewer=vote.reviewer):
            # Ignore untrusted votes
            continue
        if vote.is_pending:
            votes['Pending'] += 1
        else:
            comment = vote.comment
            if comment is not None and comment.vote != u'Abstain':
                votes[comment.vote] += 1
    approved = False
    if ((votes['Approve'] >= 1 and
         votes['Pending'] == 0 and
         votes['Needs Fixing'] == 0 and
         votes['Disapprove'] == 0 and
         votes['Resubmit'] == 0 and
         votes['Needs Information'] == 0)):
        approved = True
    return approved
