import bpy
from bpy.types import AddonPreferences
from bpy.props import BoolProperty, IntProperty, EnumProperty

from .keymaps import keymap_layout


class NodeTabberPreferences(AddonPreferences):
    bl_idname = "Node Tabber"

    show_keymaps : BoolProperty(
        name="Show Keymaps", 
        default=False, 
        description="When enabled, displays keymap list"
    )

    include_subtypes: BoolProperty(
        name="Include Subtypes",
        default=True,
        description="Include node subtypes in search entries. Ex: Math node will include operations such as Add, Subtract, etc.",
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
        description="When enabled, more frequently used entries get place higher on search results",
    )

    hide_group_selector: BoolProperty(
        name="Hide Group Selector",
        default=True,
        description="When enabled, more frequently used entries get place higher on search results",
    )

    tally_max: IntProperty(
        name="Tally Max",
        default=35,
        description='Sets the maximum cap for tallies, which affects their ranking when "Sort By Tally" is enabled',
        min=0,
        soft_max=9999,
    )

    mix_color_alias: EnumProperty(
        name="Mix Color Alias",
        items=(
            ("DEFAULT","Use Default Names","Keep the node names as-is. \n('Mix Color' for shaders, geometry, and compositor. 'Mix RGB for texture node editor')",),
            ("MIX_COLOR", "Use 'Mix Color'", "Use the label 'Mix Color' for both Mix Color and Mix RGB nodes"),
            ("MIX_RGB", "Use 'Mix RGB'", "Use the label 'Mix RGB' for both Mix Color and Mix RGB nodes"),
            ("BOTH", "Use Both Aliases", "Use both 'Mix Color' and 'Mix RGB' as valid search entries"),
        ),
        default="DEFAULT",
        description="Specifies how the Mix Color/Mix RGB nodes would be called across editors",
    )

    show_deprecated: EnumProperty(
        name="Display Deprecated Nodes",
        items=(
            ("SHOW_AND_INDICATE", "Show and Indicate", "Show deprecated nodes, but add a mark indicating they're deprecated",),
            ("SHOW_ONLY", "Show Only", "Show deprecated nodes as-is, without extra indication"),
            ("HIDE", "Hide", "Don't display nodes if they're marked as deprecated"),
        ),
        default="SHOW_AND_INDICATE",
        description="Specifies how nodes that are marked as deprecated will be handled",
    )

    include_external_nodes: BoolProperty(
        name="Include External Nodes",
        default=True,
        description="Include custom nodes by created by other addons in search entries. \n(Note: Only includes custom nodes that are registered as NodeItems)",
    )

    denote_name_collisions: BoolProperty(
        name="Denote Name Collisions",
        default=True,
        description="Prepend a hash symbol (#) to custom external nodes that share the same name as a built-in node",
    )

    def display_enum_prop(self, layout, prop_name):
        split = layout.split(factor=0.4)
        split.label(text=f"{self.get_prop_name(prop_name)}:")
        split.prop(self, prop_name, text="")

    def get_prop_name(self, prop_name):
        return self.__annotations__[prop_name].keywords["name"] 

    def draw(self, context):
        layout = self.layout
        row = layout.split(factor=0.31)
        col1 = row.column(align=True)
        col1.label(text="Node Options:")
        col1.prop(self, "quick_place")
        col1.prop(self, "hide_group_selector")

        col1.separator()
        col1.label(text="Search Options:")
        col1.prop(self, "include_subtypes")
        if self.include_subtypes:
            col1.prop(self, "use_op_symbols")
        
        col1.separator()
        col1.prop(self, "include_external_nodes")
        if self.include_external_nodes:
            col1.prop(self, "denote_name_collisions")

        col2 = row.column()
        col2.label(text="Tally Options:")

        use_recent_searches = getattr(context.preferences, "use_recent_searches", False)
        if use_recent_searches:
            box = col2.box().column(align=True)
            box.label(icon="ERROR", text="'Sort by Most Recent' is enabled.")
            box.separator(factor=1)
            box.label(text="To enable Node Tabber's own sorting, please turn the")
            box.label(text="aforementioned setting off under Preferences > Interface > Display.")
        else:
            subrow = col2.row(align=True)
            subrow.prop(self, "sort_by_tally")
            subrow.prop(self, "tally_max")
            col2.operator("node.reset_tallies")

            col2.separator()
            subcol = col2.column()
            subcol.label(text="Other Options:")
            self.display_enum_prop(subcol, "mix_color_alias")

            if bpy.app.version >= (4, 1):
                self.display_enum_prop(subcol, "show_deprecated")

        keymap_layout.draw_keyboard_shorcuts(self, layout, context)


keymap_layout.register_properties(preferences=NodeTabberPreferences)


def register():
    bpy.utils.register_class(NodeTabberPreferences)


def unregister():
    bpy.utils.unregister_class(NodeTabberPreferences)
