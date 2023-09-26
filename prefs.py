import bpy
from bpy.types import AddonPreferences
from bpy.props import BoolProperty, IntProperty
import rna_keymap_ui

addon_keymaps = []

class NodeTabberPreferences(AddonPreferences):
    bl_idname = __package__

    sort_by_tally: BoolProperty(
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

    sub_search: BoolProperty(
        name="Enable Sub Searching",
        default=True,
        description="Allows searching within node operations. Eg. PP could return Ping-Pong in the Math node.",
    )

    use_op_symbols: BoolProperty(
        name="Use Operation Symbols",
        default=False,
        description='Replaces math op abbreviations with their symbols. Eg. "ADD (A) MATH" becomes "ADD (+) MATH".',
    )

    def draw(self, context):
        layout = self.layout
        col2.operator("node.reset_tallies")
        # row4.label(text="NOTE: CTRL + TAB : Performs \"Edit Group\" functionality.")

        # Keymaps
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
    bpy.utils.register_class(NodeTabberPreferences)

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

    bpy.utils.unregister_class(NodeTabberPreferences)
