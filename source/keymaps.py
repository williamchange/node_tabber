import bpy
from .operators import (
    NODE_OT_add_tabber_search
)

addon_keymaps = []
keymap_defs = (
    (NODE_OT_add_tabber_search.bl_idname, 'TAB', False, None),
    ("node.group_edit", 'TAB', True, None),
)

def register():
    addon_keymaps.clear()
    key_config = bpy.context.window_manager.keyconfigs.addon

    if key_config:
        key_map = key_config.keymaps.new(
            name='Node Editor', space_type="NODE_EDITOR")
        for operator, key, use_ctrl, props in keymap_defs:
            keymap_item = key_map.keymap_items.new(
                operator, key, ctrl=use_ctrl, value='PRESS')

            addon_keymaps.append((key_map, keymap_item))


def unregister():
    for key_map, key_entry in addon_keymaps:
        key_map.keymap_items.remove(key_entry)
    addon_keymaps.clear()
