# -*- coding: utf-8 -*-
"""pipeline interface to assemble DAG functions"""

from __future__ import annotations

import abc
from abc import ABC
from typing import List, Dict


class Pipeline(ABC):
    def __init__(self, **kwargs):
        self.upstreams: List[Pipeline] = []
        self.downstreams: List[Pipeline] = []
        self.paramters = kwargs
        self.finished = False

    def __getattr__(self, item):
        if item in self.paramters:
            return self.paramters[item]
        else:
            raise AttributeError

    def run(self):
        for pipeline in self.upstreams:
            if not pipeline.finished:
                return
        self.check_types()
        self.run_job()
        self.finished = True
        for pipeline in self.downstreams:
            pipeline.run()

    @abc.abstractmethod
    def run_job(self):
        pass

    @property
    @abc.abstractmethod
    def parameter_types(self) -> Dict[str, type]:
        pass

    def check_types(self):
        for parameter, parameter_type in self.parameter_types.items():
            if parameter not in self.paramters:
                raise TypeError(f"{parameter} is not defined")
            if not isinstance(self.paramters[parameter], parameter_type):
                raise TypeError(f"{parameter} is not of type {parameter_type}")

    def add_downstream(self, pipeline: Pipeline):
        if pipeline in self.downstreams:
            return
        self.downstreams.append(pipeline)
        pipeline.upstreams.append(self)

    def add_serial_pipeline(self, pipelines: List[Pipeline]):
        node = self
        for pipeline in pipelines:
            node.add_downstream(pipeline)
            node = pipeline

    def transmit_paramters(self, pipeline: Pipeline):
        pipeline.paramters.update(self.paramters)


class P1(Pipeline):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def parameter_types(self):
        return {"a": int}

    def run_job(self):
        print(self.a)
        for downstream in self.downstreams:
            self.transmit_paramters(downstream)


class P2(Pipeline):
    def run_job(self):
        print(self.a)

    @property
    def parameter_types(self):
        return {"a": int}


if __name__ == "__main__":
    p = P1(a=1)
    p2 = P2()
    p.add_downstream(p2)
    p.run()
