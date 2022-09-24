from importlib.metadata import entry_points
from setuptools import find_packages, setup

setup(
    name="PySMS",
    version="0.0.0",
    packages=find_packages(),
    install_requires=[
        "click==8.1.3",
        "Faker==14.2.1",
        "pydantic==1.10.2",
        "pytest==7.1.3",
        "pytest-cov==3.0.0",
        "transliterate==1.10.2"
    ],
    # extras_require={
    #     "'dev'": [
    #         "autopep8==1.7.0",
    #         "flake8==5.0.4",
    #         "pytest==7.1.3",
    #         "pytest-cov==3.0.0"
    #     ]
    # },
    entry_points="""
    [console_scripts]
    pysms=pysms.pysms:pysms
    """
)
