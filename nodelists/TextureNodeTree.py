from ..utils import check_mix_color_alias, in_nodegroup

group_nodes = [
    "NodeGroupInput",
    "NodeGroupOutput",
]

frame_and_reroute = [
    "NodeFrame",
    "NodeReroute",
]

basic_subtypes = [
    ("TextureNodeMath", {"subtypes":("operation",)}),
    ("TextureNodeCombineColor", {"subtypes":("mode",)}),
    ("TextureNodeSeparateColor", {"subtypes":("mode",)}),
]

mix_color = [
    ("TextureNodeMixRGB", {"label":"Mix Color", "subtypes":("blend_type",)}),
]

mix_rgb = [
    ("TextureNodeMixRGB", {"subtypes":("blend_type",)}),
]

items = [
    "TextureNodeCoordinates",
    "TextureNodeCurveTime",
    "TextureNodeImage",
    "TextureNodeTexture",
    "TextureNodeOutput",
    "TextureNodeViewer",
    "TextureNodeHueSaturation",
    "TextureNodeInvert",
    "TextureNodeCurveRGB",
    "TextureNodeValToRGB",
    "TextureNodeDistance",
    "TextureNodeRGBToBW",
    "TextureNodeValToNor",
    "TextureNodeAt",
    "TextureNodeRotate",
    "TextureNodeScale",
    "TextureNodeTranslate",
    "TextureNodeBricks",
    "TextureNodeChecker",
    "TextureNodeTexBlend",
    "TextureNodeTexClouds",
    "TextureNodeTexDistNoise",
    "TextureNodeTexMagic",
    "TextureNodeTexMarble",
    "TextureNodeTexMusgrave",
    "TextureNodeTexNoise",
    "TextureNodeTexStucci",
    "TextureNodeTexVoronoi",
    "TextureNodeTexWood",
]

all_items = [
    items,
    basic_subtypes,
    (mix_color, check_mix_color_alias, {"valid_options": ('MIX_COLOR', 'BOTH')}),
    (mix_rgb, check_mix_color_alias, {"valid_options": ('DEFAULT', 'MIX_RGB', 'BOTH')}),
    (group_nodes, in_nodegroup, None),
    frame_and_reroute,
]