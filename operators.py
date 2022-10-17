import bpy
import json

import time

import nodeitems_utils
import pprint
from . import nt_extras

import os
import pathlib

from bpy.types import (
    Operator,
    PropertyGroup,
)
from bpy.props import (
    BoolProperty,
    CollectionProperty,
    EnumProperty,
    IntProperty,
    StringProperty,
)

ADD_ON_PATH = pathlib.PurePath(os.path.dirname(__file__)).name


def nt_debug(msg):
    addon = bpy.context.preferences.addons[ADD_ON_PATH]
    prefs = addon.preferences

    if prefs.nt_debug:
        print(str(msg))

    return


def take_fifth(elem):
    return int(elem[2])


def write_score(category, enum_items):
    addon = bpy.context.preferences.addons[ADD_ON_PATH]
    prefs = addon.preferences

    if category == "S":
        category = "shader.json"
    if category == "C":
        category = "compositor.json"
    if category == "T":
        category = "texture.json"
    if category == "G":
        category = "geometry.json"

    path = os.path.dirname(__file__) + "/" + category
    if not os.path.exists(path):
        content = {}
        content[enum_items] = {"tally": 1}

        with open(path, "w") as f:
            json.dump(content, f)

        print("Nodetabber created :" + path)
    else:
        with open(path, "r") as f:
            content = json.load(f)

        if enum_items in content:
            if content[enum_items]["tally"] < prefs.tally_weight:
                content[enum_items]["tally"] += 1
        else:
            content[enum_items] = {"tally": 1}

        with open(path, "w") as f:
            json.dump(content, f)

    return


def sub_search(
    enum_items, node_type_index, node_type, extras_ops, index_offset, content
):
    if node_type_index > -1:
        nt_debug(f"Adding ${node_type} nodes")
        for index2, subname in enumerate(extras_ops):
            tally = 0
            if subname[1] in content:
                tally = content[subname[1]]["tally"]
            enum_items.append(
                (
                    str(node_type_index) + subname[0] + " " + subname[1],
                    subname[1],
                    str(tally),
                    index_offset + 1 + index2,
                )
            )
        index_offset += index2 + 1
    return enum_items, index_offset


class NodeTabSetting(PropertyGroup):
    value: StringProperty(
        name="Value",
        description="Python expression to be evaluated " "as the initial node setting",
        default="",
    )


class NODE_OT_add_tabber_search(bpy.types.Operator):
    """Add a node to the active tree using node tabber"""

    bl_idname = "node.add_tabber_search"
    bl_label = "Search and Add Node"
    bl_options = {"REGISTER", "UNDO"}
    bl_property = "node_item"

    _enum_item_hack = []

    # Create an enum list from node items
    def node_enum_items(self, context):
        nt_debug("DEF: node_enum_items")
        enum_items = NODE_OT_add_tabber_search._enum_item_hack

        addon = bpy.context.preferences.addons[ADD_ON_PATH]
        prefs = addon.preferences

        enum_items.clear()

        category = ""
        space = context.space_data.tree_type

        if space[0] == "S":
            category = "shader.json"
        if space[0] == "C":
            category = "compositor.json"
        if space[0] == "T":
            category = "texture.json"
        if space[0] == "G":
            category = "geometry.json"

        path = os.path.dirname(__file__) + "/" + category
        if not os.path.exists(path):
            content = {}
        else:
            with open(path, "r") as f:
                content = json.load(f)

        index_offset = 0

        item_index = {}
        for key in nt_extras.SUBNODE_ENTRIES:
            item_index[key] = -1

        for index, item in enumerate(nodeitems_utils.node_items_iter(context)):
            if isinstance(item, nodeitems_utils.NodeItem):
                short = ""
                tally = 0
                words = item.label.split()
                for word in words:
                    short += word[0]
                match = item.label + " (" + short + ")"
                if match in content:
                    tally = content[match]["tally"]

                enum_items.append(
                    (
                        str(index) + " 0 0",
                        item.label + " (" + short + ")",
                        str(tally),
                        index,
                    )
                )
                index_offset = index

                item_index[item.label] = index

        # Add sub node searching if enabled
        if prefs.sub_search:
            si = [item_index[i] for i in item_index]
            sn = [str.lower(k) for k in item_index]
            se = [nt_extras.SUBNODE_ENTRIES[e] for e in nt_extras.SUBNODE_ENTRIES]
            nt = [t for t in nt_extras.SUBNODE_ENTRIES]
            for s in zip(si, sn, se, nt):
                if space[0] == "C" and s[3] == "Map Range":
                    continue
                enum_items, index_offset = sub_search(
                    enum_items, s[0], s[1], s[2], index_offset, content
                )

        if prefs.tally:
            tmp = enum_items
            tmp = sorted(enum_items, key=take_fifth, reverse=True)
        else:
            tmp = enum_items
        return tmp
        # return enum_items

    # Look up the item based on index
    def find_node_item(self, context):
        nt_debug("DEF: find_node_item")
        tmp = int(self.node_item.split()[0])
        nt_debug("FIND_NODE_ITEM: Tmp : " + str(self.node_item.split()))

        node_item = tmp
        extra = self.node_item.split()[1:]
        nice_name = " ".join(self.node_item.split()[3:])

        for index, item in enumerate(nodeitems_utils.node_items_iter(context)):
            if index == node_item:
                return [item, extra, nice_name]
        return None

    def execute(self, context):
        nt_debug("DEF: execute")
        startTime = time.perf_counter()
        addon = bpy.context.preferences.addons[ADD_ON_PATH]
        prefs = addon.preferences

        _find_node_item = self.find_node_item(context)
        item = _find_node_item[0]
        extra = _find_node_item[1]
        nice_name = _find_node_item[2]

        # Add to tally
        short = ""
        words = item.label.split()
        nt_debug("EXECUTE: Item label : " + str(item.label))
        for word in words:
            short += word[0]
        match = item.label + " (" + short + ")"

        type = self.node_item.split()[1]
        nt_debug("Checking type : " + str(type))

        if type == "0":
            nt_debug("Writing normal node tally")
            write_score(item.nodetype[0], match)
        else:
            nt_debug("Writing sub node tally")
            write_score(item.nodetype[0], nice_name)

        nt_debug("Hack")

        # no need to keep
        self._enum_item_hack.clear()

        if item:
            node_tree_type = None
            if "node_tree" in item.settings:
                node_tree_type = eval(item.settings["node_tree"])
            try:
                for setting in item.settings.items():
                    if setting[0] != "node_tree":
                        ops = self.settings.add()
                        ops.name = setting[0]
                        ops.value = setting[1]
            except AttributeError:
                print("An exception occurred")

            self.create_node(context, item.nodetype, node_tree_type)

            nt_debug(str(item.nodetype))
            nt_debug("extra 0: " + str(extra[0]))
            nt_debug("extra 1: " + str(extra[1]))

            space = context.space_data
            node_tree = space.node_tree
            node_active = context.active_node
            node_selected = context.selected_nodes

            key = extra[0]

            # GN Compare
            if key == "CMP":
                node_active.data_type = extra[1]
                if extra[1] == "VECTOR":
                    node_active.mode = extra[2]
                    node_active.operation = extra[3]
                else:
                    node_active.operation = extra[2]

            # Math / Vector Math / Boolean Math
            if key in ["M", "VM", "BM"]:
                node_active.operation = extra[1]

            # Mix Color
            if key == "C":
                node_active.blend_type = extra[1]

            # Named Attribute / Random Value
            if key in ["NA", "RV"]:
                node_active.data_type = extra[1]

            # Attribute Statistic / Field at Index
            # Accumulate Field
            if key in ["AST", "FaI", "AF"]:
                node_active.data_type = extra[1]
                node_active.domain = extra[2].replace("SPLINE", "CURVE")

            # Store Named Attribute
            if key == "STO":
                node_active.data_type = extra[1].replace("FLOAT_COLOR", "BYTE_COLOR")
                node_active.domain = extra[2].replace("SPLINE", "CURVE")

            # Switch
            if key == "SW":
                node_active.input_type = extra[1]

            # Geometry Proximity
            if key == "GPX":
                node_active.target_element = extra[1]

            # Capture Attribute
            if key == "CAP":
                node_active.data_type = extra[1]

            # Scale Elements
            if key == "SE":
                node_active.domain = extra[1]
                node_active.scale_mode = extra[2]

            # Separate/Combine Color
            if key in ["SEP", "COM"]:
                node_active.mode = extra[1]

            if key == "SPT":
                node_active.spline_type = extra[1]

            # Raycast
            if key == "RAY":
                node_active.data_type = extra[1]
                node_active.mapping = extra[2]

            # Domain Size
            if key == "DS":
                node_active.component = extra[1]

            # Merge By Distance
            if key == "MbD":
                node_active.mode = extra[1]

            # Map Range
            if key == "MR":
                node_active.data_type = extra[1]
                node_active.interpolation_type = extra[2]

            # Mesh Boolean
            if key == "MB":
                node_active.operation = extra[1]

            # Separate Geometry
            if key == "SG":
                node_active.domain = extra[1].replace("SPLINE", "CURVE")

            # Duplicate Elements
            if key == "DE":
                node_active.domain = extra[1]

            # Filter
            if key == "F":
                node_active.filter_type = extra[1]

            # Float to Integer
            if key == "FtI":
                node_active.rounding_mode = extra[1]

            # Vector Rotate
            if key == "VR":
                node_active.rotation_type = extra[1]

            if not prefs.quick_place:
                bpy.ops.node.translate_attach_remove_on_cancel("INVOKE_DEFAULT")

            nt_debug("Time taken: " + str(time.perf_counter() - startTime))
            return {"FINISHED"}
        else:
            return {"CANCELLED"}

    def create_node(self, context, node_type=None, node_tree_type=None):
        nt_debug("DEF: create_node")
        space = context.space_data
        tree = space.edit_tree

        if node_type is None:
            node_type = self.type

        # select only the new node
        for n in tree.nodes:
            n.select = False

        node = tree.nodes.new(type=node_type)

        if node_tree_type != None:
            node.node_tree = node_tree_type

        node.select = True
        tree.nodes.active = node
        node.location = space.cursor_location
        return node

    def invoke(self, context, event):
        # self.store_mouse_cursor(context, event)
        # Delayed execution in the search popup
        context.window_manager.invoke_search_popup(self)
        return {"CANCELLED"}

    populate = node_enum_items

    node_item: EnumProperty(
        name="Node Type",
        description="Node type",
        items=populate,
    )


class NODE_OT_reset_tally(bpy.types.Operator):
    """Reset the tally count"""

    bl_idname = "node.reset_tally"
    bl_label = "Reset node tally count"

    def execute(self, context):
        categories = ["shader.json", "compositor.json", "texture.json", "geometry.json"]
        reset = False
        for cat in categories:
            path = os.path.dirname(__file__) + "/" + cat
            if os.path.exists(path):
                reset = True
                # delete file
                os.remove(path)

            if reset:
                info = "Reset Tallies"
                self.report({"INFO"}, info)
            else:
                info = "No tallies to reset."
                self.report({"INFO"}, info)

        return {"FINISHED"}


def register():
    bpy.utils.register_class(NodeTabSetting)
    bpy.utils.register_class(NODE_OT_add_tabber_search)
    bpy.utils.register_class(NODE_OT_reset_tally)


def unregister():
    bpy.utils.unregister_class(NodeTabSetting)
    bpy.utils.unregister_class(NODE_OT_add_tabber_search)
    bpy.utils.unregister_class(NODE_OT_reset_tally)
