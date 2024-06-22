__version__ = "0.1.1"

import argparse
import pathlib

# NOTE: limitation; ``make ..\some.css`` - cannot walk upwards while createing file


class ParserArguments(argparse.Namespace):
    filepath: str
    recursive_mode: bool
    # silent: bool
    # verbose: bool


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="make",
        description="Makes a file with the given filename, encoded in UTF-8",
        add_help=False
    )
    parser.add_argument(
        "-h", "--help",
        action="help",
        help="Show this help message and exit",
        default=argparse.SUPPRESS
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s: v{__version__}",
        help="Show `%(prog)s` version number and exit"
    )
    # print_group = parser.add_mutually_exclusive_group()
    # print_group.add_argument(
    #     "--verbose",
    #     action="store_true",
    #     help="Display more info during execution"
    # )
    # print_group.add_argument(
    #     "--silent",
    #     action="store_true",
    #     help="Display less info during execution"
    # )
    parser.add_argument(
        "-r", "--recursive",
        action="store_true",
        dest="recursive_mode",
        help="Recursively create the folder and file"
    )
    parser.add_argument(
        "filepath",
        help="Filepath to create"
    )

    args = ParserArguments()
    parser.parse_args(namespace=args)

    origin = pathlib.Path.cwd()
    target_path = (
        origin
        .joinpath(args.filepath)
        .resolve()
    )

    if target_path.exists():
        return 1 # path already exists

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
    target_path.resolve().touch()
    target_path.write_text("", encoding="utf8") # ensure utf-8 encoded
    
    return 0
