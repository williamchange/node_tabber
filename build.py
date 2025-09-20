import ast
import shutil
from pathlib import Path
from tempfile import TemporaryDirectory

versions = [p.name for p in Path("source", "nodelists").glob("[0-9].[0-9]")]
root = Path(__file__).parent

RELEASE_FOLDER = Path("release")
SOURCE_FOLDER = Path("source")


def get_bl_info(init_path):
    with open(init_path, 'r') as f:
        node = ast.parse(f.read())

    n: ast.Module
    for n in ast.walk(node):
        for b in n.body:
            if isinstance(b, ast.Assign) and isinstance(b.value, ast.Dict) and (
                    any(t.id == 'bl_info' for t in b.targets)):
                bl_info_dict = ast.literal_eval(b.value)
                return bl_info_dict
            
    raise ValueError('Cannot find bl_info')


BL_INFO_BASE = get_bl_info(Path("__init__.py"))
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
    bl_info["name"] = bl_info["name"].removesuffix(" (Development)") 

    if version is not None:
        bl_info["name"] = bl_info["name"] + f" (v{version})"
        bl_info["blender"] = tuple(map(int, version.split(".") + ["0"]))

    replace_text(init_path, BL_INFO_PATTERN, generate_bl_info_text(bl_info))


def build_package(archive_name, version=None):
    with TemporaryDirectory(dir=RELEASE_FOLDER) as temp_dir:
        dest_folder = Path(temp_dir, "Node Tabber")
        shutil.copytree(SOURCE_FOLDER, dest_folder, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"))
        make_empty(dest_folder / "tally_cache")

        if version is not None:
            versions_to_delete = (v for v in versions if v != version)
            for v in versions_to_delete:
                shutil.rmtree(dest_folder / "nodelists" / v)

        init_path = dest_folder / "__init__.py"
        write_bl_info(init_path, version)

        for f in dest_folder.glob("*.py"):
            replace_text(f, pattern="from ..debug import profile_code\n", replacement="")

        replace_text(
            dest_folder / "prefs.py", pattern='bl_idname = "Node Tabber"', replacement="bl_idname = __package__"
        )
        replace_text(
            dest_folder / "utils.py",
            pattern='prefs = context.preferences.addons["Node Tabber"].preferences',
            replacement="prefs = context.preferences.addons[__package__].preferences",
        )

        shutil.make_archive(RELEASE_FOLDER / archive_name, "zip", temp_dir)
        print(f"Successfully created archive at '{archive_name}'")


def run():
    initialize(RELEASE_FOLDER)

    version = BL_INFO_BASE['version']
    addon_version = f"{version[0]}.{version[1]}.{version[2]}"

    for version in versions:
        build_package(archive_name=f"Node-Tabber_v{addon_version}_(Blender-v{version})", version=version)

    build_package(archive_name=f"Node-Tabber_v{addon_version}_(multi-version)")
    return


if __name__ == "__main__":
    run()
