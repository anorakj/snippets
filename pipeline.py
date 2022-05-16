# -*- coding: utf-8 -*-
"""pipeline interface to assemble DAG functions"""

from __future__ import annotations

import abc
from abc import ABC
from typing import List, Dict

from rich import traceback

traceback.install()


class Pipeline(ABC):
    def __init__(self, **kwargs):
        self.upstream: List[Pipeline] = []
        self.downstream: List[Pipeline] = []
        self.parameters: Dict = kwargs
        self.finished: bool = False

    def __getattr__(self, item):
        try:
            return self.parameters[item]
        except KeyError:
            raise AttributeError

    def run(self):
        for pipeline in self.upstream:
            if not pipeline.finished:
                return
        self._check_parameter_types()
        self.run_job()
        self.finished = True
        for pipeline in self.downstream:
            pipeline.run()

    @abc.abstractmethod
    def run_job(self):
        pass

    @property
    @abc.abstractmethod
    def parameter_types(self) -> Dict[str, type]:
        pass

    def _check_parameter_types(self):
        for parameter, parameter_type in self.parameter_types.items():
            if parameter not in self.parameters:
                raise TypeError(f"{parameter} is not defined")
            if not isinstance(self.parameters[parameter], parameter_type):
                raise TypeError(f"{parameter} is not of type {parameter_type}")

    def update_parameters(self, **kwargs):
        self.parameters.update(kwargs)

    def add_downstream(self, pipeline: Pipeline):
        if pipeline in self.downstream:
            return
        self.downstream.append(pipeline)
        pipeline.upstream.append(self)

    def add_serial_pipeline(self, pipelines: List[Pipeline]):
        node = self
        for pipeline in pipelines:
            node.add_downstream(pipeline)
            node = pipeline

    def transmit_parameters(self):
        for pipeline in self.downstream:
            pipeline.parameters.update(self.parameters)


class P1(Pipeline):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def parameter_types(self):
        return {"a": int}

    def run_job(self):
        print(self.a)
        self.transmit_parameters()


class P2(Pipeline):
    def run_job(self):
        print(self.a)
        self.transmit_parameters()

    @property
    def parameter_types(self):
        return {"a": int}


class P3(Pipeline):
    def run_job(self):
        print(self.a)
        raise Exception("test")

    @property
    def parameter_types(self):
        return {"a": int}


if __name__ == "__main__":
    p = P1(a=1)
    p2 = P2()
    p3 = P3()
    p.add_downstream(p2)
    p2.add_downstream(p3)
    p.run()
