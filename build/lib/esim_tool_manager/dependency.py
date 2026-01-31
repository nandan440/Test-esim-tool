import yaml
import shutil
import os
from .version import get_version   

def load_tools():
    base_dir = os.path.dirname(__file__)
    tools_path = os.path.join(base_dir, "tools.yml")

    with open(tools_path) as f:
        return yaml.safe_load(f)

def check_executable(names):
    if isinstance(names, str):
        names = [names]
    return any(shutil.which(name) for name in names)

def check_directory(path):
    return os.path.exists(path)

def check_dependencies():
    tools = load_tools()

    for tool, info in tools.items():
        ttype = info["type"]

        # EXECUTABLE TOOLS
        if ttype == "executable":
            found = check_executable(info["check"])

            if found:
                version = None

                # Call get_version if version_cmd exists
                if "version_cmd" in info and info["version_cmd"]:
                    version = get_version(info["version_cmd"])

                if version:
                    print(f"{tool}: FOUND ({version})")
                else:
                    print(f"{tool}: FOUND")

            else:
                print(f"{tool}: MISSING")

        # DIRECTORY TOOLS
        elif ttype == "directory":
            found = check_directory(info["path"])
            print(f"{tool}: {'FOUND' if found else 'MISSING'}")

        # EXTERNAL TOOLS
        elif ttype == "external":
            print(f"{tool}: EXTERNAL (skip)")
