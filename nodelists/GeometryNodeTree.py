
zones = [
    ("Simulation Zone", {"label": "Simulation Zone", "function":"create_zone", "settings":{"input_type": "GeometryNodeSimulationInput", "output_type": "GeometryNodeSimulationOutput"}}),
    ("Repeat Zone", {"label": "Repeat Zone", "function":"create_zone", "settings":{"input_type": "GeometryNodeRepeatInput", "output_type": "GeometryNodeRepeatOutput"}})
]

#Note - Structure -> (idname, {properties})
specific_types = [
    "ShaderNodeMix", #Note - Include as default entry
    ("ShaderNodeMix", {"label": "Mix Vector", "settings":{"data_type": "VECTOR"}, "subtypes":("factor_mode",) }),
    ("ShaderNodeMix", {"label": "Mix Color", "settings":{"data_type": "RGBA"}, "subtypes":("blend_type",)}),
    ("ShaderNodeMix", {"label": "Mix Rotation", "settings":{"data_type": "ROTATION"}}),

    "GeometryNodeRaycast", #Note - Include as default entry
    ("GeometryNodeRaycast", {"label": "Raycast Nearest", "settings":{"mapping": "NEAREST"}, "subtypes":({"name":"data_type", "only_include":("Float", "Integer", "Vector", "Color", "Boolean", "Quaternion")},)}),
    ("GeometryNodeRaycast", {"label": "Raycast Interpolated", "settings":{"mapping": "INTERPOLATED"}, "subtypes":({"name":"data_type", "only_include":("Float", "Integer", "Vector", "Color", "Boolean", "Quaternion")},)}),

    "ShaderNodeMapRange",
    ("ShaderNodeMapRange", {"label": "Map Range - Float", "settings":{"data_type": "FLOAT"}, "subtypes":("interpolation_type",)}),
    ("ShaderNodeMapRange", {"label": "Map Range - Vector", "settings":{"data_type": "FLOAT_VECTOR"}, "subtypes":("interpolation_type",)}),
 
    #Note - 'data_type' subtypes are explicitly defined in order to have different abbreviations for each
    #Note - Another reason is that it offers a "Compare Vector (CV)" default option. -for example, for when you don't want to define other paraameters like operation/mode
    ("FunctionNodeCompare", {"label": "Compare", "settings":{"data_type": "FLOAT"}, "subtypes":({"name":"operation", "only_include":("Less Than", "Less Than or Equal", "Greater Than", "Greater Than or Equal", "Equal", "Not Equal")},)}),
    ("FunctionNodeCompare", {"label": "Compare Integer", "settings":{"data_type": "INT"}, "subtypes":({"name":"operation", "only_include":("Less Than", "Less Than or Equal", "Greater Than", "Greater Than or Equal", "Equal", "Not Equal")},)}),
    ("FunctionNodeCompare", {"label": "Compare Vector", "settings":{"data_type": "VECTOR"}, "subtypes":({"name":"operation", "only_include":("Less Than", "Less Than or Equal", "Greater Than", "Greater Than or Equal", "Equal", "Not Equal")}, "mode",)}),
    ("FunctionNodeCompare", {"label": "Compare String", "settings":{"data_type": "STRING"}, "subtypes":({"name":"operation", "only_include":("Equal", "Not Equal")},)}),
    ("FunctionNodeCompare", {"label": "Compare Color", "settings":{"data_type": "RGBA"}, "subtypes":({"name":"operation", "only_include":("Equal", "Not Equal", "Brighter", "Darker")},)}),    
]

def is_tool(context):
    return context.space_data.geometry_nodes_type == 'TOOL'

def use_experimental_volume_nodes(context):
    return context.preferences.experimental.use_new_volume_nodes

group_nodes = [
    "NodeGroupInput",
    "NodeGroupOutput",
]

items = [
    "GeometryNodeRemoveAttribute",
    "ShaderNodeValToRGB",
    "ShaderNodeRGBCurve",
    "GeometryNodeInputCurveHandlePositions",
    "GeometryNodeCurveLength",
    "GeometryNodeInputTangent",
    "GeometryNodeInputCurveTilt",
    "GeometryNodeCurveEndpointSelection",
    "GeometryNodeSplineLength",
    "GeometryNodeSplineParameter",
    "GeometryNodeInputSplineResolution",
    "GeometryNodeSampleCurve",
    "GeometryNodeSetCurveNormal",
    "GeometryNodeSetCurveRadius",
    "GeometryNodeSetCurveTilt",
    "GeometryNodeSetCurveHandlePositions",
    "GeometryNodeSetSplineResolution",
    "GeometryNodeCurveToMesh",
    "GeometryNodeCurveToPoints",        
    "GeometryNodeDeformCurvesOnSurface",
    "GeometryNodeFillCurve",
    "GeometryNodeInterpolateCurves",
    "GeometryNodeResampleCurve",
    "GeometryNodeReverseCurve",
    "GeometryNodeSubdivideCurve",
    "GeometryNodeTrimCurve",
    "GeometryNodeCurveArc",
    "GeometryNodeCurvePrimitiveBezierSegment",
    "GeometryNodeCurvePrimitiveLine",
    "GeometryNodeCurveSpiral",
    "GeometryNodeCurveQuadraticBezier",
    "GeometryNodeCurvePrimitiveQuadrilateral",
    "GeometryNodeCurveStar",
    "GeometryNodeCurveOfPoint",
    "GeometryNodeOffsetPointInCurve",
    "GeometryNodePointsOfCurve",
    "GeometryNodeGeometryToInstance",
    "GeometryNodeJoinGeometry",
    "GeometryNodeInputID",
    "GeometryNodeInputIndex",
    "GeometryNodeInputNormal",
    "GeometryNodeInputPosition",
    "GeometryNodeInputRadius",
    "GeometryNodeSetID",
    "GeometryNodeSetPosition",
    "GeometryNodeBoundBox",
    "GeometryNodeConvexHull",
    "GeometryNodeDeleteGeometry",
    "GeometryNodeTransform",
    "GeometryNodeSeparateComponents",
    "GeometryNodeIndexOfNearest",
    "FunctionNodeInputBool",
    "FunctionNodeInputColor",
    "GeometryNodeInputImage",
    "FunctionNodeInputInt",
    "GeometryNodeInputMaterial",
    "FunctionNodeInputString",
    "ShaderNodeValue",
    "FunctionNodeInputVector",
    "GeometryNodeCollectionInfo",
    "GeometryNodeImageInfo",
    "GeometryNodeIsViewport",
    "GeometryNodeObjectInfo",
    "GeometryNodeInputSceneTime",
    "GeometryNodeSelfObject",
    "GeometryNodeInstanceOnPoints",
    "GeometryNodeInstancesToPoints",
    "GeometryNodeRealizeInstances",
    "GeometryNodeRotateInstances",
    "GeometryNodeScaleInstances",
    "GeometryNodeTranslateInstances",
    "GeometryNodeInputInstanceRotation",
    "GeometryNodeInputInstanceScale",
    "GeometryNodeReplaceMaterial",
    "GeometryNodeInputMaterialIndex",
    "GeometryNodeMaterialSelection",
    "GeometryNodeSetMaterial",
    "GeometryNodeSetMaterialIndex",
    "GeometryNodeInputMeshEdgeAngle",
    "GeometryNodeInputMeshEdgeNeighbors",
    "GeometryNodeInputMeshEdgeVertices",
    "GeometryNodeEdgesToFaceGroups",
    "GeometryNodeInputMeshFaceArea",
    "GeometryNodeMeshFaceSetBoundaries",
    "GeometryNodeInputMeshFaceNeighbors",
    "GeometryNodeInputMeshFaceIsPlanar",
    "GeometryNodeInputShadeSmooth",
    "GeometryNodeInputEdgeSmooth",
    "GeometryNodeInputMeshIsland",
    "GeometryNodeInputShortestEdgePaths",
    "GeometryNodeInputMeshVertexNeighbors",
    "GeometryNodeSetShadeSmooth",
    "GeometryNodeDualMesh",
    "GeometryNodeEdgePathsToCurves",
    "GeometryNodeEdgePathsToSelection",
    "GeometryNodeExtrudeMesh",
    "GeometryNodeMeshToCurve",
    "GeometryNodeMeshToPoints",
    "GeometryNodeMeshToVolume",
    "GeometryNodeSplitEdges",
    "GeometryNodeSubdivideMesh",
    "GeometryNodeSubdivisionSurface",
    "GeometryNodeTriangulate",
    "GeometryNodeMeshCone",
    "GeometryNodeMeshCube",
    "GeometryNodeMeshCylinder",
    "GeometryNodeMeshGrid",
    "GeometryNodeMeshIcoSphere",
    "GeometryNodeMeshLine",
    "GeometryNodeMeshUVSphere",
    "GeometryNodeCornersOfEdge",
    "GeometryNodeCornersOfFace",
    "GeometryNodeCornersOfVertex",
    "GeometryNodeEdgesOfCorner",
    "GeometryNodeEdgesOfVertex",
    "GeometryNodeOffsetCornerInFace",
    "GeometryNodeVertexOfCorner",
    "GeometryNodeViewer",
    "GeometryNodePoints",
    "GeometryNodePointsToCurves",
    "GeometryNodePointsToVertices",
    "GeometryNodePointsToVolume",
    "GeometryNodeSetPointRadius",
    "GeometryNodeStringJoin",
    "FunctionNodeReplaceString",
    "FunctionNodeSliceString",
    "FunctionNodeStringLength",
    "GeometryNodeStringToCurves",
    "FunctionNodeValueToString",
    "FunctionNodeInputSpecialCharacters",
    "ShaderNodeTexBrick",
    "ShaderNodeTexChecker",
    "GeometryNodeImageTexture",
    "ShaderNodeTexMagic",
    "FunctionNodeAlignEulerToVector",
    "FunctionNodeAxisAngleToRotation",
    "FunctionNodeEulerToRotation",
    "FunctionNodeInvertRotation",
    "FunctionNodeRotateEuler",
    "FunctionNodeRotateVector",
    "FunctionNodeRotationToAxisAngle",
    "FunctionNodeRotationToEuler",
    "FunctionNodeRotationToQuaternion",
    "FunctionNodeQuaternionToRotation",
    "ShaderNodeFloatCurve",
    "GeometryNodeUVPackIslands",
    "ShaderNodeVectorCurve",
    "ShaderNodeCombineXYZ",
    "ShaderNodeSeparateXYZ",
    "GeometryNodeVolumeCube",
    "GeometryNodeVolumeToMesh",
]

basic_subtypes = [
    ("ShaderNodeClamp", {"subtypes":("clamp_type",)}),
    ("GeometryNodeSwitch", {"subtypes":("input_type",)}),
    ("GeometryNodeFilletCurve", {"subtypes":("mode",)}),
    ("GeometryNodeUVUnwrap", {"subtypes":("method",)}),
    ("ShaderNodeMath", {"subtypes":("operation",)}),
    ("ShaderNodeVectorMath", {"subtypes":("operation",)}),
    ("FunctionNodeBooleanMath", {"subtypes":("operation",)}),
    ("GeometryNodeAttributeDomainSize", {"subtypes":("component",)}),
    ("GeometryNodeProximity", {"subtypes":("target_element",)}),
    ("GeometryNodeSampleNearest", {"subtypes":("domain",)}),
    ("GeometryNodeCurveSplineType", {"subtypes":("spline_type",)}),
    ("GeometryNodeCurveSetHandles", {"subtypes":("handle_type",)}),
    ("GeometryNodeCurveHandleTypeSelection", {"subtypes":("handle_type",)}),
    ("GeometryNodeMeshBoolean", {"subtypes":("operation",)}),
    ("FunctionNodeCombineColor", {"subtypes":("mode",)}),
    ("FunctionNodeSeparateColor", {"subtypes":("mode",)}),
    ("GeometryNodeMergeByDistance", {"subtypes":("mode",)}),
    ("GeometryNodeSeparateGeometry", {"subtypes":("domain",)}),
    ("GeometryNodeDuplicateElements", {"subtypes":("domain",)}),
    ("FunctionNodeFloatToInt", {"subtypes":("rounding_mode",)}),
    ("ShaderNodeVectorRotate", {"subtypes":("rotation_type",)}),
    ("GeometryNodeDistributePointsInVolume", {"subtypes":("mode",)}),
    ("GeometryNodeDistributePointsOnFaces", {"subtypes":("distribute_method",)}),
    ("GeometryNodeScaleElements", {"subtypes":("domain", "scale_mode")}),
]

texture_subtypes = [
    ("ShaderNodeTexGradient", {"subtypes":("gradient_type",)}),
    ("ShaderNodeTexMusgrave", {"subtypes":("musgrave_type", "musgrave_dimensions",)}),

    "ShaderNodeTexVoronoi",
    ("ShaderNodeTexVoronoi", {"only_subtypes":True, "subtypes":({"name":"voronoi_dimensions", "only_include":("1D",)},)}),
    ("ShaderNodeTexVoronoi", {"only_subtypes":True, "subtypes":("distance", {"name":"voronoi_dimensions", "only_include":("2D", "3D", "4D")},)}),

    ("ShaderNodeTexNoise", {"subtypes":("noise_dimensions",)}),
    ("ShaderNodeTexWhiteNoise", {"subtypes":("noise_dimensions",)}),

    "ShaderNodeTexWave",
    ("ShaderNodeTexWave", {"only_subtypes":True, "subtypes":({"name":"bands_direction", "only_include":("X", "Y", "Z", "Diagonal")}, "wave_profile", {"name":"wave_type", "only_include":("Bands")},)}),    
    ("ShaderNodeTexWave", {"only_subtypes":True, "subtypes":({"name":"rings_direction", "only_include":("X", "Y", "Z", "Spherical")}, "wave_profile", {"name":"wave_type", "only_include":("Rings")},)}),    
]

filtered_subtypes = [
    ("FunctionNodeRandomValue", {"subtypes":({"name":"data_type", "only_include":("Float", "Integer", "Vector", "Boolean")},)}),
    ("GeometryNodeBlurAttribute", {"subtypes":({"name":"data_type", "only_include":("Float", "Integer", "Vector", "Color")},)}),
    ("GeometryNodeSampleNearestSurface", {"subtypes":({"name":"data_type", "only_include":("Float", "Integer", "Vector", "Color", "Boolean", "Quaternion")},)}),
    ("GeometryNodeSampleUVSurface", {"subtypes":({"name":"data_type", "only_include":("Float", "Integer", "Vector", "Color", "Boolean", "Quaternion")},)}),
    ("GeometryNodeInputNamedAttribute", {"subtypes":({"name":"data_type", "only_include":("Float", "Integer", "Vector", "Color", "Boolean", "Quaternion")},)}),
]

data_type_domain_nodes = [
    ("GeometryNodeAttributeStatistic", {"subtypes":({"name":"data_type", "only_include":("Float", "Vector")}, "domain")}),
    ("GeometryNodeAccumulateField", {"subtypes":({"name":"data_type", "only_include":("Float", "Integer", "Vector")}, "domain")}),
    ("GeometryNodeSampleIndex", {"subtypes":({"name":"data_type", "only_include":("Float", "Integer", "Vector", "Color", "Boolean", "Quaternion")}, "domain")}),
    ("GeometryNodeFieldAtIndex", {"subtypes":({"name":"data_type", "only_include":("Float", "Integer", "Vector", "Color", "Boolean", "Quaternion")}, "domain")}),
    ("GeometryNodeFieldOnDomain", {"subtypes":({"name":"data_type", "only_include":("Float", "Integer", "Vector", "Color", "Boolean", "Quaternion")}, "domain")}),
    ("GeometryNodeCaptureAttribute", {"subtypes":({"name":"data_type", "only_include":("Float", "Integer", "Vector", "Color", "Boolean", "Quaternion")}, "domain")}),
    ("GeometryNodeStoreNamedAttribute", {"subtypes":({"name":"data_type", "only_include":("Float", "Integer", "Vector", "Color", "Byte Color", "Boolean", "2D Vector", "Quaternion")}, "domain")}),
]

#Note - Included when context.preferences.experimental.use_new_volume_nodes is True:
experimental_volumes = [
    "GeometryNodeMeanFilterSDFVolume",
    "GeometryNodeOffsetSDFVolume",
    "GeometryNodeSampleVolume",
    "GeometryNodeSDFVolumeSphere",
    "GeometryNodeInputSignedDistance",
    "GeometryNodePointsToSDFVolume",
    "GeometryNodeMeshToSDFVolume",
]

#Note - Included when context.space_data.geometry_nodes_type == 'TOOL':
tool_nodes = [
    "GeometryNodeToolFaceSet",
    "GeometryNodeToolSetFaceSet",
    "GeometryNodeTool3DCursor",
    "GeometryNodeToolSetSelection",
    "GeometryNodeToolSelection",
]


all_items = [
    items,
    zones,
    group_nodes,
    basic_subtypes,
    texture_subtypes,
    filtered_subtypes,
    data_type_domain_nodes,
    specific_types,
    (tool_nodes, is_tool, None),
    (experimental_volumes, use_experimental_volume_nodes, None),
]