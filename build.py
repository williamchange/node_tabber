import shutil
from pathlib import Path 
from tempfile import TemporaryDirectory

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


def initialize(path):
    if not path.exists():
        path.mkdir()
        return 

    for item in path.iterdir():
        if item.is_dir():
            shutil.rmtree(item)
        elif not str(item).endswith(".gitignore"):
            item.unlink()


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


def replace_text(path, pattern, replacement):
    with open(path, "r") as f:
        text = f.read()
    
    text = text.replace(pattern, replacement)

    with open(path, "w") as f:
        f.write(text)


def write_bl_info(init_path, version):
    bl_info = BL_INFO_BASE.copy()
    if version is not None:
        bl_info["name"] = bl_info["name"] + f" (v{version})"
        bl_info["blender"] = tuple(map(int, version.split(".") + ["0"]))

    replace_text(init_path, BL_INFO_PATTERN, generate_bl_info_text(bl_info))


def build_package(archive_name, version=None):
    with TemporaryDirectory(dir=RELEASE_FOLDER) as temp_dir:
        dest_folder = Path(temp_dir, "Node Tabber")
        shutil.copytree(SOURCE_FOLDER, dest_folder, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '*.pyo'))
        make_empty(dest_folder/"tally_cache")

        if version is not None:
            versions_to_delete = (v for v in versions if v != version)
            for v in versions_to_delete:
                shutil.rmtree(dest_folder/"nodelists"/v)

        init_path = dest_folder/"__init__.py"
        write_bl_info(init_path, version)

        replace_text(dest_folder/"prefs.py", 
            pattern='bl_idname = "Node Tabber"', replacement='bl_idname = __package__')
        replace_text(dest_folder/"utils.py", 
            pattern='prefs = context.preferences.addons["Node Tabber"].preferences', 
            replacement='prefs = context.preferences.addons[__package__].preferences')

        shutil.make_archive(RELEASE_FOLDER/archive_name, 'zip', temp_dir)
    

def run():
    initialize(RELEASE_FOLDER)

    for version in versions:
        build_package(archive_name=f"Node Tabber (v{version})", version=version)
    
    build_package(archive_name="Node Tabber")
    return


if __name__ == "__main__":
    run()