import itertools

from . import __poll_functions__ as poll_funcs
from .. import utils

from bpy.types import Node
from bpy.app.translations import (
    pgettext_iface as iface_,
    contexts as i18n_contexts,
)

from bpy.app import version as app_version
from nodeitems_utils import node_items_iter, NodeItemCustom

import bpy
import json
from pathlib import Path

NODELIST_PATH = Path(__file__).parent

settings_dict = {}
vanilla_nodelist = []
vanilla_labels = set()


if app_version[:2] > (3, 4):
    def contains_group(parent, group):
        return parent.contains_tree(group)
else:
    def contains_group(parent, group):
        node_tree_group_type = {
            "CompositorNodeTree": "CompositorNodeGroup",
            "ShaderNodeTree": "ShaderNodeGroup",
            "TextureNodeTree": "TextureNodeGroup",
            "GeometryNodeTree": "GeometryNodeGroup",
        }

        if parent == group:
            return True
        for node in parent.nodes:
            if node.bl_idname in node_tree_group_type.values() and node.node_tree is not None:
                if contains_group(node.node_tree, group):
                    return True
        return False

if bpy.app.version > (4, 3):
    def nodegroup_settings(group):
        return {
            "node_tree": group.name,
            "width" : group.default_group_node_width,
            }
else:
    def nodegroup_settings(group):
        return {"node_tree": group.name}


def generate_nodegroup_entries(context):
    active_tree = utils.fetch_active_nodetree(context)
    node_groups = context.blend_data.node_groups

    valid_groups = (
        group for group in node_groups
        if (
            group.bl_idname == active_tree.bl_idname
            and group.name != active_tree.name
            and not contains_group(parent=group, group=active_tree)
            and not group.name.startswith(".")
        )
    )

    # Note - Function for converting strings like 'ShaderNodeTree' to 'ShaderNodeGroup'
    nodegroup_id = lambda group: group.bl_idname.removesuffix("Tree").__add__("Group")

    group_entries = [
        generate_entry_item(nodegroup_id(group), label=group.name, settings=nodegroup_settings(group), can_cause_name_collision=True)
        for group in valid_groups
    ]

    return group_entries


def generate_custom_node_entries(context):
    builtin_nodes = set(vanilla_nodelist)
    
    custom_node_entries = [
        generate_entry_item(item.nodetype, label=item.label, settings=item.settings, can_cause_name_collision=True) 
        for item in node_items_iter(context) if not (isinstance(item, NodeItemCustom) or item.nodetype in builtin_nodes)
    ]

    return custom_node_entries


def abbreviation(label):
    # Note - Remove symbols like "-" "_" "()" "[]"
    stripped_label = label
    for char in ("/", "\\", "-", "_"):
        stripped_label = stripped_label.replace(char, " ")

    for char in ("*", "#"):
        stripped_label = stripped_label.replace(char, "")

    for parens in ("()", "[]", "{}"):
        for char in parens:
            stripped_label = stripped_label.replace(char, "")

    abbr = "".join(word[0] for word in stripped_label.split())
    return f"({abbr})"


def generate_label(idname=None, label=None, subtype_labels=None, can_cause_name_collision=False, is_deprecated=False):
    prefs = utils.fetch_user_prefs()

    if (label is None) and (idname is None):
        raise ValueError("Both idname and label inputs are None.")

    if label is None:
        bl_rna = Node.bl_rna_get_subclass(idname)
        if bl_rna is not None:
            label = bl_rna.name
            # label = idname #Note - Temporary for easier debugging, should change back to label
        else:
            raise ValueError(f"'{idname}' is not a valid node type.")

    if prefs.use_op_symbols and (subtype_labels is not None) and (idname in utils.nodes_with_op_symbols):
        subtype_labels = (utils.add_op_symbols(label) for label in subtype_labels)

    label = iface_(label)
    if subtype_labels is not None:
        subtype_string = " ".join(subtype_labels) + " > "
    else:
        subtype_string = ""
    
    if can_cause_name_collision:
        if label in vanilla_labels and prefs.denote_name_collisions:
            label = f"#{label}"
    else:
        vanilla_labels.add(label)

    if is_deprecated and prefs.show_deprecated == 'SHOW_AND_INDICATE':
        return f"[Deprecated] {subtype_string}{label} {abbreviation(label)}"
    else:
        return f"{subtype_string}{label} {abbreviation(label)}"


def fetch_subtypes_from_bl_rna(node_id, name, only_include=None, exclude=None):
    enum_list = Node.bl_rna_get_subclass(node_id).properties[name].enum_items.values()
    if only_include is not None:
        enum_list = (item for item in enum_list if (item.name in only_include))

    if exclude is not None:
        enum_list = (item for item in enum_list if (item.name not in exclude))

    return enum_list


def merge_settings(settings, subtype_settings):
    all_settings = {}
    for i in (settings, subtype_settings):
        if i is not None:
            all_settings.update(i)

    return all_settings


def generate_entry_item(
    idname, label=None, function="create_node", settings=None, subtype_labels=None, subtype_settings=None, can_cause_name_collision=False, is_deprecated=False, **kwargs
):
    enum_label = generate_label(idname, label, subtype_labels, can_cause_name_collision, is_deprecated)
    identifier = str((idname, enum_label))
    all_settings = merge_settings(settings, subtype_settings)

    settings_dict[identifier] = (idname, function, all_settings)
    if not can_cause_name_collision:
        vanilla_nodelist.append(idname)

    return (identifier, enum_label, "")


def process_entries(context, entries, *, poll=None, poll_args=None):
    if poll is None:
        return entries, True
    else:
        if poll_args is None:
            poll_args = {}

        poll = getattr(poll_funcs, poll)
        return entries, poll(context, **poll_args)


def filter_by_poll(context, entries):
    for entry in entries:
        entries, include = process_entries(context, **entry)
        if include:
            yield entries


def is_entry_invalid(entry, properties):
    if properties.get("function") != "create_zone":
        node_data = Node.bl_rna_get_subclass(entry)

        if node_data is not None:
            settings = properties.get("settings")
            if settings is not None:
                invalid = False
                for prop_name, value in settings.items():
                    props = (prop.identifier for prop in fetch_subtypes_from_bl_rna(entry, prop_name))
                    if value not in props:
                        invalid = True

                if invalid:
                    print(f"Node Tabber: {entry} - {properties} is not a valid node type, entry not included in search.")
                    return True
        else:
            print(f"Node Tabber: {entry} is not a valid node type, entry not included in search.")
            return True
    else:
        settings = properties["settings"]
        input_node_exists = Node.bl_rna_get_subclass(settings["input_type"]) is None
        output_node_exists = Node.bl_rna_get_subclass(settings["output_type"]) is None

        if input_node_exists and output_node_exists:
            print(f"Node Tabber: {entry} is not a valid node type, entry not included in search.")
            return True


def get_data_from_filepath(editor_type):
    version_number = ".".join(map(str, app_version[:2]))
    filepath = NODELIST_PATH / version_number / f"{editor_type}.json"

    if not filepath.exists():
        versions = [
            tuple(map(int, f.name.split(".")))
            for f in NODELIST_PATH.iterdir()
            if f.is_dir() and f.name != "__pycache__"
        ]
        fallback_version = min(max(min(versions), app_version), max(versions))
        fallback_version = ".".join(map(str, fallback_version[:2]))

        filepath = NODELIST_PATH / fallback_version / f"{editor_type}.json"

        if not filepath.exists():
            raise FileNotFoundError(f"This instance of Node Tabber does not support Blender version {version_number}")
        else:
            print(f"WARNING : Node Tabber does not support editor type '{editor_type}' for Blender {version_number}'")
            print(f"WARNING : Using entries for version {fallback_version} instead.")

    with open(filepath, "r") as f:
        json_data = json.load(f)

    return json_data


def generate_entries(context, editor_type):
    entries = []
    settings_dict.clear()
    vanilla_nodelist.clear()
    vanilla_labels.clear()
    prefs = utils.fetch_user_prefs()

    json_data = get_data_from_filepath(editor_type)

    for item in itertools.chain(*filter_by_poll(context, json_data.values())):
        if isinstance(item, (tuple, list)):
            idname, properties, *_ = item
        else:
            idname, properties = item, {}

        is_deprecated = properties.get("is_deprecated", False) and bpy.app.version >= (4, 1)

        # Add check for skipping invalid entries to prevent the function from short-circuiting
        if is_entry_invalid(idname, properties) or (is_deprecated and prefs.show_deprecated == 'HIDE'):
            continue

        subtypes = properties.get("subtypes", None)
        only_subtypes = properties.get("only_subtypes", False)
        properties["is_deprecated"] = is_deprecated

        if not only_subtypes:
            entries.append(generate_entry_item(idname, **properties))

        if prefs.include_subtypes and subtypes is not None:
            enum_list, name_list = [], []
            for subtype in subtypes:
                if isinstance(subtype, dict):
                    enum_list.append(fetch_subtypes_from_bl_rna(idname, **subtype))
                    name_list.append(subtype.get("name"))
                else:
                    enum_list.append(fetch_subtypes_from_bl_rna(idname, subtype))
                    name_list.append(subtype)

            for props in itertools.product(*enum_list):
                subtype_labels = [iface_(prop.name) for prop in props]
                subtype_settings = {name: prop.identifier for (name, prop) in zip(name_list, props)}
                entries.append(
                    generate_entry_item(
                        idname, subtype_labels=subtype_labels, subtype_settings=subtype_settings, **properties
                    )
                )

    entries.extend(generate_nodegroup_entries(context))

    if prefs.include_external_nodes:
        entries.extend(generate_custom_node_entries(context))

    return entries
