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

def fetch_active_nodetree(context):
    edit_tree = context.space_data.edit_tree
    node_tree = context.space_data.node_tree

    if edit_tree is not None:
        return edit_tree
    else:
        return node_tree

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


def create_node(context, node_type=None, *_, node_tree=None, **settings):
    tree = fetch_active_nodetree(context)
    node = tree.nodes.new(type=node_type)

    if settings is not None:
        for key, value in settings.items():
            setattr(node, key, value)

    if node_tree is not None:
        node.node_tree = context.blend_data.node_groups.get(node_tree)        

    node.location = context.space_data.cursor_location
    return (node,)


def create_zone(context, *_, input_type=None, output_type=None, offset=(150, 0), **settings,):
    tree = fetch_active_nodetree(context)
    input_node = tree.nodes.new(type=input_type)
    output_node = tree.nodes.new(type=output_type)

    # Simulation input must be paired with the output.
    input_node.pair_with_output(output_node)

    for node in (input_node, output_node):
        node.location = context.space_data.cursor_location

    x_offset, y_offset = offset
    input_node.location.x -= x_offset
    input_node.location.y -= y_offset
    output_node.location.x += x_offset
    output_node.location.y += y_offset

    # Connect geometry sockets by default.
    # Get the sockets by their types, because the name is not guaranteed due to i18n.
    from_socket = next(s for s in input_node.outputs if s.type == 'GEOMETRY')
    to_socket = next(s for s in output_node.inputs if s.type == 'GEOMETRY')
    tree.links.new(to_socket, from_socket)
    return (input_node, output_node)


def make_selection(context, nodes):
    tree = fetch_active_nodetree(context)
    # select only the new node
    for n in tree.nodes:
        n.select = False
    
    for n in nodes:
        n.select = True

    tree.nodes.active = nodes[-1]

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

# TODO - Make this more extensible instead of having to define stuff in a dictionary
functions = {
    "create_node" : create_node,
    "create_zone" : create_zone,
}

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
        #    items.extend(append_subtypes(items))

        return items

    my_enum: bpy.props.EnumProperty(items = define_items, name='New Name', default=None)

    def execute(self, context):
        prefs = fetch_user_prefs()
        node_type, function_name, settings = nodelists.settings_dict.get(self.my_enum)
        if settings is None:
            settings = {}

        self.report({'INFO'}, f"Selected: {self.my_enum} - {function_name}:{settings}")
        function = functions.get(function_name)
        nodes = function(context, node_type, **settings)

        make_selection(context, nodes)

        # Note - Disabled for easy debugging, will enable later
        #if not prefs.quick_place:
        #    bpy.ops.node.translate_attach_remove_on_cancel("INVOKE_DEFAULT")

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
