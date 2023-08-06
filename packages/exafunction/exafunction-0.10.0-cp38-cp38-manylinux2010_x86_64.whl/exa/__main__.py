# Copyright Exafunction, Inc.

""" Entry point into Exafunction's Python tooling """

import argparse
import logging
import sys

from exa.py_module_repository import module_repository_tool

logging.basicConfig(level=logging.INFO)

# TODO(douglas): move to some utils class? This is primarily needed for
# compatibility with Python 3.6/3.7
class _ExtendAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        items = getattr(namespace, self.dest) or []
        items.extend(values)
        setattr(namespace, self.dest, items)


def _main():
    parser = argparse.ArgumentParser()
    parser.register("action", "extend", _ExtendAction)

    # No global arguments yet

    subparsers = parser.add_subparsers(
        title="Subcommands", description="Valid subcommands"
    )

    module_repository_parser = subparsers.add_parser(
        "module_repository",
        aliases=["mr"],
        help="Commands for manipulating the module repository",
    )
    module_repository_parser.set_defaults(tool_main=module_repository_tool.main)
    module_repository_parser.set_defaults(tool_parser=module_repository_parser)
    module_repository_tool.setup_parser(module_repository_parser)

    args = parser.parse_args()

    # Ideally we would use add_subparsers(required=True) but Python 3.6
    # doesn't have it.
    # TODO(douglas): revisit this later
    if not hasattr(args, "tool_main"):
        parser.print_help()
        logging.error("error: missing subcommand")
        sys.exit(-1)

    args.tool_main(args)


if __name__ == "__main__":
    _main()
