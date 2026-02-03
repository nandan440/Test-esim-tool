import argparse
import importlib.metadata
from esim_tool_manager import dependency
from esim_tool_manager import installer


def show_version():
    version = importlib.metadata.version("esim-tools-manager")
    print(f"esim-tools v{version}")

def show_help():
    print("""
esim-tools help

Commands:
  install <tool|all>     Install tools
  uninstall <tool>       Uninstall tool
  list                   List installed tools
  doctor                 Check system & dependencies
  version                Show tool manager version
  update <tool|all>      Update tools
""")


def main():
    parser = argparse.ArgumentParser(
        description="eSim Tool Manager"
    )

    parser.add_argument(
    "command",
    help="Command to run (install, uninstall, list, doctor, update, help)"
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
            print("❌ Specify tool: ngspice / kicad / nghdl/ all")
            return

        if args.tool == "all":
            installer.install_all()
        else:
            installer.install_tool(args.tool)

    # CHECK DEPENDENCIES
    elif args.command == "list":
        dependency.check_dependencies()

    # LIST TOOLS
    elif args.command == "help":
        show_help()

    elif args.command == "update":
            if not args.tool:
               print("❌ Specify tool: <tool> or all")
               return

            if args.tool == "all":
              installer.update_all()
            else:
             installer.update_tool(args.tool)
    
    # Run Doctor
    elif args.command == "doctor":
        dependency.run_doctor()
    # Version check 
    elif args.command == "version":
        show_version()


    else:
        print("❌ Unknown command")


if __name__ == "__main__":
    main()
