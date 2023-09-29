import bpy
from bpy.types import AddonPreferences
from bpy.props import BoolProperty, IntProperty
import rna_keymap_ui

addon_keymaps = []

class NodeTabberPreferences(AddonPreferences):
    bl_idname = __package__

    include_subtypes: BoolProperty(
        name="Include Subtypes",
        default=True,
        description='Include node subtypes in search entries. Ex: Math node will include operations such as Add, Subtract, etc',
    )

    quick_place: BoolProperty(
        name='Enable "Quick Place"',
        default=False,
        description="Once a node entry is selected, immediately place it on the nodetree",
    )

    use_op_symbols: BoolProperty(
        name="Use Operation Symbols",
        default=True,
        description='Add a symbol for specific math operations. Ex: "Add > Math (M)" becomes "Add (+) > Math (M)"',
    )

    sort_by_tally: BoolProperty(
        name="Enable Sort By Tally",
        default=True,
        description='When enabled, more frequently used entries get place higher on search results',
    )

    hide_group_selector: BoolProperty(
        name="Hide Group Selector",
        default=True,
        description='When enabled, more frequently used entries get place higher on search results',
    )
    
    tally_max: IntProperty(
        name="Tally Max",
        default=35,
        description='Sets the maximum cap for tallies, which affects their ranking when "Sort By Tally" is enabled',
        min=0,
        soft_max=9999,
    )

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        col1 = row.column(align=True)
        col1.label(text="Node Options:")
        col1.prop(self, "quick_place")
        col1.prop(self, "hide_group_selector")

        col1.separator()
        col1.label(text="Search Options:")
        col1.prop(self, "include_subtypes")
        if self.include_subtypes:
            col1.prop(self, "use_op_symbols")

        col2 = row.column()
        col2.label(text="Tally Options:")
        subrow = col2.row(align=True)
        subrow.prop(self, "sort_by_tally")
        subrow.prop(self, "tally_max")
        col2.operator("node.reset_tallies")

        # Keymaps
        box = layout.box()
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
