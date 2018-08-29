#  ***** BEGIN GPL LICENSE BLOCK *****
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, see <http://www.gnu.org/licenses/>
#  and write to the Free Software Foundation, Inc., 51 Franklin Street,
#  Fifth Floor, Boston, MA  02110-1301, USA..
#
#  All rights reserved.
#
#  Contact:      dawid.aniol@teredo.tech    ###
#  Information:  http://teredo.tech         ###
#
#  ***** END GPL LICENSE BLOCK *****
#


bl_info = {
    "name": "ocvl",
    "author": (
        "Dawid Aniol",
        "OCVL team",
        "Teredo team",
    ),
    "version": (1, 0, 4),
    "blender": (2, 7, 9),
    "location": "Nodes > CustomNodesTree > Add user nodes",
    "description": "Computer vision node-based programming",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Node"
}


import sys

if __name__ != "ocvl":
    sys.modules["ocvl"] = sys.modules[__name__]

from .auth import register_extended_operators, unregister_extended_operators


def register():
    from .tutorial_engine import operatores as tutorial_operatores
    from . import ui
    from .operatores import operatores
    from .operatores import abc
    ui.register()
    operatores.register()
    register_extended_operators()
    tutorial_operatores.register()
    abc.register()


def unregister():
    from .tutorial_engine import operatores as tutorial_operatores
    from . import ui
    from .operatores import operatores
    from .operatores import abc
    ui.unregister()
    operatores.unregister()
    unregister_extended_operators()
    tutorial_operatores.unregister()
    abc.unregister()
