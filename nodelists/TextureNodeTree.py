from ..utils import in_nodegroup

group_nodes = [
    "NodeGroupInput",
    "NodeGroupOutput",
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
    "TextureNodeMixRGB",
    "TextureNodeCurveRGB",
    "TextureNodeCombineColor",
    "TextureNodeSeparateColor",
    "TextureNodeValToRGB",
    "TextureNodeDistance",
    "TextureNodeMath",
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
    (items, None, None),
    (group_nodes, in_nodegroup, None),
]