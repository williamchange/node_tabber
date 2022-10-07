from nodeitems_utils import NodeItem
geonodes_node_items = [
	NodeItem("GeometryNodeAttributeStatistic"),
	NodeItem("GeometryNodeCaptureAttribute"),
	NodeItem("GeometryNodeAttributeDomainSize"),
	NodeItem("GeometryNodeRemoveAttribute"),
	NodeItem("GeometryNodeStoreNamedAttribute"),
	NodeItem("ShaderNodeValToRGB"),
	NodeItem("FunctionNodeCombineColor"),
	NodeItem("ShaderNodeMix"),
	NodeItem("ShaderNodeRGBCurve"),
	NodeItem("FunctionNodeSeparateColor"),
	NodeItem("GeometryNodeCurveLength"),
	NodeItem("GeometryNodeCurveToMesh"),
	NodeItem("GeometryNodeCurveToPoints"),
	NodeItem("GeometryNodeDeformCurvesOnSurface"),
	NodeItem("GeometryNodeFillCurve"),
	NodeItem("GeometryNodeFilletCurve"),
	NodeItem("GeometryNodeResampleCurve"),
	NodeItem("GeometryNodeReverseCurve"),
	NodeItem("GeometryNodeSampleCurve"),
	NodeItem("GeometryNodeSubdivideCurve"),
	NodeItem("GeometryNodeTrimCurve"),
	NodeItem("GeometryNodeInputCurveHandlePositions"),
	NodeItem("GeometryNodeInputTangent"),
	NodeItem("GeometryNodeInputCurveTilt"),
	NodeItem("GeometryNodeCurveEndpointSelection"),
	NodeItem("GeometryNodeCurveHandleTypeSelection"),
	NodeItem("GeometryNodeInputSplineCyclic"),
	NodeItem("GeometryNodeSplineLength"),
	NodeItem("GeometryNodeSplineParameter"),
	NodeItem("GeometryNodeInputSplineResolution"),
	NodeItem("GeometryNodeSetCurveNormal"),
	NodeItem("GeometryNodeSetCurveRadius"),
	NodeItem("GeometryNodeSetCurveTilt"),
	NodeItem("GeometryNodeSetCurveHandlePositions"),
	NodeItem("GeometryNodeCurveSetHandles"),
	NodeItem("GeometryNodeSetSplineCyclic"),
	NodeItem("GeometryNodeSetSplineResolution"),
	NodeItem("GeometryNodeCurveSplineType"),
	NodeItem("GeometryNodeCurveArc"),
	NodeItem("GeometryNodeCurvePrimitiveBezierSegment"),
	NodeItem("GeometryNodeCurvePrimitiveCircle"),
	NodeItem("GeometryNodeCurvePrimitiveLine"),
	NodeItem("GeometryNodeCurveSpiral"),
	NodeItem("GeometryNodeCurveQuadraticBezier"),
	NodeItem("GeometryNodeCurvePrimitiveQuadrilateral"),
	NodeItem("GeometryNodeCurveStar"),
	NodeItem("GeometryNodeOffsetPointInCurve"),
	NodeItem("GeometryNodeCurveOfPoint"),
	NodeItem("GeometryNodePointsOfCurve"),
	NodeItem("GeometryNodeBoundBox"),
	NodeItem("GeometryNodeConvexHull"),
	NodeItem("GeometryNodeDeleteGeometry"),
	NodeItem("GeometryNodeDuplicateElements"),
	NodeItem("GeometryNodeProximity"),
	NodeItem("GeometryNodeGeometryToInstance"),
	NodeItem("GeometryNodeJoinGeometry"),
	NodeItem("GeometryNodeMergeByDistance"),
	NodeItem("GeometryNodeRaycast"),
	NodeItem("GeometryNodeSampleIndex"),
	NodeItem("GeometryNodeSampleNearest"),
	NodeItem("GeometryNodeSeparateComponents"),
	NodeItem("GeometryNodeSeparateGeometry"),
	NodeItem("GeometryNodeTransform"),
	NodeItem("GeometryNodeSetID"),
	NodeItem("GeometryNodeSetPosition"),
	NodeItem("FunctionNodeInputBool"),
	NodeItem("GeometryNodeCollectionInfo"),
	NodeItem("FunctionNodeInputColor"),
	NodeItem("FunctionNodeInputInt"),
	NodeItem("GeometryNodeIsViewport"),
	NodeItem("GeometryNodeInputMaterial"),
	NodeItem("GeometryNodeObjectInfo"),
	NodeItem("GeometryNodeSelfObject"),
	NodeItem("FunctionNodeInputString"),
	NodeItem("ShaderNodeValue"),
	NodeItem("FunctionNodeInputVector"),
	NodeItem("GeometryNodeInputID"),
	NodeItem("GeometryNodeInputIndex"),
	NodeItem("GeometryNodeInputNamedAttribute"),
	NodeItem("GeometryNodeInputNormal"),
	NodeItem("GeometryNodeInputPosition"),
	NodeItem("GeometryNodeInputRadius"),
	NodeItem("GeometryNodeInputSceneTime"),
	NodeItem("GeometryNodeInstanceOnPoints"),
	NodeItem("GeometryNodeInstancesToPoints"),
	NodeItem("GeometryNodeRealizeInstances"),
	NodeItem("GeometryNodeRotateInstances"),
	NodeItem("GeometryNodeScaleInstances"),
	NodeItem("GeometryNodeTranslateInstances"),
	NodeItem("GeometryNodeInputInstanceRotation"),
	NodeItem("GeometryNodeInputInstanceScale"),
	NodeItem("GeometryNodeReplaceMaterial"),
	NodeItem("GeometryNodeInputMaterialIndex"),
	NodeItem("GeometryNodeMaterialSelection"),
	NodeItem("GeometryNodeSetMaterial"),
	NodeItem("GeometryNodeSetMaterialIndex"),
	NodeItem("GeometryNodeDualMesh"),
	NodeItem("GeometryNodeEdgePathsToCurves"),
	NodeItem("GeometryNodeEdgePathsToSelection"),
	NodeItem("GeometryNodeExtrudeMesh"),
	NodeItem("GeometryNodeFlipFaces"),
	NodeItem("GeometryNodeMeshBoolean"),
	NodeItem("GeometryNodeMeshToCurve"),
	NodeItem("GeometryNodeMeshToPoints"),
	NodeItem("GeometryNodeMeshToVolume"),
	NodeItem("GeometryNodeSampleNearestSurface"),
	NodeItem("GeometryNodeSampleUVSurface"),
	NodeItem("GeometryNodeScaleElements"),
	NodeItem("GeometryNodeSplitEdges"),
	NodeItem("GeometryNodeSubdivideMesh"),
	NodeItem("GeometryNodeSubdivisionSurface"),
	NodeItem("GeometryNodeTriangulate"),
	NodeItem("GeometryNodeInputMeshEdgeAngle"),
	NodeItem("GeometryNodeInputMeshEdgeNeighbors"),
	NodeItem("GeometryNodeInputMeshEdgeVertices"),
	NodeItem("GeometryNodeInputMeshFaceArea"),
	NodeItem("GeometryNodeInputMeshFaceNeighbors"),
	NodeItem("GeometryNodeMeshFaceSetBoundaries"),
	NodeItem("GeometryNodeInputMeshFaceIsPlanar"),
	NodeItem("GeometryNodeInputShadeSmooth"),
	NodeItem("GeometryNodeInputMeshIsland"),
	NodeItem("GeometryNodeInputShortestEdgePaths"),
	NodeItem("GeometryNodeInputMeshVertexNeighbors"),
	NodeItem("GeometryNodeSetShadeSmooth"),
	NodeItem("GeometryNodeMeshCone"),
	NodeItem("GeometryNodeMeshCube"),
	NodeItem("GeometryNodeMeshCylinder"),
	NodeItem("GeometryNodeMeshGrid"),
	NodeItem("GeometryNodeMeshIcoSphere"),
	NodeItem("GeometryNodeMeshCircle"),
	NodeItem("GeometryNodeMeshLine"),
	NodeItem("GeometryNodeMeshUVSphere"),
	NodeItem("GeometryNodeCornersOfFace"),
	NodeItem("GeometryNodeCornersOfVertex"),
	NodeItem("GeometryNodeEdgesOfCorner"),
	NodeItem("GeometryNodeEdgesOfVertex"),
	NodeItem("GeometryNodeFaceOfCorner"),
	NodeItem("GeometryNodeOffsetCornerInFace"),
	NodeItem("GeometryNodeVertexOfCorner"),
	NodeItem("GeometryNodeViewer"),
	NodeItem("GeometryNodeDistributePointsInVolume"),
	NodeItem("GeometryNodeDistributePointsOnFaces"),
	NodeItem("GeometryNodePoints"),
	NodeItem("GeometryNodePointsToVertices"),
	NodeItem("GeometryNodePointsToVolume"),
	NodeItem("GeometryNodeSetPointRadius"),
	NodeItem("GeometryNodeStringJoin"),
	NodeItem("FunctionNodeReplaceString"),
	NodeItem("FunctionNodeSliceString"),
	NodeItem("FunctionNodeStringLength"),
	NodeItem("GeometryNodeStringToCurves"),
	NodeItem("FunctionNodeValueToString"),
	NodeItem("FunctionNodeInputSpecialCharacters"),
	NodeItem("ShaderNodeTexBrick"),
	NodeItem("ShaderNodeTexChecker"),
	NodeItem("ShaderNodeTexGradient"),
	NodeItem("GeometryNodeImageTexture"),
	NodeItem("ShaderNodeTexMagic"),
	NodeItem("ShaderNodeTexMusgrave"),
	NodeItem("ShaderNodeTexNoise"),
	NodeItem("ShaderNodeTexVoronoi"),
	NodeItem("ShaderNodeTexWave"),
	NodeItem("ShaderNodeTexWhiteNoise"),
	NodeItem("GeometryNodeAccumulateField"),
	NodeItem("FunctionNodeAlignEulerToVector"),
	NodeItem("FunctionNodeBooleanMath"),
	NodeItem("ShaderNodeClamp"),
	NodeItem("FunctionNodeCompare"),
	NodeItem("GeometryNodeFieldAtIndex"),
	NodeItem("ShaderNodeFloatCurve"),
	NodeItem("FunctionNodeFloatToInt"),
	NodeItem("GeometryNodeFieldOnDomain"),
	NodeItem("ShaderNodeMapRange"),
	NodeItem("ShaderNodeMath"),
	NodeItem("ShaderNodeMix"),
	NodeItem("FunctionNodeRandomValue"),
	NodeItem("FunctionNodeRotateEuler"),
	NodeItem("GeometryNodeSwitch"),
	NodeItem("GeometryNodeUVPackIslands"),
	NodeItem("GeometryNodeUVUnwrap"),
	NodeItem("ShaderNodeCombineXYZ"),
	NodeItem("ShaderNodeSeparateXYZ"),
	NodeItem("ShaderNodeVectorCurve"),
	NodeItem("ShaderNodeVectorMath"),
	NodeItem("ShaderNodeVectorRotate"),
	NodeItem("GeometryNodeVolumeCube"),
	NodeItem("GeometryNodeVolumeToMesh"),
	NodeItem("NodeFrame"),
	NodeItem("NodeReroute"),
]