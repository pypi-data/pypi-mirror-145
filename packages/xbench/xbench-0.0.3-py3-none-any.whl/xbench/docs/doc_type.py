import datetime
from faker import Faker
import importlib
import multiprocessing
import pathlib
from pydantic import BaseModel, validate_arguments
import random
from typing import Any

from ..types import Config, GenOpts
from ..utils import batch

_doc_registry = {}


class DocType(object):
    START_DATE = datetime.date(year=2020, month=1, day=1)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        _doc_registry[cls.DOC_NUMBER] = cls

    @staticmethod
    def get_template_path(fname: str):
        return pathlib.Path(__file__).parent.resolve().joinpath("templates", fname)

    @staticmethod
    def faker():
        return Faker()

    @classmethod
    @validate_arguments
    def generate_doc(cls, dstdir: pathlib.PosixPath, count: int, opts: GenOpts, i: int):
        raise Exception("Unimplemented: generate")

    @classmethod
    @validate_arguments
    def generate(
        cls, dstdir: pathlib.PosixPath, count: int, opts: GenOpts, config: Config
    ):
        # This approach is not ideal but it avoids using multiprocessing.Pool which tries to pickle
        # the inherited function (and fails to do so)
        for b in batch(range(count), config.parallelism):
            for i in b:
                cls.generate_doc(dstdir, opts, config, i)


#                procs = [
#                    multiprocessing.Process(
#                        target=cls.generate_doc, args=(dstdir, opts, config, i)
#                    )
#                    for i in range(count)
#                ]
#                [p.start() for p in procs]
#                [p.join() for p in procs]
