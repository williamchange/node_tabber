import bpy

from . import nodelists, utils
from bpy.types import Operator
from bpy.props import EnumProperty

# EnumProperties that are generated dynamically tend to misbehave as Python tends to clean up memory
# Caching the results forces Python to keep track of the data while the operator is in use
enum_callback_cache = []
def cache_enum_results(function):
    def wrapped_func(self, context):
        enum_callback_cache.clear()
        output = function(self, context)
        enum_callback_cache.extend(output)
        return output
            
    return wrapped_func


class NODE_OT_add_tabber_search(Operator):
    '''Add a node to the active tree'''
    bl_idname = "node.add_tabber_search"
    bl_label = "Search and Add Node"
    bl_options = {'REGISTER', 'UNDO'}
    bl_property = "search_entry"

    @classmethod
    def poll(self, context):
        if hasattr(context, "space_data"):
            space = context.space_data
            has_tree = space.node_tree is not None
            is_node_editor = space.type == 'NODE_EDITOR'
            return has_tree and is_node_editor
        else:
            return False
            

    @cache_enum_results
    def define_items(self, context):
        prefs = utils.fetch_user_prefs()
        tree_type = context.space_data.tree_type

        items = nodelists.generate_entries(context, editor_type=tree_type)

        if prefs.sort_by_tally and (not context.preferences.use_recent_searches):
            utils.sort_enum_items(tree_type, items)

        return items

    search_entry: EnumProperty(items = define_items, name='Search Entry', default=None)

    def execute(self, context):
        prefs = utils.fetch_user_prefs()
        node_type, function_name, settings = nodelists.settings_dict.get(self.search_entry)
        if settings is None:
            settings = {}

        self.report({'INFO'}, f"Selected: {self.search_entry} - {function_name}:{settings}")
        function = getattr(utils, function_name)
        nodes = function(context, node_type, **settings)

        if not prefs.quick_place:
            bpy.ops.node.translate_attach_remove_on_cancel("INVOKE_DEFAULT")

        utils.update_tally(context, entry=self.search_entry)
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.invoke_search_popup(self)
        return {'CANCELLED'}


class NODE_OT_reset_tallies(Operator):
    """Reset the tally count"""
    bl_idname = "node.reset_tallies"
    bl_label = "Reset Tallies"

    def execute(self, context):
        tally_path = utils.TALLY_FOLDER
        tally_files = tuple(tally_path.glob("*.json"))

        if len(tally_files) <= 0:
            self.report({"INFO"}, "No tallies to reset.")
            return {"CANCELLED"}

        for tally_file in tally_files:
            tally_file.unlink()

        self.report({"INFO"}, "Successfully reset tallies.")

        return {"FINISHED"}


classes = (
    NODE_OT_add_tabber_search,
    NODE_OT_reset_tallies
    )


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
