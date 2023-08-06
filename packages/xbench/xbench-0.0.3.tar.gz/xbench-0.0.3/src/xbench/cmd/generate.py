import distutils.spawn
import logging
import pathlib
import sys

from xbench import documents
from xbench.types import GenOpts, Config
from .utils import doc_dir


def require_binary(name):
    # https://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
    if distutils.spawn.find_executable(name) is None:
        logging.fatal(
            "The generate command depends on the '%s' binary being available in $PATH. Unable to find it."
            % (name)
        )
        exit(1)


def build_parser(subparsers, parent_parser, add_doc_args):
    generate = subparsers.add_parser(
        "generate", help="generate help", parents=[parent_parser]
    )
    generate.add_argument("scale_factor", type=int, help="relative size of the dataset")
    generate.add_argument(
        "--outdir",
        "-d",
        required=True,
        type=str,
        help="Directory to save generated documents.",
    )
    generate.add_argument(
        "--num-rows",
        type=int,
        default=None,
        help="The exact number of rows per document [for testing purposes only].",
    )
    generate.add_argument(
        "--optional-vals",
        default=False,
        action="store_true",
        help="Whether to include optional values [for testing purposes only]",
    )
    generate.add_argument(
        "--skip-training-data",
        default=False,
        action="store_true",
        help="Pass this flag to skip building training data",
    )
    generate.add_argument(
        "--remove-multipage-rows",
        default=False,
        action="store_true",
        help="Pass this flag to skip building training data",
    )
    add_doc_args(generate)
    generate.set_defaults(func=main)
    return generate


def main(args, config: Config):
    require_binary("soffice")

    if args.remove_multipage_rows and args.skip_training_data:
        logging.fatal(
            "Cannot --remove-multipage-rows unless we build training data. Please remove the --skip-training-data flag"
        )
        return 1

    opts = GenOpts(
        num_rows=args.num_rows,
        optional_vals=args.optional_vals,
        build_training_data=not args.skip_training_data,
        remove_multipage_rows=args.remove_multipage_rows,
    )

    workdir = pathlib.Path(args.outdir).joinpath("docs", "sf-%d" % args.scale_factor)
    docs = set([x for x in documents.keys()]) if args.all else args.docs

    count = 10 ** (args.scale_factor - 1)
    for d in docs:
        if d not in documents:
            logging.fatal("Unknown document type %d" % (d))
            return 1
        dst = workdir.joinpath(doc_dir(d))
        dst.mkdir(parents=True, exist_ok=True)
        logging.debug("Generating document %d at path: %s", d, dst)
        documents[d].generate(dst, count, opts, config)

        logging.info(
            "Done! %d instances each of document numbers %d have been generated at path: %s. You can now run `xbench eval` against this directory."
            % (count, d, workdir)
        )
