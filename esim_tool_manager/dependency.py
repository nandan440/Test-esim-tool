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
        if info.get("type") != "executable":
            continue

        tool_name = tool.lower()
        found = check_executable(info.get("check"))

        # Missing
        if not found:
            print(f"✖ {tool_name} missing")
            system_ready = False
            continue

        # Version detection
        installed_version = None
        if "version_cmd" in info:
            installed_version = get_version(info["version_cmd"]) or None

        #  Minimum version check
        if installed_version and "min_version" in info:
            cmp = compare_versions(installed_version, info["min_version"])
            if cmp == -1:
                print(
                    f"⚠ {tool_name} version outdated "
                    f"({installed_version} < {info['min_version']})"
                )
                system_ready = False
                continue

        #  Recommended version hint (non-blocking)
        if installed_version and "recommended_version" in info:
            cmp = compare_versions(installed_version, info["recommended_version"])
            if cmp == -1:
                print(
                    f"ℹ {tool_name} update recommended "
                    f"(v{installed_version} < {info['recommended_version']})"
                )
                continue

        # ✔ All good
        if installed_version:
            print(f"✔ {tool_name} found (v{installed_version})")
        else:
            print(f"✔ {tool_name} found")

    # ---------- FINAL STATUS ----------
    print("\nStatus:", end=" ")
    if system_ready:
        print("✅ System ready")
    else:
        print("❌ System not ready")
