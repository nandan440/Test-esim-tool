import os
import platform
import subprocess
import urllib.request
import tarfile
import yaml
import shutil
import sys
from .version import get_version 

TOOLS_DIR = os.path.expanduser("~/esim-tools-bin")
os.makedirs(TOOLS_DIR, exist_ok=True)

TOOLS_FILE = os.path.join(os.path.dirname(__file__), "tools.yml")



# ---------------- OS DETECTION ----------------

def get_os():
    sys = platform.system().lower()
    if "windows" in sys:
        return "windows"
    elif "linux" in sys:
        return "linux"
    elif "darwin" in sys:
        return "mac"
    return None


# ---------------- HELPERS ----------------

def load_tools():
    with open(TOOLS_FILE) as f:
        return yaml.safe_load(f)
    

def run(cmd):
    print("Running:", cmd)
    subprocess.run(cmd, shell=True, check=True)


def download(url, output):
    print(f"Downloading: {url}")
    urllib.request.urlretrieve(url, output)

def tool_exists(name):
    return shutil.which(name) is not None

# ---------------- NGSPICE INSTALL ----------------

def install_ngspice():
    tools = load_tools()
    ngspice_cfg = tools["ngspice"]
    os_type = get_os()

    # Check if already installed
    if tool_exists("ngspice"):
        print("\n✅ Ngspice is already installed")

        version_cmd = ngspice_cfg.get("version_cmd")
        if version_cmd:
            version = get_version(version_cmd)
            if version:
                print("📦 Version:", version)

        print("Skipping install...")
        return

    print("\n⚠️ Ngspice not found — installing...")

    # WINDOWS INSTALL
    if os_type == "windows":
        url = ngspice_cfg["install"]["windows"]["url"]

        archive = os.path.join(TOOLS_DIR, "ngspice.7z")
        out_folder = os.path.join(TOOLS_DIR, "ngspice")

        download(url, archive)
        os.makedirs(out_folder, exist_ok=True)

        run(f'7z x "{archive}" -o"{out_folder}"')

        print("\n✅ Ngspice installed at:", out_folder)
        print("👉 Add this to PATH:", out_folder)

    # LINUX INSTALL
    elif os_type == "linux":
        url = ngspice_cfg["install"]["linux"]["url"]

        archive = os.path.join(TOOLS_DIR, "ngspice.tar.gz")

        download(url, archive)

        with tarfile.open(archive) as tar:
            tar.extractall(TOOLS_DIR)

        src_dir = os.path.join(TOOLS_DIR, "ngspice-45.2")

        run(f"cd {src_dir} && ./configure")
        run(f"cd {src_dir} && make")
        run(f"cd {src_dir} && sudo make install")

        print("\n✅ Ngspice installed system-wide")

    # MAC INSTALL
    elif os_type == "mac":
        run("brew install ngspice")

    else:
        print("❌ Unsupported OS")

