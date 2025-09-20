import re
import shutil
import argparse
import platform

from pathlib import Path
from dataclasses import dataclass


build_folder = Path(Path.cwd(), "release")


@dataclass
class AddonBuild:
    version_string : tuple
    install_path : Path
    zip_path : Path


def get_version_string(zip_path):
    return str(re.findall(r"\d\.\d", zip_path.stem)[-1])


def userdata_folder():
    sys_platform = platform.system()

    if sys_platform in {"linux", "linux2"}:
        return "~/.config/blender/"
    elif sys_platform == "darwin":
        return "~/Library/Application Support/Blender/"
    elif sys_platform in {"win32", "Windows"}:
        return "~/AppData/Roaming/Blender Foundation/Blender/"


def version_to_string(version, depth=None, separator="."):
    if depth is not None:
        version = version[:depth]

    return separator.join(map(str, version[:depth]))


def get_addon_builds(user_folder, addon_name, use_multiversion=False):
    versions = (path for path in build_folder.glob("*.zip") if not path.stem.endswith("(multi-version)"))
    multiversion_zip = next(path for path in build_folder.glob("*.zip") if path.stem.endswith("(multi-version)"))
    for zip_path in versions:
        version_string = get_version_string(zip_path)
        addon_path = Path(
            Path(user_folder).expanduser(),
            version_string,
            f"scripts/addons/{addon_name}",
            )

        if use_multiversion:
            yield AddonBuild(version_string, addon_path, multiversion_zip)
        else:
            yield AddonBuild(version_string, addon_path, zip_path)


def is_symbolic_link(path):
    if hasattr(path, "is_junction"):
        return path.is_junction() or path.is_symlink()
    else:
        return path.is_symlink() or not path.is_dir()
    

def remove_symlink(addon_path, version):
    addon_path.unlink()
    print(f"Blender {version}: Unlinked working directory from \"{addon_path}\"")


def uninstall_addon_builds(builds):
    for build in builds:
        version_string = build.version_string
        addon_path = build.install_path

        if not addon_path.exists():
            print(f"Blender {version_string}: No installation found in \"{addon_path}\"")
            continue

        if is_symbolic_link(addon_path):
            remove_symlink(addon_path, version=version_string)
            continue
        else:
            try:
                shutil.rmtree(addon_path)
                print(f"Blender {version_string}: Uninstalled addon in \"{addon_path}\"")
                continue
            except OSError:
                remove_symlink(addon_path, version=version_string)
                continue


def install_addon_builds(builds):
    for build in builds:
        version_string = build.version_string
        install_path = build.install_path
        zip_path = build.zip_path

        shutil.unpack_archive(zip_path, install_path.parent)
        print(f"Blender {version_string}: Installed addon \"{zip_path.stem}\" in \"{install_path}\"")


def symlink_current_directory(builds):
    for build in builds:
        version_string = build.version_string
        install_path = build.install_path

        install_path.symlink_to(target=Path.cwd())
        print(f"Blender {version_string}: Linked working directory from \"{install_path}\"")


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["SYMLINK", "MULTI_VERSION", "SINGLE_VERSION"], help="Specifies whether to install addon through symlinks, multiversion zip, or individual version zips.")
    args = parser.parse_args()

    if args.mode == "SYMLINK":
        use_symlinks = True
        use_multiversion = False

    elif args.mode == "MULTI_VERSION":
        use_symlinks = False
        use_multiversion = True
    
    elif args.mode == "SINGLE_VERSION":
        use_symlinks = False
        use_multiversion = False

    return (use_symlinks, use_multiversion)


def run():
    use_symlinks, use_multiversion = parse_arguments()
    builds = tuple(get_addon_builds(userdata_folder(), addon_name="Node Tabber", use_multiversion=use_multiversion))

    print("===== UNINSTALLING ADDON BUILDS =====")
    uninstall_addon_builds(builds)
    print()

    print("===== INSTALLING ADDON BUILDS =====")
    if use_symlinks:
        symlink_current_directory(builds)
    else:
        install_addon_builds(builds)
    print()


if __name__ == "__main__":
    run()
