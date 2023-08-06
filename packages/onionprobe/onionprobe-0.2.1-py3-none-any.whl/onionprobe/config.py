#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Handle Onionprobe configurations.
#
# Copyright (C) 2022 Silvio Rhatto <rhatto@torproject.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License,
# or any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Dependencies
import os
import argparse

try:
    import yaml
except ImportError:
    print("Please install pyaml first!")
    raise ImportError

# The Onionprobe version string
# Uses Semantic Versioning 2.0.0
# See https://semver.org
onionprobe_version = '0.2.1'

# The base path for this project
basepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir) + os.sep

# Default configuration
defaults = {
        'log_level'               : 'info',
        'launch_tor'              : True,
        'tor_address'             : '127.0.0.1',
        'socks_port'              : 19050,
        'control_port'            : 19051,
        'control_password'        : False,
        'loop'                    : False,
        'prometheus_exporter'     : False,
        'prometheus_exporter_port': 9091,
        'shuffle'                 : True,
        'randomize'               : True,
        'new_circuit'             : False,
        'interval'                : 60,
        'sleep'                   : 60,
        'descriptor_max_retries'  : 5,
        'descriptor_timeout'      : 30,
        'http_connect_timeout'    : 30,
        'http_connect_max_retries': 3,
        'http_read_timeout'       : 30,
        'circuit_stream_timeout'  : 60,
        'endpoints'               : {
            'www.torproject.org': {
                'address' : '2gzyxa5ihm7nsggfxnu52rck2vv4rvmdlkiu3zzui5du4xyclen53wid.onion',
                'protocol': 'http',
                'port'    : '80',
                'paths'   : [
                        {
                            'path'   : '/',
                            'pattern': 'Tor Project',
                        },
                    ],
                },
            }
        }

def cmdline():
    """
    Evalutate the command line.

    :return: Command line arguments.
    """

    epilog = """Examples:

      onionprobe -c configs/tor.yaml
      onionprobe -e http://2gzyxa5ihm7nsggfxnu52rck2vv4rvmdlkiu3zzui5du4xyclen53wid.onion
    """

    epilog += """\nAvailable metrics:
    """

    from .metrics import metrics

    for metric in metrics:
        item = metrics[metric].describe()[0]

        epilog += "\n  {}:\n        {}".format(item.name, item.documentation)

    description = 'Test and monitor onion services'
    parser      = argparse.ArgumentParser(
                    description=description,
                    epilog=epilog,
                    formatter_class=argparse.RawDescriptionHelpFormatter,
                  )

    parser.add_argument('-c', '--config', help='Read options from configuration file')

    parser.add_argument('-e', '--endpoints', nargs='*', help='Add endpoints to the test list', metavar="onion-address1")

    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + onionprobe_version)

    args = parser.parse_args()

    return args

class OnionprobeConfig:
    """
    Onionprobe class with configuration-related methods.
    """

    def get_config(self, item, default = None):
        """
        Helper to get instance configuration

        Retrieve a config parameter from the self.config object or use a
        default value as fallback

        :type  item: str
        :param item: Configuration item name

        :param default: Default config value to be used as a fallback if there's
                        no self.config[item] available.
                        Defaults to None

        :return: The configuration parameter value or the default fallback value.
        """

        if item in self.config:
            return self.config[item]

        # Optionally override the default with an argument provided
        elif default is not None:
            self.config[item] = default

            return default

        return defaults[item]

class OnionprobeConfigCompiler:
    """Base class to build Onionprobe configs from external sources of Onion Services"""

    def __init__(self, databases, template_config = None, output_path = None):
        """
        Constructor for the OnionprobeConfigCompiler class.

        Loads the default Onionprobe configuration to be used as a template.

        Keeps the dictionary of Onion Services databases as a class attribute.

        :type  databases: dict
        :param databases: Dictionary of data sources to fetch .onion sites.
                          Format is { 'database_name': 'database_url' }

        :type  template_config: str
        :param template_config: Configuration file path to be used as template

        :type  output_path: str
        :param output_path: Output folder where configs are written
        """

        # Save the databases of Onion Services
        self.databases = databases

        # Determine the default configuration file
        if template_config is None:
            template_config = os.path.join(basepath, 'configs', 'tor.yaml')

        # Determine the output path
        if output_path is None:
            self.output_path = os.path.join(basepath, 'configs')
        else:
            self.output_path = output_path

        # Load the default configuration file as a template
        if os.path.exists(template_config):
            with open(template_config, 'r') as config:
                self.config = yaml.load(config, yaml.CLoader)

    def build_endpoints_config(self, database):
        """
        Build the Onion Service endpoints dictionary.

        This method is only a placeholder.

        By default this method returns an empty dictionary as it's meant to be
        overriden by specific implementations inheriting from the
        OnionprobeConfigCompiler base class and where custom logic for
        extracting .onion endpoints from external databases should be located.

        :type database : str
        :param database: A database name from the databases dictionary. This
                         parameter allows accesing the URL of the external
                         database from the self.databases class attribute.

        :rtype: dict
        :return: Onion Service endpoints in the format accepted by Onionprobe.
        """

        return dict()

    def build_onionprobe_config(self):
        """
        Build an Onionprobe config.

        Writes an Onionprobe-compatible configuration file for each database
        listed in self.databases attribute.

        The Onion Service endpoints are generated from the
        build_endpoints_config() methods. To be effective, it's required that
        classes inheriting from this base class to implement the
        build_endpoints_configs() method.

        The filenames ared derived from the database names (each key from the
        self.databases attribute).
        """

        for database in self.databases:
            try:
                # Build list of endpoints
                endpoints = self.build_endpoints_config(database)

                # Create a new config using the default as base
                config = dict(self.config)

                # Replace the endpoints
                config['endpoints'] = endpoints

                # Save
                with open(os.path.join(self.output_path, database + '.yaml'), 'w') as output:
                    output.write(yaml.dump(config))

            except Exception as e:
                print(e)
