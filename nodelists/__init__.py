from . import CompositorNodeTree, GeometryNodeTree, ShaderNodeTree, TextureNodeTree
from .. import utils

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

def generate_nodegroup_entries(context):
    active_tree = utils.fetch_active_nodetree(context)
    node_groups = context.blend_data.node_groups

    valid_groups = (group for group in node_groups
        if (group.bl_idname == active_tree.bl_idname and
            group.name != active_tree.name and
            not group.contains_tree(active_tree) and
            not group.name.startswith('.'))
    )

    # Note - Function for converting strings like 'ShaderNodeTree' to 'ShaderNodeGroup'
    nodegroup_id = lambda group : group.bl_idname.removesuffix("Tree").__add__("Group")
    

    group_entries = [generate_entry_item(nodegroup_id(group), 
            **{
                "label":group.name, 
                "settings":{"node_tree": group.name}
            })
        for group in valid_groups
        ]

    return group_entries


def add_abbreviation(label):
    abbr = "".join(word[0] for word in label.replace("/", " ").split())
    return f"{label} ({abbr})"


def generate_label(idname=None, label=None, subtype_labels=None):
    if (label is None) and (idname is None):
        raise ValueError("Both idname and label inputs are None.")

    if label is None:
        bl_rna = Node.bl_rna_get_subclass(idname)
        if bl_rna is not None:
            label = bl_rna.name
            #label = idname #Note - Temporary for easier debugging, should change back to label
        else:
            raise ValueError(f"'{idname}' is not a valid node type.")
    
    with_abbr = add_abbreviation(iface_(label))

    if subtype_labels is not None:
        subtype_string = " ".join(subtype_label.title() for subtype_label in subtype_labels) + " > "
    else:
        subtype_string = ""

    return f"{subtype_string}{with_abbr}"

def fetch_subtypes_from_bl_rna(node_id, subtype_id):
    return Node.bl_rna_get_subclass(node_id).properties[subtype_id].enum_items.values()

def merge_settings(settings, subtype_settings):
    all_settings = {}
    for i in (settings, subtype_settings):
        if i is not None:
            all_settings.update(i)
    
    return all_settings


def generate_entry_item(idname, label=None, function="create_node", settings=None, subtype_labels=None, subtype_settings=None, **kwargs):
    enum_label = generate_label(idname, label, subtype_labels)
    identifier = str((idname, enum_label))

    all_settings = merge_settings(settings, subtype_settings)

    settings_dict[identifier] = (idname, function, all_settings)
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
            for item in item_list:
                if isinstance(item, tuple):
                    idname, properties, *_ = item   
                    subtypes = properties.get("subtypes")
                else:
                    idname, properties = item, {}
                    subtypes = None

                entries.append(generate_entry_item(idname, **properties))

                # TODO - Make this support multiple subtype products, not just single subtypes
                # TODO - Move most of this code to its own function once functionality is finalized
                if subtypes is not None:
                    for subtype in subtypes:
                        for subtype_value in fetch_subtypes_from_bl_rna(idname, subtype):
                            value_id = subtype_value.identifier
                            value_label = subtype_value.name
                            subtype_labels = [value_label]
                            subtype_settings = {subtype : value_id}
                            entries.append(generate_entry_item(idname, subtype_labels=subtype_labels, subtype_settings=subtype_settings, **properties))

    entries.extend(generate_nodegroup_entries(context))
    return entries
