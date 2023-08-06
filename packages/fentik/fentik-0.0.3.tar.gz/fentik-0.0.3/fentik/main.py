import argparse
import sys

from fentik.auth import AuthTokenManager
from fentik.deploy import DeployCommand
from fentik.list import ListCommand
from fentik.clean import CleanCommand
from fentik.util import FentikClient, InitCommand


def main(args):
    auth_manager = AuthTokenManager()
    client = FentikClient(auth_manager)

    init_command = InitCommand()
    list_command = ListCommand(client)
    deploy_command = DeployCommand(client)
    clean_command = CleanCommand(client)

    parser = argparse.ArgumentParser(
        description='Fentik: real time streaming data pipelines'
    )
    subparsers = parser.add_subparsers(help='sub-command help')

    auth_manager.register_subparser(subparsers)
    init_command.register_subparser(subparsers)
    list_command.register_subparser(subparsers)
    deploy_command.register_subparser(subparsers)
    clean_command.register_subparser(subparsers)

    if len(args) == 1:
        parser.print_help()
        sys.exit(0)
    args = parser.parse_args(args[1:])
    args.func(args)
