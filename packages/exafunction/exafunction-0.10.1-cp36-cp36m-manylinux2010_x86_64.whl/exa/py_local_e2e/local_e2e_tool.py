# Copyright Exafunction, Inc.

""" Entry point for the Exafunction local e2e tool """

import logging
import os
import subprocess
import sys


def setup_parser(subparser):
    """Sets up the argument subparser"""
    subparser.add_argument("image_name", type=str)
    subparser.add_argument("--config", type=str, action="extend", nargs="+")
    subparser.add_argument("--no_default_config", action="store_true")


_DEFAULT_CONFIG_FILE = os.path.join(os.path.dirname(__file__), "default_config.pbtxt")


def main(args):
    """The main function for this tool"""

    image_name = args.image_name
    configs = args.config

    configs = []
    if not args.no_default_config:
        configs.append(_DEFAULT_CONFIG_FILE)

    if args.config is not None:
        configs.extend(args.config)

    cmd = [
        "docker",
        "run",
        "--net=host",
        "--gpus=all",
        "-it",
        "--rm",
        "--mount",
        "type=bind,source=/tmp/exafunction,target=/tmp/exafunction",
        "--mount",
        "type=bind,source=/dev/shm,target=/dev/shm",
        "--shm-size=1024m",
    ]

    for config in configs:
        real_config = os.path.realpath(config)
        cmd.extend(["--mount", f"type=bind,source={real_config},target={real_config}"])

    cmd.extend(
        [
            f"{image_name}",
        ]
    )

    for config in configs:
        real_config = os.path.realpath(config)
        cmd.extend(["--config", real_config])

    logging.info("Running command %s", cmd)

    # Don't print Python stacktrace on failure, just exit with the right
    # return code.
    ret = subprocess.run(cmd, check=False)
    sys.exit(ret.returncode)
