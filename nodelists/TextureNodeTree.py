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
    {"entries" : items},
    {"entries" : basic_subtypes},
    {"entries" : mix_color, "poll" : "check_mix_color_alias", "poll_args" : {"valid_options": ('MIX_COLOR', 'BOTH')}},
    {"entries" : mix_rgb, "poll" : "check_mix_color_alias", "poll_args" : {"valid_options": ('DEFAULT', 'MIX_RGB', 'BOTH')}},
    {"entries" : group_nodes, "poll" : "in_nodegroup"},
    {"entries" : frame_and_reroute},
]