
#TODO - Add functionality for supporting iface_ and settings
specific_types = [
    ("ShaderNodeMix", {"label":'iface_("Mix Vector")', "settings":{"data_type": "VECTOR"}}),
    ("ShaderNodeMix", {"label":'iface_("Mix Color")', "settings":{"data_type": "RGBA"}})
]

items = [
    "ShaderNodeAmbientOcclusion",
    "ShaderNodeAttribute",
    "ShaderNodeBevel",
    "ShaderNodeCameraData",
    "ShaderNodeVertexColor",
    "ShaderNodeHairInfo",
    "ShaderNodeFresnel",
    "ShaderNodeNewGeometry",
    "ShaderNodeLayerWeight",
    "ShaderNodeLightPath",
    "ShaderNodeObjectInfo",
    "ShaderNodeParticleInfo",
    "ShaderNodePointInfo",
    "ShaderNodeRGB",
    "ShaderNodeTangent",
    "ShaderNodeTexCoord",
    "ShaderNodeUVMap",
    "ShaderNodeValue",
    "ShaderNodeVolumeInfo",
    "ShaderNodeWireframe",
    "ShaderNodeOutputAOV",
    "ShaderNodeVolumePrincipled",
    "ShaderNodeBrightContrast",
    "ShaderNodeGamma",
    "ShaderNodeHueSaturation",
    "ShaderNodeInvert",
    "ShaderNodeLightFalloff",
    "ShaderNodeRGBCurve",
    "ShaderNodeBlackbody",
    "ShaderNodeClamp",
    "ShaderNodeValToRGB",
    "ShaderNodeCombineColor",
    "ShaderNodeCombineXYZ",
    "ShaderNodeFloatCurve",
    "ShaderNodeMapRange",
    "ShaderNodeMath",
    "ShaderNodeMix",
    "ShaderNodeRGBToBW",
    "ShaderNodeSeparateColor",
    "ShaderNodeSeparateXYZ",
    "ShaderNodeVectorMath",
    "ShaderNodeWavelength",
    "ShaderNodeTexBrick",
    "ShaderNodeTexChecker",
    "ShaderNodeTexEnvironment",
    "ShaderNodeTexGradient",
    "ShaderNodeTexIES",
    "ShaderNodeTexImage",
    "ShaderNodeTexMagic",
    "ShaderNodeTexMusgrave",
    "ShaderNodeTexNoise",
    "ShaderNodeTexPointDensity",
    "ShaderNodeTexSky",
    "ShaderNodeTexVoronoi",
    "ShaderNodeTexWave",
    "ShaderNodeTexWhiteNoise",
    "ShaderNodeBump",
    "ShaderNodeDisplacement",
    "ShaderNodeMapping",
    "ShaderNodeNormal",
    "ShaderNodeNormalMap",
    "ShaderNodeVectorCurve",
    "ShaderNodeVectorDisplacement",
    "ShaderNodeVectorRotate",
    "ShaderNodeVectorTransform",
    "ShaderNodeScript",
]

#TODO - Add poll for -> context.space_data.shader_type == 'OBJECT' and context.engine in ('CYCLES', 'BLENDER_EEVEE'):
object_eevee_cycles_shader_nodes = [
    "ShaderNodeOutputMaterial",
    "ShaderNodeBsdfDiffuse",
    "ShaderNodeBsdfGlass",
    "ShaderNodeBsdfGlossy",
    "ShaderNodeHoldout",
    "ShaderNodeBsdfPrincipled",
    "ShaderNodeBsdfRefraction",
    "ShaderNodeSubsurfaceScattering",
    "ShaderNodeBsdfTranslucent",
    "ShaderNodeBsdfTransparent",
    ]

#TODO - Add poll for -> context.space_data.shader_type == 'OBJECT' and context.engine == 'BLENDER_EEVEE':
object_eevee_shader_nodes = [
    "ShaderNodeShaderToRGB",
    "ShaderNodeEeveeSpecular",
    ]

#TODO - Add poll for -> context.space_data.shader_type == 'OBJECT' and context.engine == 'CYCLES':
object_cycles_shader_nodes = [
    "ShaderNodeOutputLight",
    "ShaderNodeBsdfHair",
    "ShaderNodeBsdfHairPrincipled",
    "ShaderNodeBsdfSheen",
    "ShaderNodeBsdfToon",
    ]

#TODO - Add poll for -> context.space_data.shader_type == 'LINESTYLE':
line_style_shader_nodes = [
    "ShaderNodeUVAlongStroke",
    "ShaderNodeOutputLineStyle",
    ]

#TODO - Add poll for -> context.space_data.shader_type == 'WORLD':
world_shader_nodes = [
    "ShaderNodeOutputWorld",
    "ShaderNodeBackground",
    ]

#TODO - Add poll for -> context.engine in ('CYCLES', 'BLENDER_EEVEE'):
eevee_cycles_shader_nodes = [
    "ShaderNodeAddShader",
    "ShaderNodeEmission",
    "ShaderNodeMixShader",
    "ShaderNodeVolumeAbsorption",
    "ShaderNodeVolumeScatter",
    ]