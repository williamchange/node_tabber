from . import CompositorNodeTree, GeometryNodeTree, ShaderNodeTree, TextureNodeTree
from bpy.types import Node

def generate_label(idname):
    bl_rna = Node.bl_rna_get_subclass(idname)

    if bl_rna is not None:
        bl_label = bl_rna.name
        # Split abbreviation based on spaces and backslash
        abbr = "".join(word[0] for word in bl_label.replace("/", " ").split())
        return f"{bl_label} ({abbr})"

    else:
        return "Unknown"
        #TODO - Catch errors when node type isn't valid, right now just ignore them
        #raise ValueError(f"'{idname}' is not a valid node type.")


compositor_items = [(item, generate_label(item), "") for item in CompositorNodeTree.all_items]
shader_items = [(item, generate_label(item), "") for item in ShaderNodeTree.all_items]
geometry_items = [(item, generate_label(item), "") for item in GeometryNodeTree.all_items]
texture_items = [(item, generate_label(item), "") for item in TextureNodeTree.all_items]
