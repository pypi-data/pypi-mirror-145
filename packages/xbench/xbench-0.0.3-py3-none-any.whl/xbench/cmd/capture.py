"""A one line summary of the module or program, terminated by a period.

Leave one blank line.  The rest of this docstring should contain an
overall description of the module or program.  Optionally, it may also
contain a brief description of exported classes and functions and/or usage
examples.

  Typical usage example:

  foo = ClassFoo()
  bar = foo.FunctionBar()
"""

import pathlib
from shutil import copyfile
from uuid import uuid4

from xbench.tools.textract import Textract
from ..schema import record_to_schema
from ..types import Config, DocManifest


def build_parser(subparsers, parent_parser, add_doc_args):
    capture = subparsers.add_parser(
        "infer-fields",
        help="process a document with AWS Textract and save its fields",
        parents=[parent_parser],
    )
    capture.add_argument("file_name", type=str, help="path to document to use")
    Textract.add_arguments(capture)

    capture.add_argument(
        "--outdir",
        "-d",
        required=True,
        type=str,
        help="Directory to save documents.",
    )

    capture.set_defaults(func=main)
    return capture


def main(args, config: Config):
    log = config.logger("infer-fields")

    log.info("Running '%s' through textract", args.file_name)
    textract = Textract(config=Textract.Config(**{**dict(config), **vars(args)}))
    record = textract.process_document(args.file_name)

    fpath = pathlib.Path(args.file_name)
    fpath_prefix = fpath.name.rsplit(".", 1)[0]
    workdir = pathlib.Path(args.outdir).joinpath(
        "capture", fpath_prefix + "-" + str(uuid4())[:4]
    )
    workdir.mkdir(parents=True, exist_ok=True)
    copyfile(args.file_name, workdir.joinpath(fpath.name))

    docs = [{"fname": fpath.name, "record": record}]
    manifest = DocManifest(doc_schema=record_to_schema(record), docs=docs)

    with open(workdir.joinpath("manifest.json"), "w") as f:
        f.write(manifest.json(indent=2))

    log.info("Document has been written to directory '%s'", workdir)
