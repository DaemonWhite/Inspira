# capability.py
#
# Copyright 2025 DaemonWhite
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass, field


@dataclass(frozen=True)
class TagCapability:
    present: bool = False
    strict: bool = False
    include: bool = True
    exclude: bool = False
    know: list = field(default_factory=list)
    know_nsfw: list = field(default_factory=list)


@dataclass(frozen=True)
class EndPointCapability:
    present: bool = False
    nsfw: bool = False
    tag: TagCapability = field(default_factory=TagCapability)
    limit_min: int = 1
    limit_max: int = 1
    timeout: int = 5
    skip: int = -1
    sorts: list[str] = field(default_factory=list)
