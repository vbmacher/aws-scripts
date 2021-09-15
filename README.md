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

### AWS CLI configuration

Before using, please set up AWS CLI configuration:

- `.aws/config`: AWS configuration (e.g. default region to use)
- `.aws/credentials`: AWS key and secret of the AWS account. 
  For more information, visit [AWS CLI configuration][cli-config].

### AWSome scripts accounts

Script `aws-accounts` allows you to manage "profiles" or "accounts" used by AWSome scripts.
One account is represented by a single JSON file in user home directory,
e.g.: `~/.aws-scripts/accounts/your_account.json`. Multiple accounts can be used for multiple real AWS accounts,
or VPCs.

Default account is determined by a symlink `~/.aws-scripts/accounts/.default.json`. This symlink is fully managed
by the `aws-accounts` script.

The content of the files is a JSON, a single object with keys representing AWS services, e.g.:

```
{
  "emr": {
    ...
  },
  "codeartifact": {
    ...
  },
  ...
}
```

CRUD of AWSome accounts and making default account is fully automatic. It is expected from users to just
edit the files and filling the templates values in their accounts. For example, if a user wants to configure AWS EMR,
it is required to execute:

```
aws-accounts -a your_account -c emr
```

This will add EMR template in the `~/.aws-scripts/accounts/your_account.json` file. Then, it is required to manually
open and edit the file to fill the values in.

This setup is required to be done for all supported AWS services, if you want to use AWSome script for those
services.

Note: `aws-accounts` can autofill the settings for some services if you give it a sample. For example, in order to
autofill an EMR configuration, type:

```
aws-accounts -a myaccount -cemr j-D9OAIJX09SJ3
```

## Build

List of prerequisites:

- https://python-poetry.org/
- https://github.com/mtkennerly/poetry-dynamic-versioning

```
poetry build
```

## Local testing

```
poetry install
```

## Publish to PyPi

```
poetry publish
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

- `mwaa` - Executes Airflow CLI command remotely on any MWAA environment

### CodeArtifact

List of available scripts:

- `codeartifact` - Logs in/logs out to CodeArtifact: optionally configures `pip` and `twine` tools




[cli-install]: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html
[cli-config]: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html
[pip]: https://packaging.python.org/tutorials/installing-packages/