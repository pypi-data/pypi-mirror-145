import argparse
from faker import Faker
import logging
import multiprocessing
import random
import sys

from . import bootstrap
from . import capture
from . import evaluate
from . import generate
from . import snapshot
from .utils import parse_int_set
from ..types import Config


def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument("--verbose", "-v", default=False, action="store_true")
    parent_parser.add_argument("--seed", default=201707, type=int)
    parent_parser.add_argument(
        "--parallelism", default=multiprocessing.cpu_count(), type=int
    )

    parser = argparse.ArgumentParser(
        description="Xbench utility to generate data and run benchmarks."
    )
    subparsers = parser.add_subparsers(
        help="sub-command help", dest="subcommand", required=True
    )

    for module in [generate, evaluate, capture, snapshot, bootstrap]:
        cmd_parser = module.build_parser(subparsers, parent_parser, add_doc_args)

    args = parser.parse_args()

    random.seed(args.seed)
    Faker.seed(args.seed)
    level = logging.DEBUG if args.verbose else logging.INFO
    config = Config(log_level=level, parallelism=args.parallelism)
    logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s", level=level)

    return args.func(args, config)


def add_doc_args(parser):
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--all", default=False, action="store_true")
    group.add_argument("--docs", type=parse_int_set)


if __name__ == "__main__":
    sys.exit(main())
