import bpy
import json
import time

from . import nt_extras
from . import nodelists

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

def write_score(enum_items):
    tree_type = bpy.context.space_data.tree_type
    category = f'{tree_type.removesuffix("NodeTree").lower()}.json'
    prefs = bpy.context.preferences.addons[ADDON_NAME].preferences

    path = Path(TALLY_PATH, category)
    if not path.exists():
        with open(path, "w") as f:
            json.dump({enum_items: {"tally": 1}}, f, indent=4)

        print(f"Nodetabber created : {path}")
    else:
        with open(path, "r") as f:
            tally_dict = json.load(f)

        old_tally = tally_dict.get(enum_items, {"tally": 0})["tally"]
        new_tally = min(old_tally + 1, prefs.tally_weight)
        tally_dict[enum_items] = {"tally": new_tally}

        with open(path, "w") as f:
            json.dump(tally_dict, f, indent=4)

    return


def fetch_user_prefs(attr_id=None):
    prefs = bpy.context.preferences.addons[__package__].preferences
    if attr_id is None:
        return prefs
    else:
        return getattr(prefs, attr_id)


def append_subtypes(items):
    from . import nt_extras
    editor_type = bpy.context.space_data.tree_type
    prefs = fetch_user_prefs()
    sn_entries = nt_extras.subnode_entries(use_symbols=prefs.use_op_symbols, editor_type=editor_type)

    subitems = []
    for node, *_ in items:
        subtypes = sn_entries.get(node, None)

        if subtypes is not None:
            for item in subtypes:
                subitems.append((*item, ""))
    
    return subitems


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
    bl_property = "my_enum"

    # TODO - Add poll function to only execute operator when current space type is NODE_EDITOR
    #@classmethod
    #def poll(self, context):

    # TODO - Verify if this caching is still necessary to prevent enum_callback bug
    @cache_enum_results
    def define_items(self, context):
        tree_type = context.space_data.tree_type

        if tree_type is not None:
            items = nodelists.generate_entries(context, editor_type=tree_type)
        else:
            items = []

        #if fetch_user_prefs("sub_search"):
        #    items += append_subtypes(items)

        return items

    my_enum: bpy.props.EnumProperty(items = define_items, name='New Name', default=None)

    def execute(self, context):
        self.report({'INFO'}, f"Selected: {self.my_enum}")
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
