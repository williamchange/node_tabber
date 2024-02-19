import bpy
import itertools
from dataclasses import dataclass
from typing import Dict, Iterator, Tuple

from bpy.types import AddonPreferences
from bpy.props import BoolProperty
from rna_keymap_ui import _indented_layout, draw_km


def ui_property_name(name: str) -> str:
    return f'show_keymaps_{name.strip().lower().replace(" ", "_")}'
        

@dataclass(frozen=True, slots=True)
class KeymapItemDef:
    bl_idname: str
    keymap_name: str
    space_type: str

    key_type: str = 'NONE'
    input_mode: str = 'PRESS'

    ctrl: bool = False
    shift: bool = False
    alt: bool = False
    oskey: bool = False
    any_modifier: bool = False
    custom_modifier: str = 'NONE'
    
    direction: str = 'ANY'
    repeat: bool = False
    head: bool = False
    props: dict = None

    @property
    def keymap_props(self) -> Dict[str, str|bool]:
        return {
            "idname" : self.bl_idname,
            "type" : self.key_type,
            "value" : self.input_mode,
            "ctrl" : self.ctrl, 
            "shift" : self.shift, 
            "alt" : self.alt, 
            "oskey" : self.oskey,
            "any" : self.any_modifier,
            "key_modifier" : self.custom_modifier,
            "direction" : self.direction,
            "repeat" : self.repeat,
            "head" : self.head
        }


class KeymapStructure():
    def __init__(self, structure:Dict[str, KeymapItemDef]) -> None:
        """
        A helper class for describing the intended structure of a collection of KeymapItemDefs

        Args:
            structure : Specifies which keymap items will be grouped together when drawn by a KeymapLayout object
        """

        self.registered_keymaps = []
        try:
            self.structure = dict(structure)
            self.display_mode = 'NESTED'

        except TypeError:
            self.structure = {"Unsorted": structure}
            self.display_mode = 'FLAT'

    @property
    def ui_properties(self):
        if self.display_mode == 'NESTED':
            return tuple(map(ui_property_name, self.structure.keys()))
        else:
            return []

    def draw_items(self):
        return itertools.zip_longest(self.structure.keys(), self.structure.values(), self.ui_properties)

    @property
    def keymap_items(self) -> Iterator[KeymapItemDef]:
        for v in self.structure.values():
            for kmi_def in v:
                yield kmi_def

    @property
    def keymap_list(self) -> Iterator[Tuple[str, str]]:
        for kmi_def in self.keymap_items:
            yield (kmi_def.keymap_name, kmi_def.bl_idname, kmi_def.props)

    @staticmethod
    def fetch_keymap_data(kmi) -> Tuple[str, str]:
        return (kmi.keymap_name, kmi.space_type)

    @property
    def keymap_defs(self):
        kmi_defs = sorted((kmi for kmi in self.keymap_items), key=self.fetch_keymap_data)
        return itertools.groupby(kmi_defs, key=self.fetch_keymap_data)

    def register(self):
        self.registered_keymaps.clear()

        if key_config := bpy.context.window_manager.keyconfigs.addon:
            for (km_name, km_space), kmi_defs in self.keymap_defs:
                keymap = key_config.keymaps.new(name=km_name, space_type=km_space)
                for definition in kmi_defs:
                    keymap_item = keymap.keymap_items.new(**definition.keymap_props)

                    if (props := definition.props) is not None:
                        for prop, value in props.items():
                            setattr(keymap_item.properties, prop, value)

                    self.registered_keymaps.append((keymap, keymap_item))

    def unregister(self):
        for keymap, keymap_item in self.registered_keymaps:
            keymap.keymap_items.remove(keymap_item)
        self.registered_keymaps.clear()


class KeymapLayout():
    def __init__(self, layout_structure: KeymapStructure, custom_label_mappings: Dict[str, Tuple[str, Dict]] = None) -> None:
        """
        A helper class for drawing keymaps in an addon's User Preferences

        Args:
            layout_structure : Specifies which operators will be grouped with each other during display
            include_keymaps : Specifies the names of keymaps that will be searched to retrieve keymap items
            property_label_mappings (optional): Specifies dynamic labels for operators based on their property values 
        """
        
        self.structure = layout_structure

        if custom_label_mappings is None:
            custom_label_mappings = {}
        self.custom_label_mappings = custom_label_mappings

    def register_properties(self, preferences: AddonPreferences) -> None:
        """
        Adds properties related to the keymap UI to the specified AddonPreferences class. \\
        This must be invoked before the AddonPreferences class is registered.
        """

        pref_properties = preferences.__annotations__

        pref_properties["show_keymaps"] = BoolProperty(
            name="Show Keymaps",
            default=False,
            description="When enabled, displays keymap list",
            )

        for prop_name in self.structure.ui_properties:
            pref_properties[prop_name] = BoolProperty(
                name="Show/Hide Items",
                default=True
                )

    @property
    def ui_properties(self) -> Iterator[str]:
        """
        Yields all the names of properties used for drawing the keymap layout 
        """

        yield "show_keymaps"

        for prop_name in self.structure.ui_properties:
            yield prop_name


    def draw_keyboard_shorcuts(self, pref_data, layout, context, *, keymap_spacing=0.15, group_spacing = 0.35, indent_level=0):
        col = layout.box().column()
        kc = context.window_manager.keyconfigs.user
        display_mode = self.structure.display_mode

        if not collapsible_row(col, pref_data, "show_keymaps", text="Keymap List:", icon="KEYINGSET"):
            return

        if display_mode == 'NESTED':
            for km_group, kmi_defs, ui_prop in self.structure.draw_items():
                get_kmi_l = tuple(find_matching_keymaps(keyconfig=kc, keymap_item_defs=kmi_defs))
                category_header = _indented_layout(col, indent_level)
            
                if collapsible_row(category_header, pref_data, ui_prop, text=km_group, show_dots=True):
                    for km, kmi in get_kmi_l:
                        col.context_pointer_set("keymap", km)
                        self.draw_kmi([], kc, km, kmi, col, level=indent_level + 1)
                        col.separator(factor=keymap_spacing)

                    col.separator(factor=group_spacing)

        elif display_mode == 'FLAT':
            for km_group, kmi_defs, ui_prop in self.structure.draw_items():
                get_kmi_l = tuple(find_matching_keymaps(keyconfig=kc, keymap_item_defs=kmi_defs))

                for km, kmi in get_kmi_l:
                    col.context_pointer_set("keymap", km)
                    self.draw_kmi([], kc, km, kmi, col, level=indent_level)
                    col.separator(factor=keymap_spacing)

        else:
            raise ValueError(f"'{display_mode}' is not a valid display type.")


    def keymap_label(self, keymap_item):
        item = self.custom_label_mappings.get(keymap_item.idname, "")

        if isinstance(item, tuple):
            prop_name, mapping = item
            prop_value = getattr(keymap_item.properties, prop_name)

            return mapping[prop_value]
        else:
            return keymap_item.name


    def draw_keymap_item_header(self, layout, keymap, kmi):
        split = layout.split()

        row = split.row(align=True)
        row.prop(kmi, "show_expanded", text="", emboss=False)
        row.prop(kmi, "active", text="", emboss=False)

        if keymap.is_modal:
            row.separator()
            row.prop(kmi, "propvalue", text="")
        else:
            row.label(text=self.keymap_label(kmi))

        row = split.row()
        row.prop(kmi, "map_type", text="")

        map_type = kmi.map_type
        if map_type in {"KEYBOARD", "MOUSE", "NDOF"}:
            row.prop(kmi, "type", text="", full_event=True)
        elif map_type == "TWEAK":
            subrow = row.row()
            subrow.prop(kmi, "type", text="")
            subrow.prop(kmi, "value", text="")
        elif map_type == "TIMER":
            row.prop(kmi, "type", text="")
        else:
            row.label()

        if (not kmi.is_user_defined) and kmi.is_user_modified:
            row.operator("preferences.keyitem_restore", text="", icon="BACK").item_id = kmi.id
        else:
            remove_icon = "TRACKING_CLEAR_BACKWARDS" if kmi.is_user_defined else "X"
            row.operator("preferences.keyitem_remove", text="", icon=remove_icon).item_id = kmi.id


    def draw_kmi(self, display_keymaps, kc, km, kmi, layout, level):
        col = _indented_layout(layout, level)

        if not kmi.show_expanded:
            self.draw_keymap_item_header(col, km, kmi)
        else:
            col = col.column(align=True)
            self.draw_keymap_item_header(col.box(), km, kmi)

            box = col.box()
            split = box.split(factor=0.4)
            sub = split.row()

            if km.is_modal:
                sub.prop(kmi, "propvalue", text="")
            else:
                # One day...
                # sub.prop_search(kmi, "idname", bpy.context.window_manager, "operators_all", text="")
                sub.prop(kmi, "idname", text="")

            map_type = kmi.map_type
            if map_type not in {"TEXTINPUT", "TIMER"}:
                sub = split.column()
                subrow = sub.row(align=True)

                if map_type == "KEYBOARD":
                    subrow.prop(kmi, "type", text="", event=True)
                    subrow.prop(kmi, "value", text="")
                    subrow_repeat = subrow.row(align=True)
                    subrow_repeat.active = kmi.value in {"ANY", "PRESS"}
                    subrow_repeat.prop(kmi, "repeat", text="Repeat")
                elif map_type in {"MOUSE", "NDOF"}:
                    subrow.prop(kmi, "type", text="")
                    subrow.prop(kmi, "value", text="")

                if map_type in {"KEYBOARD", "MOUSE"} and kmi.value == "CLICK_DRAG":
                    subrow = sub.row()
                    subrow.prop(kmi, "direction")

                subrow = sub.row()
                subrow.scale_x = 0.75

                for prop_name in ("any", "shift_ui", "ctrl_ui", "alt_ui"):
                    subrow.prop(kmi, prop_name, toggle=True)
                subrow.prop(kmi, "oskey_ui", text="Cmd", toggle=True)
                subrow.prop(kmi, "key_modifier", text="", event=True)

            # Operator properties
            box.template_keymap_item_properties(kmi)

            # Modal key maps attached to this operator
            if not km.is_modal:
                kmm = kc.keymaps.find_modal(kmi.idname)
                if kmm:
                    draw_km(display_keymaps, kc, kmm, None, layout, level + 1)
                    layout.context_pointer_set("keymap", km)


def find_matching_keymaps(keyconfig, keymap_item_defs):
    for kmi_def in keymap_item_defs:
        keymap_name = kmi_def.keymap_name
        kmi_idname = kmi_def.bl_idname

        for km_con in keyconfig.keymaps:
            if keymap_name != km_con.name:
                continue

            # Newer defined keymaps appear first in .keymap_items
            # To make the display order match the order of definition, 
            # keymap_items must be reversed.
            for kmi_con in reversed(km_con.keymap_items):
                if kmi_idname == kmi_con.idname:
                    properties = kmi_def.props
                    
                    if properties is None:
                        yield (km_con, kmi_con)
                    else:
                        properties_match = all(v == getattr(kmi_con.properties, k) for k,v in properties.items())
                    
                        if properties_match:
                            yield (km_con, kmi_con)


if bpy.app.version >= (4, 1):
    OPEN_ICON = "DOWNARROW_HLT"
    CLOSE_ICON = "RIGHTARROW"
else:
    OPEN_ICON = "DISCLOSURE_TRI_DOWN"
    CLOSE_ICON = "DISCLOSURE_TRI_RIGHT"


def collapsible_row(layout, data, property_name, text, icon='NONE', *, show_dots=False) -> bool:
    row = layout.row(align=True)
    toggle_state = getattr(data, property_name)

    if toggle_state:
        row.prop(data, property_name, text="", icon=OPEN_ICON, emboss=False)
    else:
        row.prop(data, property_name, text="", icon=CLOSE_ICON, emboss=False)       
    
    row.label(text=text, icon=icon)
    if show_dots and not toggle_state:
        row.prop(data, property_name, text="", icon="THREE_DOTS", emboss=False)

    return toggle_state
