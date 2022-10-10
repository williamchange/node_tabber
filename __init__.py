# ##### BEGIN GPL LICENSE BLOCK #####
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
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


bl_info = {
    "name": "Node Tabber",
    "author": "Richard Lyons <info@rixiefx.com>",
    "version": (0, 1, 4),
    "blender": (3, 1, 0),
    "description": "Allows quick smart searching of node types.",
    "category": "Node",
}

import bpy
from bpy.types import (
    AddonPreferences,
)
from bpy.props import (
    BoolProperty,
    IntProperty,
)
from . import operators
import rna_keymap_ui


addon_keymaps = []


class node_tabberPreferences(AddonPreferences):
    # This must match the addon name, use '__package__'
    # when defining this in a submodule of a python package.

    bl_idname = __name__

    tally: BoolProperty(
        name="Enable tally count",
        default=True,
        description="Enables Node Tabber to keep a tally of most used nodes, and populate popup accordingly.",
    )
    tally_weight: IntProperty(
        name="Tally Weight",
        default=35,
        description='Maximum number of tallies for each node selected. Affects the "weighting" of the order of tallied results in the node list.',
    )
    quick_place: BoolProperty(
        name='Enable "Quick Place"',
        default=False,
        description="Allows immediate placement of selected node.",
    )
    nt_debug: BoolProperty(
        name="Debug Output",
        default=False,
        description="Prints Node Tabber debug to console.",
    )
    sub_search: BoolProperty(
        name="Enable Sub Searching",
        default=True,
        description="Allows searching within node operations. Eg. PP could return Ping-Pong in the Math node.",
    )

    def draw(self, context):
        layout = self.layout

        # Prefs

        box = layout.box()
        row1 = box.row()
        row2 = box.row()
        row3 = box.row()
        row4 = box.row()
        row1.prop(self, "sub_search")
        row1.prop(self, "quick_place")
        row2.prop(self, "tally")
        row2.operator("node.reset_tally", text="Reset Tally")
        row2.prop(self, "tally_weight")
        # row2.prop(self, "nt_debug")
        # row4.label(text="NOTE: CTRL + TAB : Performs \"Edit Group\" functionality.")

        # Keymaps

        # box = layout.box()
        col = box.column()
        col.label(text="Keymap List:", icon="KEYINGSET")

        wm = bpy.context.window_manager
        kc = wm.keyconfigs.user
        old_km_name = ""
        get_kmi_l = []
        for km_add, kmi_add in addon_keymaps:
            for km_con in kc.keymaps:
                if km_add.name == km_con.name:
                    km = km_con
                    break

            for kmi_con in km.keymap_items:
                if kmi_add.idname == kmi_con.idname:
                    if kmi_add.name == kmi_con.name:
                        get_kmi_l.append((km, kmi_con))

        get_kmi_l = sorted(set(get_kmi_l), key=get_kmi_l.index)

        for km, kmi in get_kmi_l:
            if not km.name == old_km_name:
                col.label(text=str(km.name), icon="DOT")
            col.context_pointer_set("keymap", km)
            rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)
            col.separator()
            old_km_name = km.name


def register():
    operators.register()
    bpy.utils.register_class(node_tabberPreferences)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(
            name="Node Editor", space_type="NODE_EDITOR"
        )
        kmi = km.keymap_items.new("node.add_tabber_search", type="TAB", value="PRESS")
        addon_keymaps.append((km, kmi))
        kmi = km.keymap_items.new(
            "node.group_edit", type="TAB", value="PRESS", ctrl=True
        )
        addon_keymaps.append((km, kmi))


def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    operators.unregister()
    bpy.utils.unregister_class(node_tabberPreferences)
