
#TODO - Add functionality for supporting zone types and calling their respective functions
zones = [
    ("Simulation Zone", {"label": "Simulation Zone", "function":"add_simulation_zone"}),
    ("Repeat Zone", {"label": "Repeat Zone", "function":"add_repeat_zone"})
]

#TODO - Add functionality for settings
#Note - Structure -> (idname, {properties})
specific_types = [
    ("ShaderNodeMix", {"label": "Mix Vector", "settings":{"data_type": "VECTOR"}}),
    ("ShaderNodeMix", {"label": "Mix Color", "settings":{"data_type": "RGBA"}})
]

def is_tool(context):
    return context.space_data.geometry_nodes_type == 'TOOL'

def use_experimental_volume_nodes(context):
    return context.preferences.experimental.use_new_volume_nodes

items = [
    "GeometryNodeAttributeStatistic",
    "GeometryNodeAttributeDomainSize",
    "GeometryNodeBlurAttribute",
    "GeometryNodeCaptureAttribute",
    "GeometryNodeRemoveAttribute",
    "GeometryNodeStoreNamedAttribute",
    "ShaderNodeValToRGB",
    "ShaderNodeRGBCurve",
    "FunctionNodeCombineColor",
    "FunctionNodeSeparateColor",
    "GeometryNodeInputCurveHandlePositions",
    "GeometryNodeCurveLength",
    "GeometryNodeInputTangent",
    "GeometryNodeInputCurveTilt",
    "GeometryNodeCurveEndpointSelection",
    "GeometryNodeCurveHandleTypeSelection",
    "GeometryNodeSplineLength",
    "GeometryNodeSplineParameter",
    "GeometryNodeInputSplineResolution",
    "GeometryNodeSampleCurve",
    "GeometryNodeSetCurveNormal",
    "GeometryNodeSetCurveRadius",
    "GeometryNodeSetCurveTilt",
    "GeometryNodeSetCurveHandlePositions",
    "GeometryNodeCurveSetHandles",
    "GeometryNodeSetSplineResolution",
    "GeometryNodeCurveSplineType",
    "GeometryNodeCurveToMesh",
    "GeometryNodeCurveToPoints",
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
    "GeometryNodeInputNamedAttribute",
    "GeometryNodeInputNormal",
    "GeometryNodeInputPosition",
    "GeometryNodeInputRadius",
    "GeometryNodeSetID",
    "GeometryNodeSetPosition",
    "GeometryNodeBoundBox",
    "GeometryNodeConvexHull",
    "GeometryNodeDeleteGeometry",
    "GeometryNodeDuplicateElements",
    "GeometryNodeMergeByDistance",
    "GeometryNodeTransform",
    "GeometryNodeSeparateComponents",
    "GeometryNodeSeparateGeometry",
    "GeometryNodeProximity",
    "GeometryNodeIndexOfNearest",
    "GeometryNodeRaycast",
    "GeometryNodeSampleIndex",
    "GeometryNodeSampleNearest",
    "FunctionNodeInputBool",
    "FunctionNodeInputColor",
    "GeometryNodeInputImage",
    "FunctionNodeInputInt",
    "GeometryNodeInputMaterial",
    "FunctionNodeInputString",
    "ShaderNodeValue",
    "FunctionNodeInputVector",
    "NodeGroupInput",
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
    "GeometryNodeSampleNearestSurface",
    "GeometryNodeSampleUVSurface",
    "GeometryNodeSetShadeSmooth",
    "GeometryNodeDualMesh",
    "GeometryNodeEdgePathsToCurves",
    "GeometryNodeEdgePathsToSelection",
    "GeometryNodeExtrudeMesh",
    "GeometryNodeMeshBoolean",
    "GeometryNodeMeshToCurve",
    "GeometryNodeMeshToPoints",
    "GeometryNodeMeshToVolume",
    "GeometryNodeScaleElements",
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
    "NodeGroupOutput",
    "GeometryNodeViewer",
    "GeometryNodeDistributePointsInVolume",
    "GeometryNodeDistributePointsOnFaces",
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
    "ShaderNodeTexGradient",
    "GeometryNodeImageTexture",
    "ShaderNodeTexMagic",
    "ShaderNodeTexMusgrave",
    "ShaderNodeTexNoise",
    "ShaderNodeTexVoronoi",
    "ShaderNodeTexWave",
    "ShaderNodeTexWhiteNoise",
    "FunctionNodeRandomValue",
    "GeometryNodeSwitch",
    "GeometryNodeAccumulateField",
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
    "FunctionNodeBooleanMath",
    "FunctionNodeCompare",
    "ShaderNodeMapRange",
    "ShaderNodeMath",
    "ShaderNodeMix",
    "GeometryNodeUVPackIslands",
    "GeometryNodeUVUnwrap",
    "ShaderNodeVectorCurve",
    "ShaderNodeVectorMath",
    "ShaderNodeVectorRotate",
    "ShaderNodeCombineXYZ",
    "ShaderNodeSeparateXYZ",
    "GeometryNodeVolumeCube",
    "GeometryNodeVolumeToMesh",
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
    (items, None, None),
    (zones, None, None),
    (specific_types, None, None),
    (tool_nodes, is_tool, None),
    (experimental_volumes, use_experimental_volume_nodes, None),
]