# AWSome Scripts

Scripts for comfortable management of AWS services from command line.

**NOTE: The scripts do not work as yet. Work in progress, stay tuned.**

## Installation

List of prerequisites:

- [AWS Command Line Interface (CLI)][cli-install]
- Python 3 + [pip][pip]

AWS Scripts installation (using `pip`):

```
python3 -m pip install aws-scripts
```

Before using, please set up AWS CLI configuration:

- `.aws/config`: AWS configuration (e.g. default region to use)
- `.aws/credentials`: AWS key and secret of the AWS account. 
  For more information, visit [AWS CLI configuration][cli-config].

## Build

List of prerequisites:

- https://python-poetry.org/
- https://github.com/mtkennerly/poetry-dynamic-versioning

```
python3 -m pip install --upgrade build
python3 -m build
```

## Usage

The following sections describe the usage of the scripts for supported AWS services.

### EMR

List of available scripts:

- `emr-start` - Starts a new cluster
- `emr-submit-spark` - Submits a JAR file using spark-submit command as EMR step
- `emr-terminate` - Terminates a cluster
- `emr-is-idle` - Determines if a cluster is idle for at least 2 hours (and prints for how long it is idle)

### MWAA

List of available scripts:

- `mwaa-cli` - Executes Airflow CLI command remotely on any MWAA environment

### CodeArtifact

List of available scripts:

- `codeartifact` - Logs in/logs out to CodeArtifact: optionally configures `pip` and `twine` tools




[cli-install]: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html
[cli-config]: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html
[pip]: https://packaging.python.org/tutorials/installing-packages/