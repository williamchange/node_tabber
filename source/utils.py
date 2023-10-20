import json

from bpy import context
from pathlib import Path

ADDON_FOLDER = Path(__file__).parent
TALLY_FOLDER = ADDON_FOLDER / "tally_cache"

# Create Folder for caching node tallies
if not TALLY_FOLDER.exists():
    TALLY_FOLDER.mkdir()
    

nodes_with_op_symbols = [
    "ShaderNodeMath",
    "CompositorNodeMath",
    "TextureNodeMath",
    "ShaderNodeVectorMath",
    "FunctionNodeBooleanMath",
    "FunctionNodeCompare",
]

op_symbol_dict = {
    "Add" : "+",
    "Subtract" : "-",
    "Multiply" : "*",
    "Divide" : "/",
    "Multiply Add" : "*+",
    "Power" : "^",
    "Exponent" : "e^",
    "Less Than" : "<",
    "Less Than or Equal" : "<=",
    "Greater Than" : ">",
    "Greater Than or Equal" : ">=",
    "Scale" : "*",
    "Cross Product" : "x",
    "And" : "^",
    "Or" : "v",
    "Not" : "!",
    "Not And" : "!^",
    "Nor" : "!v",
    "Equal" : "=",
    "Not Equal" : "!=",
    "Imply" : "->",
}


def add_op_symbols(operation):
    op_symbol = op_symbol_dict.get(operation)
    if op_symbol is not None:
        return f"{operation} ({op_symbol})"

    return operation


def fetch_tally_path(tree_type):
    return Path(TALLY_FOLDER, f'{tree_type}.json')    


def fetch_user_prefs(attr_id=None):
    prefs = context.preferences.addons["Node Tabber"].preferences
    if attr_id is None:
        return prefs
    else:
        return getattr(prefs, attr_id)


def sort_enum_items(tree_type, items):
    path = fetch_tally_path(tree_type)
    if path.exists():
        with open(path, "r") as f:
            tally_dict = json.load(f)

        items.sort(key=lambda x : tally_dict.get(x[0], 0), reverse=True)


def update_tally(context, entry):
    prefs = fetch_user_prefs() 
    tree_type = context.space_data.tree_type

    path = fetch_tally_path(tree_type)
    if path.exists():
        with open(path, "r") as f:
            tally_dict = json.load(f)
    else:
        tally_dict = {}

    tally_dict[entry] = min(tally_dict.get(entry, 0) + 1, prefs.tally_max)

    with open(path, "w") as f:
        json.dump(tally_dict, f, indent=4)


def fetch_active_nodetree(context):
    edit_tree = context.space_data.edit_tree
    node_tree = context.space_data.node_tree

    if edit_tree is not None:
        return edit_tree
    else:
        return node_tree


def create_node(context, node_type=None, *_, node_tree=None, **settings):
    tree = fetch_active_nodetree(context)
    node = tree.nodes.new(type=node_type)
    prefs = fetch_user_prefs()

    try:
        if settings is not None:
            for key, value in settings.items():
                setattr(node, key, value)

        if node_tree is not None:
            node.node_tree = context.blend_data.node_groups.get(node_tree)   
            node.show_options = not prefs.hide_group_selector

        node.location = context.space_data.cursor_location
        return make_selection(context, nodes=(node,))
    
    except Exception as error:
        tree.nodes.remove(node)
        raise error


def create_zone(context, *_, input_type=None, output_type=None, offset=(150, 0), **settings,):
    tree = fetch_active_nodetree(context)
    input_node = tree.nodes.new(type=input_type)
    output_node = tree.nodes.new(type=output_type)

    try:
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

        return make_selection(context, nodes=(input_node, output_node))
    
    except Exception as error:
        tree.nodes.remove(input_node)
        tree.nodes.remove(output_node)
        raise error


def make_selection(context, nodes):
    tree = fetch_active_nodetree(context)
    # select only the new node
    for n in tree.nodes:
        n.select = False
    
    for n in nodes:
        n.select = True

    tree.nodes.active = nodes[-1]
    return nodes