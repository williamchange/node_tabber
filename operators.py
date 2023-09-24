import bpy
import json
import time

from . import nt_extras, nodelists, utils

from bpy.types import Operator
from pathlib import Path

ADDON_PATH = Path(__file__).parent
TALLY_PATH = ADDON_PATH / "tally_cache"
ADDON_NAME = ADDON_PATH.name

# Create Folder for caching node tallies
if not TALLY_PATH.exists():
    TALLY_PATH.mkdir()

editor_type = {
    "CompositorNodeTree" : "compositor",
    "GeometryNodeTree" : "geometry",
    "TextureNodeTree" : "texture",
    "ShaderNodeTree" : "shader",
}
    
    
def fetch_user_prefs(attr_id=None):
    prefs = bpy.context.preferences.addons[__package__].preferences
    if attr_id is None:
        return prefs
    else:
        return getattr(prefs, attr_id)


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

    # TODO - Add poll function to only execute operator when current space type is NODE_EDITOR
    #@classmethod
    #def poll(self, context):

    @staticmethod
    def update_tally(context, entry):
        prefs = fetch_user_prefs() 
        tree_type = context.space_data.tree_type
        category_name = f'{tree_type.removesuffix("NodeTree").lower()}.json'

        path = Path(TALLY_PATH, category_name)
        if path.exists():
            with open(path, "r") as f:
                tally_dict = json.load(f)
        else:
            tally_dict = {}

        tally_dict[entry] = min(tally_dict.get(entry, 0) + 1, prefs.tally_weight)

        with open(path, "w") as f:
            json.dump(tally_dict, f, indent=4)


    # TODO - Verify if this caching is still necessary to prevent enum_callback bug
    @cache_enum_results
    def define_items(self, context):
        tree_type = context.space_data.tree_type

        if tree_type is not None:
            items = nodelists.generate_entries(context, editor_type=tree_type)
        else:
            items = []

        #if fetch_user_prefs("sub_search"):
        #    items.extend(append_subtypes(items))

        return items

    search_entry: bpy.props.EnumProperty(items = define_items, name='New Name', default=None)

    def execute(self, context):
        prefs = fetch_user_prefs()
        node_type, function_name, settings = nodelists.settings_dict.get(self.search_entry)
        if settings is None:
            settings = {}

        self.report({'INFO'}, f"Selected: {self.search_entry} - {function_name}:{settings}")
        function = getattr(utils, function_name)
        nodes = function(context, node_type, **settings)

        # Note - Disabled for easy debugging, will enable later
        #if not prefs.quick_place:
        #    bpy.ops.node.translate_attach_remove_on_cancel("INVOKE_DEFAULT")

        self.update_tally(context, entry=self.search_entry)
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.invoke_search_popup(self)
        return {'CANCELLED'}


class NODE_OT_reset_tally(Operator):
    """Reset the tally count"""

    bl_idname = "node.reset_tally"
    bl_label = "Reset node tally count"

    def execute(self, context):
        tally_files = tuple(TALLY_PATH.glob("*.json"))

        if len(tally_files) <= 0:
            self.report({"INFO"}, "No tallies to reset.")
            return {"CANCELLED"}

        for tally_file in tally_files:
            tally_file.unlink()

        self.report({"INFO"}, "Successfully reset tallies.")

        return {"FINISHED"}


classes = (
    NODE_OT_add_tabber_search,
    NODE_OT_reset_tally
    )


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
