import bpy
import json
import time

from .gn_items import geonodes_node_items
from . import nt_extras

import nodeitems_utils
from bpy.types import Operator, PropertyGroup
from bpy.props import EnumProperty, StringProperty
from pathlib import Path


ADDON_PATH = Path(__file__).parent
TALLY_PATH = ADDON_PATH / "tally_cache"
ADDON_NAME = ADDON_PATH.name

#Create Folder for caching node tallies
if not TALLY_PATH.exists():
    TALLY_PATH.mkdir()

def nt_debug(msg):
    prefs = bpy.context.preferences.addons[ADDON_NAME].preferences
    
    if prefs.nt_debug:
        print(str(msg))

    return


def sort_by_tally(elem):
    return int(elem[2])


def write_score(enum_items):
    tree_type = bpy.context.space_data.tree_type
    category = f'{tree_type.removesuffix("NodeTree").lower()}.json'
    prefs = bpy.context.preferences.addons[ADDON_NAME].preferences

    path = Path(TALLY_PATH, category)
    if not path.exists():
        with open(path, "w") as f:
            json.dump({enum_items: {"tally": 1}}, f)

        print(f"Nodetabber created : {path}")
    else:
        with open(path, "r") as f:
            tally_dict = json.load(f)

        old_tally = tally_dict.get(enum_items, {"tally":0})["tally"]
        new_tally = min(old_tally + 1, prefs.tally_weight)
        tally_dict[enum_items] = {"tally": new_tally}

        with open(path, "w") as f:
            json.dump(tally_dict, f)

    return


def sub_search(
    enum_items, node_type_index, node_type, extras_ops, index_offset, tally_dict
):
    # nt_debug(f'Adding ${node_type} nodes')
    for index2, subname in enumerate(extras_ops):
        sn_name, sn_label = subname
        tally = tally_dict.get(sn_label, {"tally":0})["tally"]
        enum_items.append(
            (
                f'{node_type_index} {sn_name} {sn_label}',
                sn_label,
                str(tally),
                index_offset + index2 + 1,
            )
        )
    index_offset += index2 + 1
    return index_offset


class NodeTabSetting(PropertyGroup):
    value: StringProperty(
        name="Value",
        description="Python expression to be evaluated " "as the initial node setting",
        default="",
    )


class NODE_OT_add_tabber_search(Operator):
    """Add a node to the active tree using node tabber"""

    bl_idname = "node.add_tabber_search"
    bl_label = "Search and Add Node"
    bl_options = {"REGISTER", "UNDO"}
    bl_property = "node_item"

    _enum_item_hack = []

    # Create an enum list from node items
    def node_enum_items(self, context):
        # nt_debug("DEF: node_enum_items")
        enum_items = NODE_OT_add_tabber_search._enum_item_hack

        prefs = bpy.context.preferences.addons[ADDON_NAME].preferences

        enum_items.clear()
        space = context.space_data.tree_type

        category = f'{space.removesuffix("NodeTree").lower()}.json'
        node_items = nodeitems_utils.node_items_iter(context)
        if space == "GeometryNodeTree":
            node_items = geonodes_node_items(context)

        path = Path(TALLY_PATH, category)
        if not path.exists():
            tally_dict = {}
        else:
            with open(path, "r") as f:
                tally_dict = json.load(f)

        index_offset = 0               
        item_index = {key: -1 for key in nt_extras.SUBNODE_ENTRIES}

        for index, item in enumerate(node_items):
            if isinstance(item, nodeitems_utils.NodeItem):
                abbr = "".join(word[0] for word in item.label.split())
                match = f'{item.label} ({abbr})'
                tally = tally_dict.get(match, {"tally":0})["tally"]

                enum_items.append((f'{index} 0 0', match, str(tally), index,))
                index_offset = index
                item_index[item.label] = index
        
        if space == "GeometryNodeTree":
            enum_items.append((f'{index+1} 0 0', "Simulation Zone (SZ)", str(tally), index+1,))
            index_offset = index + 1
            item_index["Simulation Zone"] = index + 1

        # Add sub node searching if enabled
        if prefs.sub_search:
            sn_entries = nt_extras.SUBNODE_ENTRIES
            if prefs.use_op_symbols:
                sn_entries["Math"] = nt_extras.math_symb
                sn_entries["Vector Math"] = nt_extras.vec_symb
                sn_entries["Boolean Math"] = nt_extras.bool_symb
            else:
                sn_entries["Math"] = nt_extras.math
                sn_entries["Vector Math"] = nt_extras.vec_math
                sn_entries["Boolean Math"] = nt_extras.bool_math            

            sn_info = zip(sn_entries.keys(), item_index.values(), item_index.keys(), sn_entries.values())

            for nodetype, index, *sn_data in sn_info:
                if space == "CompositorNodeTree" and nodetype == "Map Range":
                    continue
                if index > -1:
                    index_offset = sub_search(
                        enum_items, index, *sn_data, index_offset, tally_dict
                    )

        if prefs.tally:
            enum_items.sort(key=sort_by_tally, reverse=True)

        return enum_items

    # Look up the item based on index
    def find_node_item(self, context):
        # nt_debug("DEF: find_node_item")
        # nt_debug(f'FIND_NODE_ITEM: Tmp : {str(self.node_item.split())}')

        data = self.node_item.split()
        node_index, extra, nice_name = int(data[0]), data[1:], " ".join(data[3:])

        if context.space_data.tree_type == "GeometryNodeTree":
            node_items = geonodes_node_items(context)
        else:
            node_items = nodeitems_utils.node_items_iter(context)

        for index, item in enumerate(node_items):
            if index == node_index:
                return [item, extra, nice_name]
        return None

    def execute(self, context):
        # nt_debug("DEF: execute")
        startTime = time.perf_counter()
        prefs = bpy.context.preferences.addons[ADDON_NAME].preferences

        #Fetch node item info
        try:
            item, extra, nice_name = self.find_node_item(context)
        except TypeError:
            item = "GeometryNodeSimulationZone"

        # Add to tally
        
        if item == "GeometryNodeSimulationZone":
            # nt_debug("Writing normal node tally")
            write_score("Simulation Zone (SZ)")
        else:
            # nt_debug(f'EXECUTE: Item label : {str(item.label)}')
            subnodes_id = self.node_item.split()[1]
            # nt_debug(f'Checking type : {str(subnodes_id)}')

            if subnodes_id == "0":
                abbr = "".join(word[0] for word in item.label.split())
                match = f'{item.label} ({abbr})'

                # nt_debug("Writing normal node tally")
                write_score(match)
            else:
                # nt_debug("Writing sub node tally")
                write_score(nice_name)

            # nt_debug("Hack")

        # no need to keep
        self._enum_item_hack.clear()

        if item == "GeometryNodeSimulationZone":
            bpy.ops.node.add_simulation_zone(use_transform=True)
            if not prefs.quick_place:
                bpy.ops.node.translate_attach_remove_on_cancel("INVOKE_DEFAULT")

            # nt_debug("Time taken: " + str(time.perf_counter() - startTime))
            return {"FINISHED"}

        if item:
            node_tree_type = None
            if "node_tree" in item.settings:
                node_tree_type = eval(item.settings["node_tree"])
            self.create_node(context, item.nodetype, node_tree_type)

            # nt_debug(str(item.nodetype))
            # nt_debug(f'extra 0: {str(extra[0])}')
            # nt_debug(f'extra 1: {str(extra[1])}')

            space = context.space_data
            node_active = context.active_node

            key = extra[0]

            # GN Compare
            if key == "CMP":
                node_active.data_type = extra[1]
                if extra[1] == "VECTOR":
                    node_active.mode = extra[2]
                    node_active.operation = extra[3]
                else:
                    node_active.operation = extra[2]

            # UV Unwrap
            if key == "UU":
                node_active.method = extra[1]
            
            # Blur Attribute
            if key == "BA":
                node_active.data_type = extra[1].replace("COLOR", "FLOAT_COLOR").replace("VECTOR", "FLOAT_VECTOR")

            # Math / Vector Math / Boolean Math
            if key in ["M", "VM", "BM"]:
                node_active.operation = extra[1]

            # Mix Color
            if key == "C":
                if space.tree_type != "CompositorNodeTree":
                    node_active.data_type = "RGBA"
                node_active.blend_type = extra[1]

            # Named Attribute
            # Random Value
            # Sample Nearest Surface
            # Sample UV Surface
            if key in ["NA", "RV", "SNS", "SUS"]:
                node_active.data_type = extra[1]

            # Attribute Statistic / Sample Index 
            # Accumulate Field 
            if key in ["AST", "SIN", "AF"]:
                node_active.data_type = extra[1]
                node_active.domain = extra[2].replace("SPLINE", "CURVE")

            # Store Named Attribute
            if key == "SNA":
                node_active.data_type = extra[1].replace("FLOAT_COLOR", "BYTE_COLOR").replace("2D_VECTOR", "FLOAT2")
                node_active.domain = extra[2].replace("SPLINE", "CURVE")

            # Scale Elements
            if key == "SE":
                node_active.domain = extra[1]
                node_active.scale_mode = extra[2]

            # Switch
            if key == "SW":
                node_active.input_type = extra[1]

            # Geometry Proximity
            if key == "GPX":
                node_active.target_element = extra[1]

            # Sample Nearest / Duplicate Elements
            if key in ["SN", "DE"]:
                node_active.domain = extra[1]

            # Separate Geometry
            if key == "SG":
                node_active.domain = extra[1].replace("SPLINE", "CURVE")

            # Capture Attribute / Interpolate Domain / Field at Index
            if key in ["CAP", "INTER", "FaI"]:
                node_active.data_type = extra[1]
                node_active.domain = extra[2].replace("SPLINE", "CURVE")

            # Separate / Combine Color / Merge by Distance
            if key in ["SEP", "COM", "MbD"]:
                node_active.mode = extra[1]

            # Set Spline Type
            if key == "SPT":
                node_active.spline_type = extra[1]

            # Raycast
            if key == "RAY":
                node_active.data_type = extra[1]
                node_active.mapping = extra[2]

            # Domain Size
            if key == "DS":
                node_active.component = extra[1]

            # Vector Rotate
            if key == "VR":
                node_active.rotation_type = extra[1]

            # Map Range
            if key == "MR":
                node_active.data_type = extra[1]
                node_active.interpolation_type = extra[2]

            # Mesh Boolean
            if key == "MB":
                node_active.operation = extra[1]

            # Filter
            if key == "F":
                node_active.filter_type = extra[1]

            # Float to Integer
            if key == "FtI":
                node_active.rounding_mode = extra[1]

            # Fillet Curve
            if key == "FC":
                node_active.mode = extra[1]

            if not prefs.quick_place:
                bpy.ops.node.translate_attach_remove_on_cancel("INVOKE_DEFAULT")

            # nt_debug("Time taken: " + str(time.perf_counter() - startTime))
            return {"FINISHED"}
        else:
            return {"CANCELLED"}

    def create_node(self, context, node_type=None, node_tree_type=None):
        # nt_debug("DEF: create_node")
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

    node_item: EnumProperty(
        name="Node Type",
        description="Node type",
        items=node_enum_items,
    )


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


classes = (NodeTabSetting, NODE_OT_add_tabber_search, NODE_OT_reset_tally)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
