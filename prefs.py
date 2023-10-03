import bpy
from bpy.types import AddonPreferences
from bpy.props import BoolProperty, IntProperty
from . import keymap_ui

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
        row = layout.split(factor=0.3)
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
        if context.preferences.use_recent_searches:
            box = col2.box().column(align=True)
            box.label(icon="ERROR", text="'Sort by Most Recent' is enabled.")
            box.separator(factor=1)
            box.label(text="To enable Node Tabber's own sorting, please turn")
            box.label(text="this setting off under Preferences > Interface > Display.")
        else:
            subrow = col2.row(align=True)
            subrow.prop(self, "sort_by_tally")
            subrow.prop(self, "tally_max")
            col2.operator("node.reset_tallies")

        keymap_ui.draw_keyboard_shorcuts(self, layout, context, 
            toggle_idname="node_tabber_show_keymaps", starting_indent_level=0)


def register():
    bpy.types.WindowManager.node_tabber_show_keymaps = BoolProperty(
        name="Show Keymaps",
        default=False,
        description="When enabled, displays keymap list"
    )

    bpy.utils.register_class(NodeTabberPreferences)


def unregister():
    bpy.utils.unregister_class(NodeTabberPreferences)
    del bpy.types.WindowManager.node_tabber_show_keymaps