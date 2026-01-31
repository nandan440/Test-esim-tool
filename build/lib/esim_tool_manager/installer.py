from .ngspice import install_ngspice
from .kicad import install_kicad


SUPPORTED_TOOLS = ["ngspice", "kicad"]


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

    print(f"✅ {tool_name} install complete")


def install_all():
    print("🚀 Installing ALL tools...\n")

    for tool in SUPPORTED_TOOLS:
        install_tool(tool)

    print("\n✅ All tools installed successfully")
