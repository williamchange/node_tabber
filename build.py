from pathlib import Path 
import shutil

versions = ["3.4", "3.5", "3.6", "4.0"]
root = Path(__file__).parent
RELEASE_FOLDER = Path("release")
SOURCE_FOLDER = Path("source")

IGNORE = []

def make_empty(path):
    if path.exists():
        shutil.rmtree(path)
    path.mkdir()

def copy_to_release(folder_name, version=None):
    dest_folder = RELEASE_FOLDER/folder_name
    shutil.copytree(SOURCE_FOLDER, dest_folder, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '*.pyo', *IGNORE))
    make_empty(dest_folder/"tally_cache")

    if version is not None:
        versions_to_delete = (v for v in versions if v != version)
        for v in versions_to_delete:
            shutil.rmtree(dest_folder/"nodelists"/v)

def run():
    make_empty(RELEASE_FOLDER)

    for version in versions:
        copy_to_release(folder_name=f"Node Tabber (v{version})", version=version)
    
    copy_to_release(folder_name="Node Tabber (multi_version)")
    return

if __name__ == "__main__":
    run()