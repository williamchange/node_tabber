#Note - Structure -> (idname, {properties})
specific_types = [
    "ShaderNodeMix", #Note - Include as default entry
    ("ShaderNodeMix", {"label": "Mix Vector", "settings":{"data_type": "VECTOR"}, "subtypes":("factor_mode",) }),

    "ShaderNodeMapRange",
    ("ShaderNodeMapRange", {"label": "Map Range - Float", "settings":{"data_type": "FLOAT"}, "subtypes":("interpolation_type",)}),
    ("ShaderNodeMapRange", {"label": "Map Range - Vector", "settings":{"data_type": "FLOAT_VECTOR"}, "subtypes":("interpolation_type",)}),
 ]

mix_color = [
    ("ShaderNodeMix", {"label": "Mix Color", "settings":{"data_type": "RGBA"}, "subtypes":("blend_type",)}),
]

mix_rgb = [
    ("ShaderNodeMix", {"label": "Mix RGB", "settings":{"data_type": "RGBA"}, "subtypes":("blend_type",)}),
]

group_nodes = [
    "NodeGroupInput",
    "NodeGroupOutput",
]

frame_and_reroute = [
    "NodeFrame",
    "NodeReroute",
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
    "ShaderNodeValToRGB",
    "ShaderNodeCombineXYZ",
    "ShaderNodeFloatCurve",
    "ShaderNodeRGBToBW",
    "ShaderNodeSeparateXYZ",
    "ShaderNodeWavelength",
    "ShaderNodeTexBrick",
    "ShaderNodeTexChecker",
    "ShaderNodeTexEnvironment",
    "ShaderNodeTexImage",
    "ShaderNodeTexMagic",
    "ShaderNodeTexPointDensity",
    "ShaderNodeBump",
    "ShaderNodeNormal",
    "ShaderNodeVectorCurve",
    "ShaderNodeVectorTransform",
]

basic_subtypes = [
    ("ShaderNodeClamp", {"subtypes":("clamp_type",)}),
    ("ShaderNodeMath", {"subtypes":("operation",)}),
    ("ShaderNodeVectorMath", {"subtypes":("operation",)}),
    ("ShaderNodeVectorRotate", {"subtypes":("rotation_type",)}),
    ("ShaderNodeCombineColor", {"subtypes":("mode",)}),
    ("ShaderNodeSeparateColor", {"subtypes":("mode",)}),
    ("ShaderNodeNormalMap", {"subtypes":("space",)}),
    ("ShaderNodeDisplacement", {"subtypes":("space",)}),
    ("ShaderNodeVectorDisplacement", {"subtypes":("space",)}),
    ("ShaderNodeScript", {"subtypes":("mode",)}),
    ("ShaderNodeMapping", {"subtypes":("vector_type",)}),
]

texture_subtypes = [
    ("ShaderNodeTexSky", {"subtypes":("sky_type",)}),
    ("ShaderNodeTexIES", {"subtypes":("mode",)}),
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
    {"entries" : items},
    {"entries" : specific_types},
    {"entries" : basic_subtypes},
    {"entries" : texture_subtypes},
    {"entries" : group_nodes, "poll" : "in_nodegroup"},
    {"entries" : mix_color, "poll" : "check_mix_color_alias", "poll_args" : {"valid_options": ('DEFAULT', 'MIX_COLOR', 'BOTH')}},
    {"entries" : mix_rgb, "poll" : "check_mix_color_alias", "poll_args" : {"valid_options": ('MIX_RGB', 'BOTH')}},
    {"entries" : world_shader_nodes, "poll" : "engine_and_shader_type_poll", "poll_args" : {"shader_types": 'WORLD'}},
    {"entries" : line_style_shader_nodes, "poll" : "engine_and_shader_type_poll", "poll_args" : {"shader_types": 'LINESTYLE'}},
    {"entries" : cycles_eevee_shader_nodes, "poll" : "engine_and_shader_type_poll", "poll_args" : {"engines": ('CYCLES', 'BLENDER_EEVEE')}},
    {"entries" : object_cycles_shader_nodes, "poll" : "engine_and_shader_type_poll", "poll_args" : {"shader_types": "OBJECT", "engines": 'CYCLES'}},
    {"entries" : object_eevee_shader_nodes, "poll" : "engine_and_shader_type_poll", "poll_args" : {"shader_types": "OBJECT", "engines": 'BLENDER_EEVEE'}},
    {"entries" : object_cycles_eevee_shader_nodes, "poll" : "engine_and_shader_type_poll", "poll_args" : {"shader_types": "OBJECT", "engines": ('CYCLES', 'BLENDER_EEVEE')}},
    {"entries" : frame_and_reroute},
]