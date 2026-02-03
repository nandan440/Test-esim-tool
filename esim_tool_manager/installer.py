from .ngspice import install_ngspice
from .kicad import install_kicad
from .nghdl import install_nghdl
from .dependency import needs_update, load_tools
import os

SUPPORTED_TOOLS = ["ngspice", "kicad", "nghdl"]

TOOLS_DIR = os.path.expanduser("~/esim-tools-bin")
os.makedirs(TOOLS_DIR, exist_ok=True)


def update_all():
    tools = load_tools()
    updated_any = False

    for tool, info in tools.items():
        if needs_update(tool, info):
            print(f"\n⬆ Updating {tool}...")
            install_tool(tool)
            updated_any = True

    if not updated_any:
        print("\n✔ All tools are already up to date")


def install_tool(tool_name):
    tool_name = tool_name.lower()

    if tool_name not in SUPPORTED_TOOLS:
        print(f"❌ Unknown tool: {tool_name}")
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


def install_all():
    print("🚀 Installing ALL tools...\n")

    for tool in SUPPORTED_TOOLS:
        install_tool(tool)

    print("\n✅ All tools installed successfully")
