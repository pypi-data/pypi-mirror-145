#!/usr/bin/env python3

from __future__ import annotations

import contextlib
import csv
import dataclasses
import enum
import functools
import importlib.metadata
import json
import os
import pathlib
import re
import site
import subprocess
import sys
import typing as t
import venv

import configargparse


def main():
    parser = get_parser()
    arguments = parser.parse_args()
    verbosity = Verbosity(min(arguments.verbosity, 3))

    arguments.func(arguments)


def activate_virtual_env(path: pathlib.Path):
    version = sys.version_info
    site_packages = path / 'lib' / f'python{version.major}.{version.minor}' / 'site-packages'
    site.addsitedir(site_packages)


def do_usage(
    arguments: argparser.Namespace,
    parser: configargparse.ArgumentParser,
) -> None:
    parser.print_help()


def do_install(arguments: configargparse.Namespace):
    installables: list[str] = arguments.packages

    virtual_env_dir = arguments.virtual_env_dir

    if arguments.name:
        virtual_env = virtual_env_dir / arguments.name
    elif arguments.virtual_environment:
        virtual_env = arguments.virtual_environment
    else:
        if len(installables) == 1:
            package_name = installable_to_package_name(installables[0])
            virtual_env = virtual_env_dir / package_name
        else:
            raise CommandError(
                "You must specify --name or --path if installing multiple "
                "packages into one environment.\n"
                "See `pips --help' for usage")

    print(f"Creating virtual environment {display_path(virtual_env)}")
    venv.create(virtual_env, with_pip=True)

    print("Installing", " ".join(installables))
    subprocess.call([
        str(virtual_env / "bin" / "pip"), "install", "--upgrade", "pip",
    ])
    subprocess.call([
        str(virtual_env / "bin" / "pip"), "install", *installables
    ])
    activate_virtual_env(virtual_env)

    # Transform the things we just installed to a list of package names.
    # TODO Do proper introspection of the package files to find the package name,
    # instead of hoping the filename is correct
    package_names = list(map(installable_to_package_name, installables))

    executables = {
        package: list(find_executables(virtual_env, package))
        for package in package_names
    }

    with open(virtual_env / 'pips.json', 'w') as f:
        json.dump({
            "version": 1,
            "packages": package_names,
            "executables": {name: [str(p) for p in paths] for name, paths in executables.items()},
        }, f)

    print("Symlinking binaries...")
    for package in package_names:
        print(f"* Package {package}")
        for executable in executables[package]:
            print(f"  * {executable.name}")
            symlink_executable(executable, arguments.bin)


def installable_to_package_name(installable: str) -> str:
    installable_path = pathlib.Path(installable)
    if installable_path.exists():
        # TODO Extract the package name by looking for the METADATA in the package
        name = re.sub('(-\d+)\.(.*)$', '', installable_path.name)
    else:
        name = re.match('^[a-zA-Z0-9_.-]+', installable).group(0)
    return name


def do_list(arguments: configargparse.ArgumentParser):
    for entry in arguments.virtual_env_dir.iterdir():
        if not entry.is_dir():
            continue

        try:
            with open(entry / 'pips.json', 'r') as f:
                info = json.load(f)
        except ValueError:
            continue
        if info.get('version') != 1:
            continue

        name = display_path(entry)
        executables = info['executables'].keys()
        print(f"{name}")
        print(f"{'=' * len(name)}")
        for package in info['packages']:
            print(f'* {package}')
            executables = info['executables'].get(package, [])
            for executable in executables:
                print(f'  * {display_path(pathlib.Path(executable))}')
        print('')


def find_executables(
    virtual_env: pathlib.Path,
    package: str,
) -> t.Iterable[pathlib.Path]:

    distribution = importlib.metadata.distribution(package)

    site_packages = next(
        p for s in sys.path
        if (p := pathlib.Path(s)).is_relative_to(virtual_env)
    )
    bin = virtual_env / 'bin'

    # Distribution.files contains all the files that were installed as part of
    # the package, including anything in the virtualenv bin directory
    for relative_path in distribution.files:
        assert not relative_path.is_absolute()
        absolute_path = (site_packages / relative_path).resolve()
        assert absolute_path.is_relative_to(virtual_env)
        if absolute_path.is_relative_to(bin):
            yield(absolute_path)


def symlink_executable(executable_path: pathlib.Path, bin: pathlib.Path):
    symlink_path = bin / executable_path.name
    if os.path.lexists(symlink_path):
        if symlink_path.resolve() == executable_path:
            return
        else:
            raise CommandError(
                f"File {str(symlink_path)!r} already exists, and is not a "
                f"symlink to {str(executable_path)!r}!"
            )
    symlink_path.symlink_to(executable_path)


def get_parser() -> configargparse.ArgumentParser:
    """Construct a `pips` ArgumentParser."""
    parser = configargparse.ArgumentParser(
        prog="pips",
        formatter_class=configargparse.RawDescriptionHelpFormatter,
        default_config_files=['/etc/pips.yaml', '~/.config/pips.yaml'],
    )
    usage = functools.partial(do_usage, parser=parser)
    parser.set_defaults(func=usage)
    subparsers = parser.add_subparsers()

    help_cmd = subparsers.add_parser('help')
    help_cmd.set_defaults(func=usage)

    install_cmd = subparsers.add_parser('install')
    install_cmd.add_argument('packages', nargs='+')
    install_cmd.set_defaults(func=do_install)
    name_or_path = install_cmd.add_mutually_exclusive_group()
    name_or_path.add_argument(
        '-n', '--name',
        help="Name of virtual environment to install packages in.")
    name_or_path.add_argument(
        '-p', '--path',
        type=pathlib.Path, dest="virtual_environment",
        help="Path to virtual environment to install packages in.")
    install_cmd.add_argument(
        '--bin',
        type=pathlib.Path, dest="bin",
        default=pathlib.Path.home() / '.local' / 'bin',
        help="Local bin directory to install executables in to")

    list_cmd = subparsers.add_parser('list')
    list_cmd.set_defaults(func=do_list)

    config = parser.add_argument(
        '-c', '--config', is_config_file=True,
        env_var='PIPS_CONFIG_FILE',
        help="Path to a configuration file.")
    virtual_env_dir = parser.add_argument(
        '--virtual-env-dir',
        env_var='PIPS_VIRTUAL_ENV_DIR',
        default=pathlib.Path.home() / '.local' / 'share' / 'pips' / 'environments',
        help=(
            "Default directory where new virtual environments will be created."
        ))
    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument(
        '-v', '--verbose',
        action='count', dest='verbosity',
        help=(
            "Print more information when transferring. "
            "Add twice for even more output."
        ))
    verbosity.add_argument(
        '-q', '--quiet',
        action='store_const', dest='verbosity', const=0,
        help="Don't print anything except errors.")
    parser.set_defaults(verbosity=1)

    return parser


def display_path(path: pathlib.Path) -> str:
    home = pathlib.Path.home()
    if path.is_relative_to(home):
        path = pathlib.Path('~') / path.relative_to(home)
    path_str = str(path)
    if not path_str.isprintable():
        return repr(path_str)
    should_escape = '\'"{}[]:'
    if any(c.isspace() or c in should_escape for c in path_str):
        return repr(path_str)
    return path_str


class Verbosity(enum.IntEnum):
    """
    How much noise to make in the console. Select using --quiet or --verbose.
    """
    silent = 0
    minimal = 1
    most = 2
    all = 3


class CommandError(Exception):
    code: int

    def __init__(self, message: str, code: int = 1):
        super().__init__(message)
        self.code = code

    def exit(self) -> t.NoReturn:
        print(str(self), file=sys.stderr, flush=True)
        sys.exit(self.code)


@contextlib.contextmanager
def handle_errors() -> t.Iterator[None]:
    try:
        yield
    except CommandError as exc:
        exc.exit()
    except KeyboardInterrupt:
        sys.exit(1)


def run():
    with handle_errors():
        main()


if __name__ == '__main__':
    run()
