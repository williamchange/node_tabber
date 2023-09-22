from ..utils import in_nodegroup

#Note - Structure -> (idname, {properties})
specific_types = [
    ("ShaderNodeMix", {"label": "Mix Vector", "settings": {"data_type": "VECTOR"}}),
    ("ShaderNodeMix", {"label": "Mix Color", "settings": {"data_type": "RGBA"}})
]

def engine_and_shader_type_poll(context, engines=None, shader_types=None):
    current_engine = context.engine
    current_shader_type = context.space_data.shader_type

    if engines is None:
        engine_poll = True
    elif isinstance(engines, str):
        engine_poll = (current_engine == engines)
    else:
        engine_poll = current_engine in engines

    if shader_types is None:
        shader_type_poll = True
    elif isinstance(shader_types, str):
        shader_type_poll = (current_shader_type == shader_types)
    else:
        shader_type_poll = current_shader_type in shader_types

    return (engine_poll and shader_type_poll)

group_nodes = [
    "NodeGroupInput",
    "NodeGroupOutput",
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

#Note - Included when context.space_data.shader_type == 'WORLD':
world_shader_nodes = [
    "ShaderNodeOutputWorld",
    "ShaderNodeBackground",
    ]

#Note - Included when context.space_data.shader_type == 'LINESTYLE':
line_style_shader_nodes = [
    "ShaderNodeUVAlongStroke",
    "ShaderNodeOutputLineStyle",
    ]

#Note - Included when context.engine in ('CYCLES', 'BLENDER_EEVEE'):
cycles_eevee_shader_nodes = [
    "ShaderNodeAddShader",
    "ShaderNodeEmission",
    "ShaderNodeMixShader",
    "ShaderNodeVolumeAbsorption",
    "ShaderNodeVolumeScatter",
    ]

#Note - Included when context.space_data.shader_type == 'OBJECT' and context.engine == 'BLENDER_EEVEE':
object_eevee_shader_nodes = [
    "ShaderNodeShaderToRGB",
    "ShaderNodeEeveeSpecular",
    ]

#Note - Included when context.space_data.shader_type == 'OBJECT' and context.engine == 'CYCLES':
object_cycles_shader_nodes = [
    "ShaderNodeOutputLight",
    "ShaderNodeBsdfHair",
    "ShaderNodeBsdfHairPrincipled",
    "ShaderNodeBsdfSheen",
    "ShaderNodeBsdfToon",
    ]

#Note - Included when context.space_data.shader_type == 'OBJECT' and context.engine in ('CYCLES', 'BLENDER_EEVEE'):
object_cycles_eevee_shader_nodes = [
    "ShaderNodeOutputMaterial",
    "ShaderNodeBsdfDiffuse",
    "ShaderNodeBsdfGlass",
    "ShaderNodeBsdfAnisotropic",
    "ShaderNodeHoldout",
    "ShaderNodeBsdfPrincipled",
    "ShaderNodeBsdfRefraction",
    "ShaderNodeSubsurfaceScattering",
    "ShaderNodeBsdfTranslucent",
    "ShaderNodeBsdfTransparent",
    ]

all_items = [
    (items, None, None), # Note - Structure goes like -> (items, poll_function, arguments)
    (specific_types, None, None), # Note - Structure goes like -> (items, poll_function, arguments)
    (group_nodes, in_nodegroup, None),
    (world_shader_nodes, engine_and_shader_type_poll, {"shader_types": 'WORLD'}),
    (line_style_shader_nodes, engine_and_shader_type_poll, {"shader_types": 'LINESTYLE'}),
    (cycles_eevee_shader_nodes, engine_and_shader_type_poll, {"engines": ('CYCLES', 'BLENDER_EEVEE')}),
    (object_cycles_shader_nodes, engine_and_shader_type_poll, {"shader_types": "OBJECT", "engines": 'CYCLES'}),
    (object_eevee_shader_nodes, engine_and_shader_type_poll, {"shader_types": "OBJECT", "engines": 'BLENDER_EEVEE'}),
    (object_cycles_eevee_shader_nodes, engine_and_shader_type_poll, {"shader_types": "OBJECT", "engines": ('CYCLES', 'BLENDER_EEVEE')}),
]