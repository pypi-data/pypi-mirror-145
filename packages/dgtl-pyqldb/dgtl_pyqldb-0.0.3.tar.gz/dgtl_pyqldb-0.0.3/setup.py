from setuptools import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="dgtl_pyqldb",
    version="0.0.3",
    description="AWS Quantum Ledger Database python wrapper",
    author="Olivier Witteman",
    license="MIT",
    packages=["dgtl_pyqldb"],
    install_requires=["pyqldb",
                      "boto3",
                      "pandas"],
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
    ]
)

