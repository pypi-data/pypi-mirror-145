#!/usr/bin/env python3
# -*- coding:utf-8; mode:python -*-
#
# Copyright 2020-2022 Pradyumna Paranjape
# This file is part of psprint.
#
# psprint is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# psprint is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with psprint.  If not, see <https://www.gnu.org/licenses/>.
#
"""
Read configuration files from default locations
"""

import os

import xdgpspconf

from psprint.printer import PrintSpace


def read_config(custom: os.PathLike = None) -> PrintSpace:
    """
    Read psprint configurations from various locations

    Args:
        custom: custom location for configuration

    Returns:
        configured ``PrintSpace``

    Raises:
        BadMark- Bad configuration file format
    """

    discoverer = xdgpspconf.ConfDisc(project='psprint', shipped=__file__)
    default_print = PrintSpace()
    config = discoverer.read_config(custom=custom,
                                    trace_pwd=True,
                                    cname='style.yml')
    for config, style in reversed(list(config.items())):
        default_print.set_opts(style, str(config))
    return default_print
