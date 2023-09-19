from . import CompositorNodeTree, GeometryNodeTree, ShaderNodeTree, TextureNodeTree
from bpy.types import Node

data_list = {
    "CompositorNodeTree" : CompositorNodeTree,
    "GeometryNodeTree" : GeometryNodeTree,
    "ShaderNodeTree" : ShaderNodeTree,
    "TextureNodeTree" : TextureNodeTree,
}

def generate_label(idname):
    bl_rna = Node.bl_rna_get_subclass(idname)

    if bl_rna is not None:
        return idname #Note - Temporary for easier debugging, should change back to label
        bl_label = bl_rna.name
        # Split abbreviation based on spaces and backslash
        abbr = "".join(word[0] for word in bl_label.replace("/", " ").split())
        return f"{bl_label} ({abbr})"

    else:
        return "Unknown"
        #TODO - Catch errors when node type isn't valid, right now just ignore them
        #raise ValueError(f"'{idname}' is not a valid node type.")

def generate_entries(context, editor_type):
    entries = []
    data = data_list.get(editor_type)

    if data is None:
        raise ValueError(f"Node Tabber does not support editor type '{editor_type}'")

    for item_list, poll, poll_args in data.all_items:
        # Note - Move the poll checking inside function call so that it updates according to context
        if poll is None:
            poll_passed = True
        else:
            if poll_args is None:
                poll_args = {}
            poll_passed = poll(context, **poll_args)

        if poll_passed:
            entries += [(item, generate_label(item), "") for item in item_list]
     
    return entries
