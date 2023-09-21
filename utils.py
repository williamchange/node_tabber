def fetch_active_nodetree(context):
    edit_tree = context.space_data.edit_tree
    node_tree = context.space_data.node_tree

    if edit_tree is not None:
        return edit_tree
    else:
        return node_tree


def create_node(context, node_type=None, *_, node_tree=None, **settings):
    tree = fetch_active_nodetree(context)
    node = tree.nodes.new(type=node_type)

    try:
        if settings is not None:
            for key, value in settings.items():
                setattr(node, key, value)

        if node_tree is not None:
            node.node_tree = context.blend_data.node_groups.get(node_tree)        

        node.location = context.space_data.cursor_location
        return make_selection(context, nodes=(node,))
    
    except Exception as error:
        tree.nodes.remove(node)
        raise error


def create_zone(context, *_, input_type=None, output_type=None, offset=(150, 0), **settings,):
    tree = fetch_active_nodetree(context)
    input_node = tree.nodes.new(type=input_type)
    output_node = tree.nodes.new(type=output_type)

    try:
        # Simulation input must be paired with the output.
        input_node.pair_with_output(output_node)

        for node in (input_node, output_node):
            node.location = context.space_data.cursor_location

        x_offset, y_offset = offset
        input_node.location.x -= x_offset
        input_node.location.y -= y_offset
        output_node.location.x += x_offset
        output_node.location.y += y_offset

        # Connect geometry sockets by default.
        # Get the sockets by their types, because the name is not guaranteed due to i18n.
        from_socket = next(s for s in input_node.outputs if s.type == 'GEOMETRY')
        to_socket = next(s for s in output_node.inputs if s.type == 'GEOMETRY')
        tree.links.new(to_socket, from_socket)

        return make_selection(context, nodes=(input_node, output_node))
    
    except Exception as error:
        tree.nodes.remove(input_node)
        tree.nodes.remove(output_node)
        raise error


def make_selection(context, nodes):
    tree = fetch_active_nodetree(context)
    # select only the new node
    for n in tree.nodes:
        n.select = False
    
    for n in nodes:
        n.select = True

    tree.nodes.active = nodes[-1]
    return nodes