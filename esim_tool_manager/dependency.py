import yaml
import shutil
import os
from .version import get_version, compare_versions


# ---------- LOAD TOOLS ----------
def load_tools():
    base_dir = os.path.dirname(__file__)
    tools_path = os.path.join(base_dir, "tools.yml")

    with open(tools_path) as f:
        return yaml.safe_load(f)


# ---------- CHECK HELPERS ----------
def check_executable(names):
    if isinstance(names, str):
        names = [names]
    return any(shutil.which(name) for name in names)


def check_directory(path):
    return os.path.exists(path)


# ---------- TABLE VIEW (list / check) ----------
def check_dependencies():
    tools = load_tools()
    results = []

    for tool, info in tools.items():
        ttype = info.get("type")
        status = "not installed"
        version = "-"

        if ttype == "executable":
            found = check_executable(info.get("check"))

            if found:
                status = "installed"
                if "version_cmd" in info:
                    version = get_version(info["version_cmd"]) or "-"

        elif ttype == "directory":
            found = check_directory(info.get("path"))
            if found:
                status = "installed"

        results.append((tool.lower(), status, version))

    print_dependency_table(results)


def print_dependency_table(results):
    print(f"{'Tool':<12} {'Status':<14} Version")
    print("-" * 38)

    for tool, status, version in results:
        print(f"{tool:<12} {status:<14} {version}")


# ---------- DOCTOR COMMAND ----------
def run_doctor():
    print("🔍 System Diagnostics\n")

    tools = load_tools()
    system_ready = True

    for tool, info in tools.items():
        tool_name = tool.lower()

        if info.get("type") != "executable":
            continue

        # 🔑 Bundled / no-version tools → skip version checks
        if (
            "min_version" not in info
            and "recommended_version" not in info
        ):
            print(f"✔ {tool_name} (bundled / managed by eSim)")
            continue

        found = check_executable(info.get("check"))

        if not found:
            print(f"✖ {tool_name} missing")
            system_ready = False
            continue

        installed_version = None
        if "version_cmd" in info:
            installed_version = get_version(info["version_cmd"])

        if installed_version and "min_version" in info:
            cmp = compare_versions(installed_version, info["min_version"])
            if cmp == -1:
                print(
                    f"⚠ {tool_name} version outdated "
                    f"({installed_version} < {info['min_version']})"
                )
                system_ready = False
                continue

        if installed_version and "recommended_version" in info:
            cmp = compare_versions(installed_version, info["recommended_version"])
            if cmp == -1:
                print(
                    f"ℹ {tool_name} update recommended "
                    f"(v{installed_version} < {info['recommended_version']})"
                )
                continue

        if installed_version:
            print(f"✔ {tool_name} found (v{installed_version})")
        else:
            print(f"✔ {tool_name} found")

    print("\nStatus:", end=" ")
    if system_ready:
        print("✅ System ready")
    else:
        print("❌ System not ready")


#-----------------Update---------------
def needs_update(tool_name, info):
    """
    Returns True only if:
    - tool is executable
    - tool is installed
    - AND version rules are defined
    - AND installed version is outdated
    """

    # Only executables can be updated
    if info.get("type") != "executable":
        return False

    # 🔑 KEY RULE: no version rules → no update
    if "min_version" not in info and "recommended_version" not in info:
        return False

    # Tool must be installed
    if not check_executable(info.get("check")):
        return False

    # Detect version
    installed_version = None
    if "version_cmd" in info:
        installed_version = get_version(info["version_cmd"])

    if not installed_version:
        return False

    # Recommended version has priority
    if "recommended_version" in info:
        return compare_versions(
            installed_version, info["recommended_version"]
        ) == -1

    if "min_version" in info:
        return compare_versions(
            installed_version, info["min_version"]
        ) == -1

    return False

