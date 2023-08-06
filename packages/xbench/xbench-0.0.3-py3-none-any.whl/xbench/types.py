from datetime import datetime, date
from enum import Enum
import pathlib
from pydantic import BaseModel, validate_arguments, StrictFloat, StrictInt
import random
from typing import Any, ForwardRef, Dict, List, Optional, Union, Callable

from impira.types import (
    BBox,
    combine_bboxes,
    Cell,
    ScalarLabel,
    NumberLabel,
    TextLabel,
    TimestampLabel,
    CheckboxLabel,
)

from . import fmt
from . import utils


def traverse(record: Any, fn: Callable[[Any], None]):
    if isinstance(record, ScalarLabel):
        fn(record)
    elif isinstance(record, list):
        for row in record:
            traverse(row, fn)
    else:
        for v in dict(record).values():
            traverse(v, fn)


def gather_tables(record: Any):
    if isinstance(record, ScalarLabel):
        return
    if isinstance(record, list):
        yield record
        for row in record:
            for table in gather_tables(row):
                yield table
    else:
        for v in dict(record).values():
            for table in gather_tables(v):
                yield table


class DocData(BaseModel):
    fname: pathlib.Path = pathlib.Path("")
    url: Optional[str]
    record: Any = None


DocSchema = ForwardRef("DocSchema")


class DocSchema(BaseModel):
    # NOTE: This schema does not support nested objects (only lists, i.e. tables)
    fields: Dict[str, Union[DocSchema, str]]


DocSchema.update_forward_refs()


class DocManifest(BaseModel):
    doc_schema: DocSchema
    docs: List[DocData]


class GenOpts(BaseModel):
    num_rows: Optional[int]
    optional_vals: bool
    build_training_data: bool
    remove_multipage_rows: bool

    def maybe_empty(self, val: Any):
        return val if not self.optional_vals or bool(random.getrandbits(1)) else None


class Config(BaseModel):
    log_level: int
    parallelism: int

    def logger(self, prefix: str):
        return utils.prefixed_logger(prefix, self.log_level)
