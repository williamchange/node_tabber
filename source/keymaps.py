from .keymap_ui import KeymapItemDef, KeymapStructure, KeymapLayout
from .operators import NODE_OT_add_tabber_search


keymap_info = {
    "keymap_name" : "Node Editor",
    "space_type" : "NODE_EDITOR",
}


keymap_structure = KeymapStructure([
    KeymapItemDef(NODE_OT_add_tabber_search.bl_idname, **keymap_info, key_type='TAB'),
    KeymapItemDef("node.group_edit", **keymap_info, key_type='TAB', ctrl=True),
    ]
)


keymap_layout = KeymapLayout(layout_structure=keymap_structure)


def register():
    keymap_structure.register()


def unregister():
    keymap_structure.unregister()
