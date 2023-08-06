from setuptools import setup

setup(
    name="dgtl_pyqldb",
    version="0.0.2",
    description="AWS Quantum Ledger Database python wrapper",
    author="Olivier Witteman",
    license="MIT",
    packages=["dgtl_pyqldb"],
    install_requires=["pyqldb",
                      "boto3",
                      "pandas"],
    classifiers=[
    ]
)

