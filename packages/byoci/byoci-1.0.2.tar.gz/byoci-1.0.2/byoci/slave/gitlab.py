# This file is part of Build Your Own CI
#
# Copyright 2018 Vincent Ladeuil
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

import json
import logging
import requests
import sys
import time


from urllib import parse as urlparse


import byoci


from byov import (
    errors,  # FIXME: We shouldn't need to rely on byov here -- vila 2018-07-24
    timeouts,
)


logger = logging.getLogger(__name__)


class GitlabException(errors.ByovError):
    pass


class GitlabAPIException(KeyError):
    pass


class Gitlab404(GitlabAPIException):
    pass


class Client(object):
    """A client for the gitlab  API.

    This is a simple wrapper around requests.Session so we inherit all good
    bits while providing a simple point for tests to override when needed.
    """

    user_agent = 'byoci-{} python {}'.format(byoci.version(),
                                             sys.version.split()[0])

    session_class = requests.Session

    def __init__(self, base_url, token, timeouts):
        self.url = urlparse.urljoin(base_url, 'api/v4/')
        self.token = token
        self.timeouts = timeouts
        self.session = self.session_class()

    def request(self, method, url, params=None, headers=None, **kwargs):
        """Overriding base class to handle the root url."""
        # Note that url may be absolute in which case 'root_url' is ignored by
        # urljoin.
        sent_headers = {'User-Agent': self.user_agent,
                        'Private-Token': self.token,
                        'Content-Type': 'application/json'}
        if headers is not None:
            sent_headers.update(headers)
        final_url = urlparse.urljoin(self.url, url)
        response = self.session.request(
            method, final_url, headers=sent_headers, params=params, **kwargs)
        return response

    def get(self, url, **kwargs):
        return self.request('GET', url, **kwargs)

    def post(self, url, data=None, **kwargs):
        if data is not None:
            data = json.dumps(data)
        return self.request('POST', url, data=data, **kwargs)

    def put(self, url, data=None, **kwargs):
        if data is not None:
            data = json.dumps(data)
        return self.request('PUT', url, data=data, **kwargs)

    def patch(self, url, **kwargs):
        return self.request('PATCH', url, **kwargs)

    def delete(self, url, **kwargs):
        return self.request('DELETE', url, **kwargs)

    def close(self):
        self.session.close()

    def retry(self, func, url, *args, **kwargs):
        req_path = '{} {}'.format(func.__name__.upper(), url)
        no_404_retry = kwargs.pop('no_404_retry', False)
        first, up_to, retries = self.timeouts
        first = float(first)
        up_to = float(up_to)
        retries = int(retries)
        sleeps = timeouts.ExponentialBackoff(first, up_to, retries)
        for attempt, sleep in enumerate(sleeps, start=1):
            try:
                response = None
                if attempt > 1:
                    logger.debug('Re-trying {} {}/{}'.format(
                        req_path, attempt, retries))
                response = func(url, *args, **kwargs)
            except requests.ConnectionError:
                # Most common transient failure: the API server is unreachable
                # (server, network or client may be the cause).
                msg = 'Connection error for {}, will sleep for {} seconds'
                logger.warning(msg.format(req_path, sleep))
            except Exception:
                # All other exceptions are raised
                logger.error('{} failed'.format(req_path), exc_info=True)
                raise GitlabException('{} failed'.format(req_path))
            # If the request succeeded return the response (also for the 404
            # special case as instructed).
            if (response is not None and
                (response.ok or (response.status_code == 404 and
                                 no_404_retry))):
                return response
            if response is not None and not response.ok:
                if response.status_code == 429:
                    msg = ('Rate limit reached for {},'
                           ' will sleep for {} seconds')
                    # This happens rarely but breaks badly if not caught. elmo
                    # recommended a 30 seconds nap in that case.
                    sleep += 30
                    logger.warning(msg.format(req_path, sleep))
                elif response.status_code == 502:
                    # nginx can't reach gitlab, retry
                    pass
                elif response.status_code == 500:
                    # gitlab is overloaded /o\, retry
                    pass
                else:
                    try:
                        response_content = response.json()
                    except requests.compat.json.JSONDecodeError:
                        # Forget about it, gitlab didn't properly format its
                        # response :-/
                        response_content = '{}, {}'.format(
                            response.reason, response.content)
                    # All other errors are raised
                    msg = '{} failed {}: {}'.format(req_path,
                                                    response.status_code,
                                                    response_content)
                    # Nice spot to debug the API usage
                    logger.error(msg, exc_info=True)
                    raise GitlabException('{exc}', exc=msg)
            # Take a nap before retrying
            logger.debug('Sleeping {} seconds for {} {}/{}'.format(
                sleep, req_path, attempt, retries))
            time.sleep(sleep)
        # Raise if we didn't succeed at all
        raise GitlabException(
            "Failed to '{}' after {} retries".format(req_path, attempt))


class GitlabClient(object):
    """Client for the gitlab API."""

    http_class = Client

    def __init__(self, base_url, token, timeouts):
        self.http = self.http_class(base_url, token, timeouts)

    def get_project(self, project):
        encoded_project = urlparse.quote(project, safe='')
        response = self.http.retry(
            self.http.get, 'projects/{}'.format(encoded_project),
            no_404_retry=True)
        if response.status_code == 404:
            raise Gitlab404(project)
        return response.json()

    def get_branch(self, project, branch):
        encoded_project = urlparse.quote(project, safe='')
        response = self.http.retry(
            self.http.get, 'projects/{}/repository/branches/{}'.format(
                encoded_project, branch),
            no_404_retry=True)
        if response.status_code == 404:
            raise Gitlab404((project, branch))
        return response.json()

    def delete_branch(self, project, branch):
        encoded_project = urlparse.quote(project, safe='')
        response = self.http.retry(
            self.http.delete, 'projects/{}/repository/branches/{}'.format(
                encoded_project, branch),
            no_404_retry=True)
        if response.status_code == 404:
            # It's deleted, caller is happy (worst case scenario is branches
            # leaking on gitlab which is easy to spot and fix)
            pass
        return response

    def get_proposals(self, project, branch, state='opened'):
        encoded_project = urlparse.quote(project, safe='')
        response = self.http.retry(
            self.http.get,
            'projects/{}/merge_requests?target_branch={}&state={}'.format(
                encoded_project, branch, state),
            no_404_retry=True)
        if response.status_code == 404:
            raise Gitlab404((project, branch))
        return response.json()

    def get_proposal(self, project, proposal_iid):
        encoded_project = urlparse.quote(project, safe='')
        url = 'projects/{}/merge_requests/{}'.format(
            encoded_project, proposal_iid)
        response = self.http.retry(self.http.get, url, no_404_retry=True)
        if response.status_code == 404:
            raise Gitlab404([project, proposal_iid])
        return response.json()

    def create_proposal(self, project, source, target, title, description):
        encoded_project = urlparse.quote(project, safe='')
        encoded_title = urlparse.quote(title, safe='')
        encoded_description = urlparse.quote(description, safe='')
        url = ('projects/{}/merge_requests?'
               'source_branch={}&target_branch={}&title={}&description={}')
        response = self.http.retry(
            self.http.post,
            url.format(encoded_project, source, target, encoded_title,
                       encoded_description))
        return response.json()

    def update_proposal(self, project, proposal_iid, **kwargs):
        encoded_project = urlparse.quote(project, safe='')
        url = 'projects/{}/merge_requests/{}'.format(
            encoded_project, proposal_iid)
        if kwargs:
            prefix = '?'
            for k, v in kwargs.items():
                url += '{}{}={}'.format(prefix, k, urlparse.quote(v, safe=''))
                prefix = '&'
        response = self.http.retry(self.http.put, url, no_404_retry=True)
        if response.status_code == 404:
            raise Gitlab404(
                [project, proposal_iid] +
                ['{}={}'.format(k, v) for k, v in kwargs.items()])
        return response

    def get_proposal_comments(self, project, proposal_iid):
        # FIXME: paginate ? -- vila 2018-08-02
        encoded_project = urlparse.quote(project, safe='')
        sorting = '?order_by=created_at&sort=desc'
        response = self.http.retry(
            self.http.get,
            'projects/{}/merge_requests/{}/notes{}'.format(
                encoded_project, proposal_iid, sorting),
            no_404_retry=True)
        if response.status_code == 404:
            raise Gitlab404((project, proposal_iid))
        return response.json()

    def create_proposal_comment(self, project, proposal_iid, comment):
        encoded_project = urlparse.quote(project, safe='')
        encoded_comment = urlparse.quote(comment, safe='')
        response = self.http.retry(
            self.http.post,
            'projects/{}/merge_requests/{}/notes?body={}'.format(
                encoded_project, proposal_iid, encoded_comment))
        return response.json()

    def delete_proposal(self, project, proposal_iid):
        encoded_project = urlparse.quote(project, safe='')
        response = self.http.retry(
            self.http.delete, 'projects/{}/merge_requests/{}'.format(
                encoded_project, proposal_iid),
            no_404_retry=True)
        if response.status_code == 404:
            raise Gitlab404((project, proposal_iid))
        return response

    # NEEDTESTS: Used to setup the gitlab test server -- vila 2018-07-27
    def create_user(self, name, password):
        response = self.http.retry(
            self.http.post,
            'users?name={}&username={}&password={}&email={}'
            # Avoid email confirmation pre-requisite so we can create a
            # personal access token later.
            '&skip_confirmation=true'.format(
                name, name, password, '{}@example.com'.format(name)))
        return response.json()

    # NEEDTESTS: Used to setup the gitlab test server -- vila 2018-07-27
    def create_group(self, name, path, visibility):
        response = self.http.retry(
            self.http.post,
            'groups?name={}&path={}&visibility={}'.format(
                name, path, visibility))
        return response.json()

    # NEEDTESTS: Used to setup the gitlab test server -- vila 2018-07-27
    def create_project(self, name, path, namespace_id, visibility):
        encoded_name = urlparse.quote(name, safe='')
        encoded_path = urlparse.quote(path, safe='')
        response = self.http.retry(
            self.http.post,
            'projects?name={}&path={}&namespace_id={}&visibility={}'.format(
                encoded_name, encoded_path, namespace_id, visibility))
        return response.json()

    # NEEDTESTS: Used to setup the gitlab test server -- vila 2018-07-27
    def add_ssh_key_for(self, user_id, title, key):
        encoded_title = urlparse.quote(title, safe='')
        encoded_key = urlparse.quote(key, safe='')
        response = self.http.retry(
            self.http.post,
            'users/{}/keys?title={}&key={}'.format(
                user_id, encoded_title, encoded_key))
        return response

    # NEEDTESTS: Used to setup the gitlab test server -- vila 2018-07-27
    def add_project_member(self, project_id, user_id, access_level):
        response = self.http.retry(
            self.http.post,
            'projects/{}/members?user_id={}&access_level={}'.format(
                project_id, user_id, access_level))
        return response.json()


class Gitlab(object):

    def __init__(self, conf, token=None):
        self.conf = conf
        if token is None:
            with open(self.conf.get('gitlab.api.credentials')) as f:
                token = f.read().strip()
        self.gl = GitlabClient(
            self.conf.get('gitlab.api.url'),
            token,
            self.conf.get('gitlab.api.timeouts'))

    def get_project(self, name):
        return self.gl.get_project(name)

    def get_branch(self, project, branch):
        return self.gl.get_branch(project, branch)

    def delete_branch(self, project, branch):
        try:
            response = self.gl.delete_branch(project, branch)
        except Gitlab404:
            # It's dead Jim
            pass
        return response

    def get_proposals(self, project, branch):
        return self.gl.get_proposals(project, branch)

    def get_proposal(self, project, proposal_iid):
        return self.gl.get_proposal(project, proposal_iid)

    def create_proposal(self, project, source, target, title, description):
        return self.gl.create_proposal(project, source, target, title,
                                       description)

    def mark_proposal(self, project, proposal_iid, mark):
        existing = self.gl.get_proposal(project, proposal_iid)
        labels = existing['labels'] + [mark]
        return self.gl.update_proposal(project, proposal_iid,
                                       labels=','.join(labels))

    def get_proposal_comments(self, project, proposal_iid):
        return self.gl.get_proposal_comments(project, proposal_iid)

    def create_proposal_comment(self, project, proposal_iid, comment):
        return self.gl.create_proposal_comment(
            project, proposal_iid, comment)

    def delete_proposal(self, project, proposal_iid):
        try:
            response = self.gl.delete_proposal(project, proposal_iid)
        except Gitlab404:
            # It's dead Jim
            pass
        return response

    def create_user(self, name, password):
        return self.gl.create_user(name, password)

    def create_group(self, name, path=None, visibility='internal'):
        if path is None:
            path = name
        return self.gl.create_group(name, path, visibility)

    def create_project(self, name, namespace_id, path=None,
                       visibility='internal'):
        if path is None:
            path = name
        return self.gl.create_project(name, path, namespace_id, visibility)

    def add_ssh_key_for(self, user_id, title, key):
        # Note to self: the key added this way ends up in
        # git@gitlab:/var/opt/gitlab/.ssh/authorized_keys restricted with
        # gitlab-shell {key_id}
        return self.gl.add_ssh_key_for(user_id, title, key)

    def add_project_member(self, project_id, user_id, role):
        roles = dict(admin=50, master=40, developer=30)
        return self.gl.add_project_member(project_id, user_id, roles[role])
