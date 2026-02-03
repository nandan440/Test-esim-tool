import subprocess
import re
from packaging import version as vparse

# -----------useful functions---------
def parse_version(v):
    return tuple(map(int, v.split(".")))


def compare_versions(installed, target):
    """
    Compare installed version with target version.

    Returns:
        -1 → installed < target  (outdated)
         0 → installed == target
         1 → installed > target
        None → comparison failed
    """
    try:
        i = vparse.parse(installed)
        t = vparse.parse(target)

        if i < t:
            return -1
        elif i > t:
            return 1
        else:
            return 0
    except Exception:
        return None



def get_version(commands):
    if not commands:
        return None

    for cmd in commands:
        try:
            result = subprocess.run(
                cmd.split(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            output = (result.stdout or result.stderr)
            if not output:
                continue


            match = re.search(r"(\d+\.\d+(\.\d+)?)", output)
            if match:
                return match.group(1)

        except Exception:
            continue

    return None



 
#   -----Version Check--------


def check_tool_version(tool_cfg):
    installed = get_version(tool_cfg["version_cmd"][0])

    if not installed:
        return "not_installed"

    min_v = tool_cfg.get("min_version")
    rec_v = tool_cfg.get("recommended_version")

    if min_v and not compare_versions(installed, min_v):
        return "too_old"

    if rec_v and compare_versions(installed, rec_v):
        return "up_to_date"

    return "outdated"
