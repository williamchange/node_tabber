import itertools

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

    group_entries = [generate_entry_item(nodegroup_id(group), label=group.name, settings={"node_tree": group.name})
        for group in valid_groups]

    return group_entries


def abbreviation(label):
    #Note - Remove symbols like "-" "_" "()" "[]"
    stripped_label = label
    for char in ("/", "\\", "-", "_"):
        stripped_label = stripped_label.replace(char, " ")

    for parens in ("()", "[]", "{}"):
        for char in parens:
            stripped_label = stripped_label.replace(char, "")

    abbr = "".join(word[0] for word in stripped_label.split())
    return f"({abbr})"


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
    
    label = iface_(label)
    if subtype_labels is not None:
        subtype_string = " ".join(subtype_labels) + " > "
    else:
        subtype_string = ""

    return f"{subtype_string}{label} {abbreviation(label)}"


def fetch_subtypes_from_bl_rna(node_id, name, only_include=None):
    enum_list = Node.bl_rna_get_subclass(node_id).properties[name].enum_items.values()
    if only_include is not None:
        enum_list = (item for item in enum_list if (item.name in only_include))

    return enum_list

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


def filter_by_poll(context, entries):
    for entry in entries:
        if not isinstance(entry, tuple):
            yield entry
        else:
            item_list, poll, poll_args = entry
            if poll_args is None:
                poll_args = {}
                
            if poll(context, **poll_args):
                yield item_list


def is_entry_valid(entry, properties):
    return Node.bl_rna_get_subclass(entry) is None and (properties.get("function") != "create_zone")

def generate_entries(context, editor_type):
    entries = []
    settings_dict.clear()
    prefs = utils.fetch_user_prefs()
    data = data_list.get(editor_type)

    if data is None:
        raise ValueError(f"Node Tabber does not support editor type '{editor_type}'")
    
    for item in itertools.chain(*filter_by_poll(context, data.all_items)):
        if isinstance(item, tuple):
            idname, properties, *_ = item   
        else:
            idname, properties = item, {}

        # Add check for skipping invalid entries to prevent the function from short-circuiting
        if is_entry_valid(idname, properties):
            print(f"Node Tabber: {idname} is not a valid node type, entry not included in search.")
            continue

        subtypes = properties.get("subtypes", None)
        only_subtypes = properties.get("only_subtypes", False)

        if not only_subtypes:
            entries.append(generate_entry_item(idname, **properties))

        # TODO - Move most of this code to its own function once functionality is finalized
        if prefs.sub_search and subtypes is not None:
            enum_list, name_list = [], []
            for subtype in subtypes:
                if isinstance(subtype, dict):
                    enum_list.append(fetch_subtypes_from_bl_rna(idname, **subtype))
                    name_list.append(subtype.get("name"))
                else:
                    enum_list.append(fetch_subtypes_from_bl_rna(idname, subtype))
                    name_list.append(subtype)

            for props in itertools.product(*enum_list):
                subtype_labels = [prop.name for prop in props]
                subtype_settings = {name:prop.identifier for (name, prop) in zip(name_list, props)}
                entries.append(generate_entry_item(idname, subtype_labels=subtype_labels, subtype_settings=subtype_settings, **properties))

    entries.extend(generate_nodegroup_entries(context))
    return entries
