import argparse
from esim_tool_manager import dependency
from esim_tool_manager import installer


def main():
    parser = argparse.ArgumentParser(
        description="eSim Tool Manager"
    )

    parser.add_argument(
        "command",
        help="Command to run (install, list, check)"
    )

    parser.add_argument(
        "tool",
        nargs="?",
        help="Tool name (ngspice, kicad, nghdl, all)"
    )

    args = parser.parse_args()

    # INSTALL COMMAND
    if args.command == "install":
        if not args.tool:
            print("❌ Specify tool: ngspice / kicad / all")
            return

        if args.tool == "all":
            installer.install_all()
        else:
            installer.install_tool(args.tool)

    # CHECK DEPENDENCIES
    elif args.command == "check":
        dependency.check_dependencies()

    # LIST TOOLS
    elif args.command == "list":
        print("Installed tools list coming soon")

    else:
        print("❌ Unknown command")


if __name__ == "__main__":
    main()
