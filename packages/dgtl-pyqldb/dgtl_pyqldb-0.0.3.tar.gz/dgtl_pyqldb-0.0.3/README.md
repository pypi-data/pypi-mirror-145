# DGTL Health AWS Quantum Ledger Database Wrapper

Use this code to access the ledger based databases.

As of writing, `2022-04-07`, the pyqldb library has a dependency that doesn't
compile on Apple ARM-processors. For local development make a venv 
with the intel64-python to use Rosetta2 emulation.
Compiling with --platform linux/arm64 using docker will work normally.

## Installation
- (Optional) Create venv: `python3 -m venv venv` or on Apple Silicon: `python3-intel64 -m venv venv`
- (Optional) Activate venv: `source venv/bin/activate`
- Install: `python -m pip install dgtl-pyqldb`


## Usage
- Make sure you AWS credentials are set-up using `aws-config`
- `from dgtl_pyqldb.ledger_helper import LedgerHelper`
- `lh = LedgerHelper(ledger_name="pyqldb_tests", table="test_ledger", index="PID", region="eu-central-1")`
