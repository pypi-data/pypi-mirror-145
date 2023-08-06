import json
import pathlib
from shutil import copyfile
from uuid import uuid4

from xbench.tools.impira import Impira
from ..schema import schema_to_model
from ..types import Config, DocData, DocManifest


def build_parser(subparsers, parent_parser, add_doc_args):
    bootstrap = subparsers.add_parser(
        "bootstrap",
        help="setup Impira using an existing document file and schema",
        parents=[parent_parser],
    )
    bootstrap.add_argument(
        "--data",
        "-d",
        required=True,
        type=str,
        help="Directory to retrieve document. This directory should contain one or more documents and a manifest (manifest.json)",
    )
    bootstrap.add_argument(
        "--skip-new-fields",
        default=False,
        action="store_true",
        help="Only label existing fields in the collection",
    )
    Impira.add_arguments(bootstrap)

    bootstrap.set_defaults(func=main)
    return bootstrap


def main(args, config: Config):
    log = config.logger("bootstrap")

    workdir = pathlib.Path(args.data)

    manifest_file = workdir.joinpath("manifest.json")

    if not manifest_file.exists():
        log.fatal("No manifest.json file found in %s", workdir)

    manifest = DocManifest.parse_file(manifest_file)
    M = schema_to_model(manifest.doc_schema)

    for doc in manifest.docs:
        doc.fname = workdir.joinpath(doc.fname)
        assert doc.url is not None or doc.fname.exists()
        if doc.record is not None:
            doc.record = M.parse_obj(doc.record)

    tool = Impira(config=Impira.Config(**{**dict(config), **vars(args)}))
    tool.run(manifest.doc_schema, manifest.docs, skip_new_fields=args.skip_new_fields)
