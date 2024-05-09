__version__ = "0.1.1"

import argparse
import pathlib

# NOTE: limitation; ``make ..\some.css`` - cannot walk upwards while createing file


class ParserArguments(argparse.Namespace):
    filepath: pathlib.Path
    create_recursive: bool

parser = argparse.ArgumentParser(
    prog="make"
)
parser.add_argument("filepath", type=pathlib.Path, help="Filepath to create")
parser.add_argument("-r", action="store_true", help="Recursively create the folder and file")

args = ParserArguments()
parser.parse_args(namespace=args)

origin = pathlib.Path.cwd()
target_path = (
    origin
    .joinpath(args.filepath)
    .resolve()
)
if not args.filepath.exists():
    relative = (
        target_path
        .resolve()
        .relative_to(origin)
    )
    *directories, fname = relative.parts
    walked = pathlib.Path()
    for directory in directories:
        walked /= directory
        # create each directory component if needed
        step = (
            origin
            .joinpath(walked)
            .resolve()
        )
        if not step.exists():
            step.mkdir()
    # create file - directories have been created
    args.filepath.resolve().touch()
    args.filepath.write_text("", encoding="utf8") # ensure utf-8 encoded
