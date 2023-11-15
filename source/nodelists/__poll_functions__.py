from ..utils import fetch_user_prefs

## === GENERAL POLL FUNCTIONS ===
def check_mix_color_alias(_context, valid_options):
    current_pref = fetch_user_prefs("mix_color_alias")
    return current_pref in valid_options


def in_nodegroup(context):
    current_tree = context.space_data.edit_tree
    node_groups = context.blend_data.node_groups

    return current_tree in node_groups.values()


## === SHADER NODES ===
def engine_and_shader_type_poll(context, engines=None, exclude_engines=None, shader_types=None):
    current_engine = context.engine
    current_shader_type = context.space_data.shader_type

    if engines is None:
        engine_poll = True
    elif isinstance(engines, str):
        engine_poll = (current_engine == engines)
    else:
        engine_poll = current_engine in engines

    if exclude_engines is not None:
        if isinstance(exclude_engines, str):
            not_engine_poll = (current_engine != exclude_engines)
        else:
            not_engine_poll = (current_engine not in exclude_engines)
            
        engine_poll = engine_poll and not_engine_poll

    if shader_types is None:
        shader_type_poll = True
    elif isinstance(shader_types, str):
        shader_type_poll = (current_shader_type == shader_types)
    else:
        shader_type_poll = current_shader_type in shader_types

    return (engine_poll and shader_type_poll)


## === GEOMETRY NODES ===
def is_tool(context):
    return getattr(context.space_data, "geometry_nodes_type", None) == "TOOL"


def use_experimental_volume_nodes(context):
    return getattr(context.preferences.experimental, "use_new_volume_nodes", False)
