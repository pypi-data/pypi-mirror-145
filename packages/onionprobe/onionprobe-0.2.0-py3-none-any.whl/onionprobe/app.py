#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Onionprobe test/monitor tool.
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

from .init       import OnionprobeInit
from .config     import OnionprobeConfig
from .logger     import OnionprobeLogger
from .time       import OnionprobeTime
from .tor        import OnionprobeTor
from .descriptor import OnionprobeDescriptor
from .metrics    import OnionprobeMetrics
from .prober     import OnionprobeProber
from .http       import OnionprobeHTTP
from .teardown   import OnionprobeTeardown
from .main       import OnionprobeMain

class Onionprobe(
        # Inherit from subsystems
        OnionprobeInit,
        OnionprobeConfig,
        OnionprobeLogger,
        OnionprobeTime,
        OnionprobeTor,
        OnionprobeDescriptor,
        OnionprobeMetrics,
        OnionprobeProber,
        OnionprobeHTTP,
        OnionprobeTeardown,
        OnionprobeMain,
        ):
    """
    Onionprobe class to test and monitor Tor Onion Services
    """

def run(args):
    """
    Run Onionprobe from arguments

    :type  args: dict
    :param args: Instance arguments.
    """

    # Dispatch
    try:
        probe = Onionprobe(args)

        if probe.initialize() is not False:
            probe.run()
            probe.close()
        else:
            print('Error: could not initialize')
            exit(1)

    #except (FileNotFoundError, KeyboardInterrupt) as e:
    except Exception as e:
        probe.log(e, 'error')
        probe.close()
        exit(1)

def run_from_cmdline():
    """
    Run Onionprobe getting arguments from the command line.
    """

    from .config import cmdline

    run(cmdline())
