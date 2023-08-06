import argparse
from collections import defaultdict
import logging
import pathlib
import re

from xbench import documents, registry
from .utils import doc_dir
from ..schema import record_to_schema
from ..types import Config, DocData


def build_parser(subparsers, parent_parser, add_doc_args):
    evaluate = subparsers.add_parser("evaluate", help="evaluate help")

    sub_parent_parser = argparse.ArgumentParser(add_help=False)
    sub_parent_parser.add_argument(
        "--data",
        "-d",
        required=True,
        type=str,
        help="Directory to retrieve generated documents. This directory should contain one folder for each doc type you want to evaluate.",
    )
    add_doc_args(sub_parent_parser)

    subparsers = evaluate.add_subparsers(
        help="evaluate [tools] help", dest="tool", required=True
    )

    for name, ToolCls in registry.items():
        parser = subparsers.add_parser(
            name, help="%s help" % (name), parents=[parent_parser, sub_parent_parser]
        )
        ToolCls.add_arguments(parser)

    evaluate.set_defaults(func=main)
    return evaluate


def main(args, config: Config):
    workdir = pathlib.Path(args.data)
    docs = set([x for x in documents.keys()]) if args.all else args.docs

    if args.tool not in registry:
        logging.fatal("Unknown tool: %s", args.tool)
        exit(1)

    ToolCls = registry[args.tool]

    doc_data = {}
    for d in docs:
        full_path = workdir.joinpath(doc_dir(d))
        if not full_path.exists():
            logging.fatal(
                "Expected directory %s to exist for document %d" % (full_path, d)
            )
            exit(1)

        entries = defaultdict(lambda: DocData())
        DocCls = documents[d]
        for full_name in full_path.iterdir():
            doc_name, ext = full_name.name.rsplit(".", -1)
            if not re.match(r"^d[\d+]-[\d+]$", doc_name):
                logging.debug("Skipping file %s..." % (full_name))
                continue

            entry = entries[doc_name]
            if ext == "json":
                entry.record = DocCls.Record.parse_file(full_name)
            else:
                assert ext == "pdf", "Unknown file %s" % (full_name)
                entry.fname = full_name

        entries_l = [x for x in entries.values()]
        entries_l.sort(key=lambda x: x.fname)

        doc_data[d] = entries_l

    for d in docs:
        logging.info("Evaluating %s on document %s..." % (ToolCls.__name__, d))
        entries = doc_data[d]
        tool = ToolCls(config=ToolCls.Config(**{**dict(config), **vars(args)}))
        tool.run(
            record_to_schema(entries[0].record),
            entries,
            collection_prefix="xbench",
            parallelism=args.parallelism,
            existing_collection_uid=None,
            skip_type_inference=False,
            skip_upload=False,
            add_files=False,
            skip_new_fields=False,
            collection_name=None,
            max_fields=None,
            max_files=None,
        )
