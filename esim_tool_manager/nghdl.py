import os
import shutil
import subprocess
import platform
from esim_tool_manager import ngspice


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


def command_exists(cmd):
    return shutil.which(cmd) is not None


# ---------------- ESIM / NGHDL CHECK ----------------

def esim_installed():
    """
    NGHDL comes bundled with eSim.
    If eSim exists, NGHDL exists.
    """

    # Check executable
    if command_exists("esim"):
        return True

    # Common install locations
    possible_paths = [
        "/opt/esim",
        "/usr/local/esim",
        "C:\\eSim",
        "C:\\Program Files\\eSim",
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return True

    return False


# ---------------- DEPENDENCY CHECK ----------------

DEPENDENCIES = ["ghdl", "ngspice", "verilator"]


def check_dependencies():
    missing = []
    for dep in DEPENDENCIES:
        if not command_exists(dep):
            missing.append(dep)
    return missing


# ---------------- INSTALL DEPENDENCIES ----------------

def install_dependencies(deps):
    os_type = get_os()

    print(f"\nInstalling dependencies on {os_type}...\n")

    # -------- WINDOWS --------
    if os_type == "windows":
        for dep in deps:
            if dep == "ghdl":
                print("⚠️ GHDL must be installed manually on Windows")
                print("👉 https://github.com/ghdl/ghdl/releases")
            elif dep == "ngspice":
                print("Installing ngspice....")
                ngspice.install_ngspice()
            elif dep == "verilator":
                print("⚠️ Verilator on Windows requires WSL")
                print("👉 https://www.veripool.org/verilator/")

    # -------- LINUX --------
    elif os_type == "linux":
        run("sudo apt update")
        run(f"sudo apt install -y {' '.join(deps)}")

    # -------- MAC --------
    elif os_type == "mac":
        run(f"brew install {' '.join(deps)}")

    else:
        print("Unsupported OS")


# ---------------- MAIN NGHDL INSTALL LOGIC ----------------

def install_nghdl():
    print("\n🔍 Checking for eSim / NGHDL...\n")

    if not esim_installed():
        print("❌ NGHDL not found (eSim is not installed)")
        print("👉 Please install eSim first: https://esim.fossee.in/")
        return

    print("✅ NGHDL found (eSim is installed)")

    missing = check_dependencies()

    if not missing:
        print("\n✅ All NGHDL dependencies are already installed")
        return

    print("\n❌ Missing NGHDL dependencies:")
    for dep in missing:
        print(f" - {dep}")

    choice = input("\nInstall missing dependencies now? (y/n): ").strip().lower()

    if choice == "y":
        install_dependencies(missing)
        print("\n✅ Dependency installation process completed")
    else:
        print("\n⚠️ Dependencies not installed. NGHDL may not work properly.")


