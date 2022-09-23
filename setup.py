from importlib.metadata import entry_points
from setuptools import find_packages, setup

setup(
    name="PySMS",
    version="0.0.0",
    packages=find_packages(),
    install_requires=[
        "pytest==7.1.3"
    ],
    entry_points="""
    [console_scripts]
    pysms=pysms.pysms:pysms
    tsc=pysms.pysms:tsc
    """
)