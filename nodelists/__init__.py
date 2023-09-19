from . import CompositorNodeTree, GeometryNodeTree, ShaderNodeTree, TextureNodeTree
from bpy.types import Node
from bpy.app.translations import (
    pgettext_iface as iface_,
    contexts as i18n_contexts,
)


data_list = {
    "CompositorNodeTree" : CompositorNodeTree,
    "GeometryNodeTree" : GeometryNodeTree,
    "ShaderNodeTree" : ShaderNodeTree,
    "TextureNodeTree" : TextureNodeTree,
}

def add_abbreviation(label):
    abbr = "".join(word[0] for word in label.replace("/", " ").split())
    return f"{label} ({abbr})"

def generate_label(idname):
    bl_rna = Node.bl_rna_get_subclass(idname)
    if bl_rna is not None:
        #return idname #Note - Temporary for easier debugging, should change back to label
        return add_abbreviation(bl_rna.name)

    else:
        return "Unknown"
        #TODO - Catch errors when node type isn't valid, right now just ignore them
        #raise ValueError(f"'{idname}' is not a valid node type.")

def generate_entry_item(item):
    if isinstance(item, tuple):
        item, properties, *_ = item
        label = properties.get("label")
        return (item, add_abbreviation(label), "")
    else:
        return (item, generate_label(item), "")


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
            entries += [generate_entry_item(item) for item in item_list]
     
    return entries
