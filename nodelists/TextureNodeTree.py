from ..utils import in_nodegroup

group_nodes = [
    "NodeGroupInput",
    "NodeGroupOutput",
]

basic_subtypes = [
    ("TextureNodeMath", {"subtypes":("operation",)}),
    ("TextureNodeCombineColor", {"subtypes":("mode",)}),
    ("TextureNodeSeparateColor", {"subtypes":("mode",)}),
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
    (group_nodes, in_nodegroup, None),
]