from .ngspice import install_ngspice
from .kicad import install_kicad
from .nghdl import install_nghdl
from .dependency import needs_update, load_tools
import os

SUPPORTED_TOOLS = ["ngspice", "kicad", "nghdl"]

TOOLS_DIR = os.path.expanduser("~/esim-tools-bin")
os.makedirs(TOOLS_DIR, exist_ok=True)


# ---------------- UPDATE ALL ----------------

def update_all():
    tools = load_tools()
    updated_any = False

    for tool, info in tools.items():
        tool = tool.lower()

        if tool not in SUPPORTED_TOOLS:
            if needs_update(tool, info):
                print(
                    f"⚠ {tool} update recommended.\n"
                    f"👉 Please update {tool} manually."
                )
            continue

        if needs_update(tool, info):
            print(f"\n⬆ Updating {tool}...")
            install_tool(tool)
            updated_any = True

    if not updated_any:
        print("\n✔ All managed tools are already up to date")


# ---------------- INSTALL SINGLE TOOL ----------------

def install_tool(tool_name):
    tool_name = tool_name.lower()

    if tool_name not in SUPPORTED_TOOLS:
        print(f"❌ Unknown or unmanaged tool: {tool_name}")
        print("👉 Supported tools:", ", ".join(SUPPORTED_TOOLS))
        return

    print(f"🚀 Installing {tool_name}...")

    if tool_name == "ngspice":
        install_ngspice()

    elif tool_name == "kicad":
        install_kicad()

    elif tool_name == "nghdl":
        install_nghdl()

    print(f"✅ {tool_name} install complete")


# ---------------- INSTALL ALL ----------------

def install_all():
    print("🚀 Installing ALL managed tools...\n")

    for tool in SUPPORTED_TOOLS:
        install_tool(tool)

    print("\n✅ All tools installed successfully")
