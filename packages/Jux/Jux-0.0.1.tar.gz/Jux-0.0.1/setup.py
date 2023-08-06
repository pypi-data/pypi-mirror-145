from subprocess import list2cmdline
from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name="Jux",
    version="0.0.1",
    description="X-RAY Flare Burst Deterministic Detection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Team 10",
    packages=[".jux"],
    install_requires=[
        "astropy",
        "numpy",
        "pandas",
        "matplotlib",
        "scipy",
        "plotly",
        "sklearn",
    ],
    liscense="MIT",
    py_modules=[
        "file_handler",
        "create_df_minmax",
        "denoise",
        "false_positive_detection",
        "flare_detect_minmax",
        "flare_detect_thresh",
        "helper",
        "param",
        "version",
        "jux",
    ],
)
