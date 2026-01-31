import os
import subprocess
import shutil
import yaml
import platform
from .version import get_version 

TOOLS_DIR = os.path.expanduser("~/esim-tools-bin")
os.makedirs(TOOLS_DIR, exist_ok=True)

TOOLS_FILE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "tools.yml")
)

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

def run(cmd):
    print(">>", cmd)
    subprocess.run(cmd, shell=True, check=True)


def load_tools():
    with open(TOOLS_FILE) as f:
        return yaml.safe_load(f)


def tool_exists(name):
    return shutil.which(name) is not None


def check_requirements(reqs):
    missing = [tool for tool in reqs if not tool_exists(tool)]
    if missing:
        print("Missing required tools:", ", ".join(missing))
        print("Install them first and retry.")
        return False
    return True


def install_full_kicad(urls):
    os_type = get_os()
    print(f"Installing FULL KiCad for {os_type}...")

    # WINDOWS
    if os_type == "windows":
        url = urls["windows"]
        installer_path = os.path.join(TOOLS_DIR, "kicad-full.exe")

        run(f'curl -L "{url}" -o "{installer_path}"')
        run(f'"{installer_path}"')

    # LINUX
    elif os_type == "linux":
        print("Installing via apt...")
        run("sudo apt update")
        run("sudo apt install -y kicad")

    # MAC
    elif os_type == "mac":
        print("Installing via Homebrew...")
        run("brew install --cask kicad")

    else:
        print("❌ Unsupported OS for KiCad full install")


# ---------------- COMPRESSED ESIM KICAD ----------------

def install_esim_kicad(repo_url, branch):
    os_type = get_os()

    if os_type != "windows":
        print("❌ Compressed eSim KiCad is supported ONLY on Windows (NSIS builds .exe)")
        return

    work_dir = os.path.join(TOOLS_DIR, "kicad")
    nsis_dir = os.path.join(work_dir, "NSIS")

    if os.path.exists(work_dir):
        shutil.rmtree(work_dir)

    print("Cloning KiCad eSim repo...")
    run(f'git clone -b {branch} {repo_url} "{work_dir}"')

    # Cleanup
    print("Removing unnecessary files...")
    shutil.rmtree(os.path.join(work_dir, ".git"), ignore_errors=True)

    readme = os.path.join(work_dir, "README.md")
    if os.path.exists(readme):
        os.remove(readme)

    # Compress bin/lib/share
    archive_path = os.path.join(work_dir, "KiCad.7z")
    print("Compressing KiCad binaries...")
    run(f'7z a "{archive_path}" "{work_dir}/bin" "{work_dir}/lib" "{work_dir}/share"')

    # Build installer
    print("Building NSIS installer...")
    run(f'cd "{nsis_dir}" && makensis install.nsi')

    print("✅ Compressed eSim KiCad installer built successfully!")


# ---------------- MAIN ----------------

def install_kicad():
    tools = load_tools()
    kicad = tools["kicad"]
    modes = kicad["install_modes"]

    # ✅ CHECK IF ALREADY INSTALLED
    if tool_exists("kicad"):
        print("\n✅ KiCad is already installed")

        version_cmds = kicad.get("version_cmd")
        version = get_version(version_cmds)

        if version:
            print("📦 Version:", version)

        print("Skipping installation...")
        return

    # NOT INSTALLED → Ask user
    print("\nChoose KiCad install mode:")
    print("1) Full official KiCad (Cross-platform)")
    print("2) Compressed KiCad for eSim (Windows only)")

    choice = input("Enter choice [1/2]: ").strip()

    # FULL MODE
    if choice == "1":
        urls = modes["full"]["url"]
        install_full_kicad(urls)

    # ESIM COMPRESSED MODE
    elif choice == "2":
        reqs = modes["esim_compressed"]["requires"]
        if not check_requirements(reqs):
            return

        repo = modes["esim_compressed"]["repo_url"]
        branch = modes["esim_compressed"]["branch"]

        install_esim_kicad(repo, branch)

    else:
        print("❌ Invalid choice")


if __name__ == "__main__":
    install_kicad()