from ..utils import check_mix_color_alias, in_nodegroup

group_nodes = [
    "NodeGroupInput",
    "NodeGroupOutput",
]

frame_and_reroute = [
    "NodeFrame",
    "NodeReroute",
]

#Note - Structure -> (idname, {properties})
specific_types = [
    ("CompositorNodeSwitchView", {"label": "Switch Stereo View"})
]

basic_subtypes = [
    ("CompositorNodePremulKey", {"subtypes":("mapping",)}),
    ("CompositorNodeSetAlpha", {"subtypes":("mode",)}),
    ("CompositorNodeDefocus", {"subtypes":("bokeh",)}),
    ("CompositorNodeDenoise", {"subtypes":("prefilter",)}),
    ("CompositorNodeDilateErode", {"subtypes":("mode",)}),
    ("CompositorNodeGlare", {"subtypes":("glare_type",)}),
    ("CompositorNodeRotate", {"subtypes":("filter_type",)}),
    ("CompositorNodeScale", {"subtypes":("space",)}),
    ("CompositorNodeTransform", {"subtypes":("filter_type",)}),
    ("CompositorNodeTranslate", {"subtypes":("wrap_axis",)}),
    ("CompositorNodeFlip", {"subtypes":("axis",)}),
    ("CompositorNodeBlur", {"subtypes":("filter_type",)}),
    ("CompositorNodeKuwahara", {"subtypes":("variation",)}),
    ("CompositorNodeLevels", {"subtypes":("channel",)}),
    ("CompositorNodeMath", {"subtypes":("operation",)}),
    ("CompositorNodeCombineColor", {"subtypes":("mode",)}),
    ("CompositorNodeSeparateColor", {"subtypes":("mode",)}),
    ("CompositorNodeFilter", {"subtypes":("filter_type",)}),
]

mix_color = [
    ("CompositorNodeMixRGB", {"label": "Mix Color", "subtypes":("blend_type",)}),
]

mix_rgb = [
    ("CompositorNodeMixRGB", {"label": "Mix RGB", "subtypes":("blend_type",)}),
]

items = [
    "CompositorNodeBokehImage",
    "CompositorNodeImage",
    "CompositorNodeMask",
    "CompositorNodeMovieClip",
    "CompositorNodeTexture",
    "CompositorNodeRGB",
    "CompositorNodeValue",
    "CompositorNodeRLayers",
    "CompositorNodeSceneTime",
    "CompositorNodeTime",
    "CompositorNodeComposite",
    "CompositorNodeSplitViewer",
    "CompositorNodeViewer",
    "CompositorNodeOutputFile",
    "CompositorNodeValToRGB",
    "CompositorNodeConvertColorSpace",
    "CompositorNodeInvert",
    "CompositorNodeRGBToBW",
    "CompositorNodeBrightContrast",
    "CompositorNodeColorBalance",
    "CompositorNodeColorCorrection",
    "CompositorNodeExposure",
    "CompositorNodeGamma",
    "CompositorNodeHueCorrect",
    "CompositorNodeHueSat",
    "CompositorNodeCurveRGB",
    "CompositorNodeTonemap",
    "CompositorNodeAlphaOver",
    "CompositorNodeZcombine",
    "CompositorNodeAntiAliasing",
    "CompositorNodeDespeckle",
    "CompositorNodeInpaint",
    "CompositorNodePixelate",
    "CompositorNodePosterize",
    "CompositorNodeSunBeams",
    "CompositorNodeBilateralblur",
    "CompositorNodeBokehBlur",
    "CompositorNodeDBlur",
    "CompositorNodeVecBlur",
    "CompositorNodeChannelMatte",
    "CompositorNodeChromaMatte",
    "CompositorNodeColorMatte",
    "CompositorNodeColorSpill",
    "CompositorNodeDiffMatte",
    "CompositorNodeDistanceMatte",
    "CompositorNodeKeying",
    "CompositorNodeKeyingScreen",
    "CompositorNodeLumaMatte",
    "CompositorNodeCryptomatteV2",
    "CompositorNodeCryptomatte",
    "CompositorNodeBoxMask",
    "CompositorNodeEllipseMask",
    "CompositorNodeDoubleEdgeMask",
    "CompositorNodeIDMask",
    "CompositorNodePlaneTrackDeform",
    "CompositorNodeStabilize",
    "CompositorNodeTrackPos",
    "CompositorNodeCornerPin",
    "CompositorNodeCrop",
    "CompositorNodeDisplace",
    "CompositorNodeMapUV",
    "CompositorNodeLensdist",
    "CompositorNodeMovieDistortion",
    "CompositorNodeMapRange",
    "CompositorNodeMapValue",
    "CompositorNodeNormalize",
    "CompositorNodeSwitch",
    "CompositorNodeCombineXYZ",
    "CompositorNodeSeparateXYZ",
    "CompositorNodeNormal",
    "CompositorNodeCurveVec",
]

all_items = [
    items,
    specific_types,
    basic_subtypes,
    (mix_color, check_mix_color_alias, {"valid_options": ('DEFAULT', 'MIX_COLOR', 'BOTH')}),
    (mix_rgb, check_mix_color_alias, {"valid_options": ('MIX_RGB', 'BOTH')}),
    (group_nodes, in_nodegroup, None),
    frame_and_reroute,
]