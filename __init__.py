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
#  Information:  https://teredo.tech        ###
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
    "version": (0, 0, 2, 0),
    "blender": (2, 7, 9),
    "location": "Nodes > CustomNodesTree > Add user nodes",
    "description": "Computer vision node-based programming",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Node"
}


import sys
import os
import bpy


if __name__ != "ocvl":
    sys.modules["ocvl"] = sys.modules[__name__]

from .ui import INFO_HT_header_new, INFO_HT_header_old


BASE_DIR = os.path.dirname(__file__)
IS_WORK_ON_COPY_INPUT = True


def register():
    try:
        bpy.utils.unregister_class(INFO_HT_header_old)
    except:
        print("INFO_HT_header_old Unregistered")
    bpy.utils.register_class(INFO_HT_header_new)
    from .extend.operatores import register; register()


def unregister():
    bpy.utils.unregister_class(INFO_HT_header_new)
    from .extend.operatores import unregister; unregister()