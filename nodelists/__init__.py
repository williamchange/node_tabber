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

settings_dict = {}

def fetch_active_nodetree(context):
    edit_tree = context.space_data.edit_tree
    node_tree = context.space_data.node_tree

    if edit_tree is not None:
        return edit_tree
    else:
        return node_tree


def generate_nodegroup_entries(context):
    active_tree = fetch_active_nodetree(context)
    node_groups = context.blend_data.node_groups

    valid_groups = (group for group in node_groups
        if (group.bl_idname == active_tree.bl_idname and
            group.name != active_tree.name and
            not group.contains_tree(active_tree) and
            not group.name.startswith('.'))
    )

    # Note - Function for converting strings like 'ShaderNodeTree' to 'ShaderNodeGroup'
    nodegroup_id = lambda group : group.bl_idname.removesuffix("Tree").__add__("Group")
    group_entries = [
        generate_entry_item((nodegroup_id(group), {
                "label":group.name, 
                "settings":{"node_tree": group.name}
            }))
        for group in valid_groups
        ]

    return group_entries


def add_abbreviation(label):
    abbr = "".join(word[0] for word in label.replace("/", " ").split())
    return f"{label} ({abbr})"


def generate_label(*, idname=None, label=None):
    if (label is None) and (idname is None):
        raise ValueError("Both idname and label inputs are None.")

    if label is None:
        bl_rna = Node.bl_rna_get_subclass(idname)
        if bl_rna is not None:
            label = bl_rna.name
            #label = idname #Note - Temporary for easier debugging, should change back to label
        else:
            raise ValueError(f"'{idname}' is not a valid node type.")
            
    return add_abbreviation(iface_(label))


def generate_entry_item(item):
    if isinstance(item, tuple):
        item, properties, *_ = item
        label = properties.get("label")
        enum_label = generate_label(label=label)
        settings = properties.get("settings")
        function = properties.get("function", "create_node")
    else:
        enum_label = generate_label(idname=item)
        settings = None
        function = "create_node"

    identifier = str((item, enum_label))
    settings_dict[identifier] = (item, function, settings)
    return (identifier, enum_label, "")


def generate_entries(context, editor_type):
    entries = []
    settings_dict.clear()
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
            entries.extend([generate_entry_item(item) for item in item_list])
     
    entries.extend(generate_nodegroup_entries(context))
    return entries
