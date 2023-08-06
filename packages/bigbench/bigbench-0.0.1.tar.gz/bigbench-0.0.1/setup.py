# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -*- coding: utf-8 -*-

import os, sys, setuptools
from setuptools import setup


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        data = f.read()
    return data


setup(
    name="bigbench",
    version="0.0.1",
    author="The BIG-Bench Language Models Benchmark team.",
    author_email="bigbench@google.com",
    description="The official api specification for tasks for the 2021 ICLR Large Language Models Workshop.",
    # include PEP-420 subpackages under benchmark_tasks
    packages=(
        setuptools.find_packages()
        + [
            "bigbench.benchmark_tasks." + x
            for x in setuptools.find_namespace_packages(
                where="bigbench/benchmark_tasks", include=["*"]
            )
        ]
    ),
    long_description=read("README.md"),
    long_description_content_type='text/markdown',
    install_requires=[
        "absl-py==0.12.0",
        "black==21.6b0",
        # "bleurt @ https://github.com/google-research/bleurt/archive/b610120347ef22b494b6d69b4316e303f5932516.zip#egg=bleurt",
        "datasets==1.17.0",
        "immutabledict==2.2.1",
        "jax==0.2.16",
        "matplotlib==3.5.1",
        "numpy==1.19.5",
        "pytest==6.2.4",
        "requests-unixsocket==0.2.0",
        "RestrictedPython==5.1",
        "scikit-learn==0.24.2",
        "scipy==1.7.0",
        "seaborn==0.11.2",
        "t5==0.9.1",
        "seqio==0.0.6",
        "tensorflow-text==2.5.0",
        "tensorflow==2.5.0",
        "transformers==4.12.3",
    ],
    package_data={
        "": [
#            "*.json",
#            "*.jsonl",
#            "*.txt",
#            "*.tsv",
#            "*.csv",
#            "*.npz",
#            "*.ckpt",
#            "*.gz",
#            "*.zip",
#            "*.yaml",
#            "*.pkl",
        ]
    },
)
