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


import logging
import re
import sys
import time

import jenkins

from byoci import commands
from byoci.monitor import config


logger = logging.getLogger(__name__)


setup_logging = commands.setup_logging


class ArgParser(commands.ArgParser):
    """An argument parser for the byo-ci-monitor script."""

    script_name = 'byo-ci-monitor'


# All commands are registered here, defining what run() supports
command_registry = commands.CommandRegistry()


class Help(commands.Help):

    description = 'Describe byo-ci-monitor commands.'
    command_registry = command_registry
    arg_parser_class = ArgParser


command_registry.register(Help)


class Command(commands.Command):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser.add_argument(
            '--option', '-O', metavar='OPTION=VALUE',
            action='append', dest='overrides', default=[],
            help='Override OPTION with provided VALUE. Can be repeated.')
        self.conf = config.MonitorStack()

    def parse_args(self, args):
        super().parse_args(args)
        self.conf.cmdline_store.from_cmdline(self.options.overrides)
        # Now we may configure logging. It can't be configured until we reach
        # this point, this means errors occuring before this point can be
        # logged without the user specified options.
        log_level = self.conf.get('logging.level')
        log_format = self.conf.get('logging.format')
        commands.setup_logging(log_level, log_format)
        return self.options


# MISSINGTESTS: Around failures and with a fresh master -- vila 2018-02-11
class Jenkins(jenkins.Jenkins):

    def get_info(self, item="", query=None):
        info = super().get_info(item, query)
        logger.debug('Info: {}'.format(info))
        return info

    def quiet_down(self):
        request = jenkins.Request(self._build_url('quietDown'), data={})
        self.jenkins_open(request)
        info = self.get_info()
        if not info['quietingDown']:
            raise jenkins.JenkinsException('quiet down failed')

    def restart(self):
        logger.info('Restart jenkins')
        request = jenkins.Request(self._build_url('restart'), data={})
        try:
            self.jenkins_open(request)
        except jenkins.HTTPError:
            # Weirdly enough, asking to restart may break the connection before
            # the server replies...
            pass
        attempts = 0
        # FIXME: Number of attempts and sleep time should be configured via
        # timeouts -- vila 2018-01-22
        while attempts < 10:
            attempts += 1
            try:
                logger.info('Waiting for normal op (attempt {})'
                            .format(attempts))
                restarted = self.wait_for_normal_op(60)
                if restarted:
                    break
            except Exception:
                # The server may be restarting while we try to assess its state
                # so be ready
                time.sleep(2)
                pass

    def check_plugin_updates(self):
        req = jenkins.Request(
            self._build_url('pluginManager/checkUpdatesServer'), data={})
        req.add_header('Authorization', self.auth)
        self.maybe_add_crumb(req)
        resp = jenkins.urlopen(req, timeout=self.timeout)
        if not resp.status == 200:
            raise jenkins.JenkinsException(
                'Cannot check plugin updates server')
        # Find plugin updates if any
        updates = []
        try:
            url = self._build_url(
                'updateCenter/coreSource/api/json?pretty=true&depth=2')
            update_center = jenkins.json.loads(
                self.jenkins_open(jenkins.Request(url)))
            updates = [upd['name'] for upd in update_center['updates']]
        except (jenkins.HTTPError, jenkins.BadStatusLine):
            raise jenkins.BadHTTPException(
                "Error communicating with server[%s]" % self.server)
        except ValueError:
            raise jenkins.JenkinsException(
                "Could not parse JSON info for server[%s]" % self.server)
        return updates


class UpdatePlugins(Command):

    name = 'update-plugins'
    description = 'Update master plugins.'
    arg_parser_class = ArgParser

    def run(self):
        # FIXME: Administer right is needed to run groovy scripts (which
        # install_plugin() rely upon). Consider running update-plugins as as an
        # admin rather than using monitor.user -- vila 2018-03-02
        self.jk = Jenkins(self.conf.get('byoci.api'),
                          self.conf.get('byoci.user'),
                          self.conf.get('byoci.token'))
        restart = False
        plugins = self.conf.get('jenkins.plugins')
        logger.info('Updating plugin definitions {}'.format(plugins))
        updates = self.jk.check_plugin_updates()
        if updates:
            logger.info('Installing plugin updates {}'.format(updates))
            for plugin in updates:
                restart = self.jk.install_plugin(plugin) or restart
        if plugins:
            plugins = plugins.split()
            logger.info('Installing plugins {}'.format(plugins))
            for plugin in plugins:
                restart = self.jk.install_plugin(plugin) or restart
            logger.info('Plugins {} installed'.format(plugins))
        if restart:
            self.jk.quiet_down()
            self.jk.restart()
            logger.info('jenkins restarted')
        return 0


command_registry.register(UpdatePlugins)

# FIXME: This should be a config option (probably with the pattern being in a
# file by itself -- vila 2018-05-22
# FIXME: The label should a slave config option -- vila 2018-05-22
slave_pattern = '''\
<?xml version="1.0" encoding="UTF-8"?>
<slave>
  <name>{slave}</name>
  <description></description>
  <remoteFS>{slave.remote.fs}</remoteFS>
  <numExecutors>1</numExecutors>
  <mode>NORMAL</mode>
  <retentionStrategy class="hudson.slaves.RetentionStrategy$Demand">
    <inDemandDelay>{slave.demand.delay}</inDemandDelay>
    <idleDelay>{slave.idle.delay}</idleDelay>
  </retentionStrategy>
  <launcher class="hudson.slaves.CommandLauncher" plugin="command-launcher">
    <agentCommand>{slave.start}</agentCommand>
  </launcher>
  <label>production</label>
  <nodeProperties/>
</slave>
'''


class UpdateSlave(Command):

    name = 'update-slave'
    description = 'Update slave.'
    arg_parser_class = ArgParser

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser.add_argument(
            'slave', metavar='SLAVE',
            help='The slave description to update on master.')

    def run(self):
        self.jk = Jenkins(self.conf.get('byoci.api'),
                          self.conf.get('byoci.user'),
                          self.conf.get('byoci.token'))
        slave_name = self.options.slave
        self.conf.set('slave', slave_name)
        if not self.jk.node_exists(slave_name):
            logger.info('creating slave {}'.format(slave_name))
            command = self.conf.get('slave.start')
            self.jk.create_node(
                slave_name, remoteFS=self.conf.get('slave.remote.fs'),
                launcher='hudson.slaves.CommandLauncher',
                launcher_params=dict(command=command))
        logger.info('updating slave {}'.format(slave_name))
        ret = self.jk.reconfig_node(
            slave_name, self.conf.expand_options(slave_pattern))
        logger.info('slave {} created and configured'.format(slave_name))
        return ret


command_registry.register(UpdateSlave)


def get_job_default_values(name, info):
    params = None
    for action in info['actions']:
        if 'parameterDefinitions' in action:
            params = dict()
            for param_def in action['parameterDefinitions']:
                name = param_def['name']
                val = param_def['defaultParameterValue']['value']
                params[name] = val
    return params


class RunJob(Command):

    name = 'run-job'
    description = 'Run job[s].'
    arg_parser_class = ArgParser

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser.add_argument(
            'jobre', metavar='JOB_NAME_REGEXP',
            help='A regular expression for job names.')
        self.parser.add_argument(
            '--dry-run', '-n',
            action='store_true',
            help='List rather than run the matching jobs.')

    def run(self):
        self.jk = Jenkins(self.conf.get('byoci.api'),
                          self.conf.get('byoci.user'),
                          self.conf.get('byoci.token'))
        jobs = [j for j in self.jk.get_all_jobs()
                if re.search(self.options.jobre, j['fullname'])]
        if not jobs:
            if not self.options.dry_run:
                logger.error('No job matches {}'.format(self.options.jobre))
            return 1
        for job in jobs:
            name = job['fullname']
            if self.options.dry_run:
                self.out.write(name + '\n')
            else:
                logger.info('Running {}'.format(name))
                info = self.jk.get_job_info(name)
                # Get the param values as the jenkins module doesn't support
                # just calling the job without any parameter :-/
                params = get_job_default_values(name, info)
                self.jk.build_job(name, params)
        return 0


command_registry.register(RunJob)


def run(args=None, out=None, err=None):
    if args is None:
        args = sys.argv[1:]
    if not args:
        cmd = Help()
        cmd_name = 'help'
    else:
        cmd_name = args[0]
        args = args[1:]
        try:
            cmd_class = command_registry.get(cmd_name)
            cmd = cmd_class(out=out, err=err)
        except KeyError:
            cmd = Help(out=out, err=err)
            args = [cmd_name]
    try:
        cmd.parse_args(args)
        return cmd.run()
    except Exception as e:
        logger.debug('{} failed'.format(cmd_name), exc_info=True)
        logger.error('{} failed: {!r}'.format(cmd_name, e))
        return -1
