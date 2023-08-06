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

    # [positional: ?]
    # The destination's parent directory (default: .)
    dest: Argument

    # [positional: *]
    # key=value pairs to substitute
    env: Argument

    if not Path(dest).exists():
        env.insert(0, dest)
        dest = "."

    if not all("=" in k for k in env):
        sys.exit("Error: arguments after path and dest should all be key=value pairs.")

    env_dict = dict(k.split("=") for k in env)

    full_path = os.path.abspath(path)

    if not os.path.exists(full_path):
        print(f"Error: {full_path} does not exist", file=sys.stderr)
        sys.exit(1)

    base = os.path.dirname(full_path)
    if not base.endswith("/"):
        base += "/"
    base_length = len(base)

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
            fn = os.path.join(dest, new_relative)
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
