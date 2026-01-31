import subprocess

def get_version(commands):
    if commands is None:
        return None

    for cmd in commands:
        try:
            result = subprocess.run(
                cmd.split(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            output = (result.stdout or result.stderr).strip()

            if output:
                return output.split("\n")[0]

        except Exception:
            continue

    return None
