import os
import sys
from pathlib import Path

from coleo import Argument, auto_cli
from pystache import Renderer
from pystache.context import KeyNotFoundError

render = Renderer(missing_tags="strict")


def transform(path, text, env):
    try:
        return render.render(text, env)
    except KeyNotFoundError as err:
        print(
            f"Key '{err.args[0]}' required for file '{path}' was not found",
            file=sys.stderr,
        )
        sys.exit(1)


class NewFile:
    def __init__(self, filename, contents, stat):
        self.filename = filename
        self.contents = contents
        self.stat = stat

    def save(self):
        if self.contents is None:
            print(f"Generating directory: {self.filename}")
            os.makedirs(self.filename)
            os.chmod(self.filename, self.stat.st_mode)
        else:
            print(f"Generating file: {self.filename}")
            open(self.filename, "w").write(self.contents)
            os.chmod(self.filename, self.stat.st_mode)


def run():
    """Copy a template file or directory."""

    # [positional]
    # Path to the file or directory to copy
    path: Argument

    # [positional]
    # The destination file or directory
    dest: Argument

    # [positional: *]
    # key=value pairs to substitute
    env: Argument

    if not all("=" in k for k in env):
        sys.exit("Error: arguments after path and dest should all be key=value pairs.")

    env_dict = dict(k.split("=") for k in env)

    full_path = Path(path).absolute()
    if not os.path.exists(full_path):
        sys.exit(f"Error: template '{full_path}' does not exist")

    dest = Path(dest)
    if dest.exists():
        sys.exit(f"Error: destination '{dest}' must not exist")

    stem = full_path.stem
    if "{{" in stem:
        if stem.startswith("{{") and stem.endswith("}}"):
            env_dict[stem[2:-2]] = dest.stem
        else:
            sys.exit(
                "Error: If the template path contains a template it must encompass the full stem"
            )

    env_dict["STEM"] = dest.stem

    base = os.path.dirname(full_path)
    if not base.endswith("/"):
        base += "/"
    base_length = len(str(full_path) + "/")

    gen = []

    data = list(os.walk(full_path, topdown=True))
    if os.path.isdir(full_path):
        first_entry = (base, [os.path.basename(full_path)], [])
    else:
        first_entry = (base, [], [os.path.basename(full_path)])
    data.insert(0, first_entry)
    for dirname, dirs, files in data:
        for d in dirs:
            full = os.path.join(dirname, d)
            relative = full[base_length:]
            new_relative = transform(full, relative, env_dict)
            fn = os.path.join(dest, new_relative)
            gen.append(
                NewFile(
                    filename=fn,
                    contents=None,
                    stat=os.stat(full),
                )
            )

        for f in files:
            full = os.path.join(dirname, f)
            relative = full[base_length:]
            new_relative = transform(relative, relative, env_dict)
            if new_relative:
                fn = os.path.join(dest, new_relative)
            else:
                fn = dest
            gen.append(
                NewFile(
                    filename=fn,
                    contents=transform(full, open(full).read(), env_dict),
                    stat=os.stat(full),
                )
            )

    for new_file in gen:
        new_file.save()


def main():
    auto_cli(run, [])
