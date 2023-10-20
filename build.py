import shutil
from pathlib import Path 

versions = ["3.4", "3.5", "3.6", "4.0"]
root = Path(__file__).parent

RELEASE_FOLDER = Path("release")
SOURCE_FOLDER = Path("source")

# NOTE - This isn't synced with the bl_info in the __init__.py used in the dev version
# Be sure to update both when updating one of them
BL_INFO_BASE = {   
    "name": "Node Tabber",
    "author": "Richard Lyons, williamchange, Quackers",
    "version": (0, 1, 4),
    "blender": (3, 4, 0),
    "description": "Allows quick smart searching of node types.",
    "category": "Node",
}
BL_INFO_PATTERN = "### INSERT BL_INFO BLOCK HERE ###"


def make_empty(path):
    if path.exists():
        shutil.rmtree(path)
    path.mkdir()


def generate_bl_info_text(bl_info):
    lines = ["bl_info = {"]

    for key, value in bl_info.items():
        if isinstance(key, str):
            key = f'"{key}"'
        if isinstance(value, str):
            value = f'"{value}"'

        lines.append(f"    {key} : {value},")

    lines.append("}")
    return "\n".join(lines)


def write_bl_info(init_path, version):
    bl_info = BL_INFO_BASE.copy()
    if version is not None:
        bl_info["name"] = bl_info["name"] + f" (v{version})"
        bl_info["blender"] = tuple(map(int, version.split(".") + ["0"]))

    with open(init_path, "r") as f:
        init_code = f.read()
    
    init_code = init_code.replace(BL_INFO_PATTERN, generate_bl_info_text(bl_info))

    with open(init_path, "w") as f:
        f.write(init_code)


def copy_to_release(folder_name, version=None):
    IGNORE = []
    dest_folder = RELEASE_FOLDER/folder_name
    shutil.copytree(SOURCE_FOLDER, dest_folder, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '*.pyo'))
    make_empty(dest_folder/"tally_cache")

    if version is not None:
        versions_to_delete = (v for v in versions if v != version)
        for v in versions_to_delete:
            shutil.rmtree(dest_folder/"nodelists"/v)

    init_path = dest_folder/"__init__.py"
    write_bl_info(init_path, version)
    

def run():
    make_empty(RELEASE_FOLDER)

    for version in versions:
        copy_to_release(folder_name=f"Node Tabber (v{version})", version=version)
    
    copy_to_release(folder_name="Node Tabber (multi_version)")
    return


if __name__ == "__main__":
    run()