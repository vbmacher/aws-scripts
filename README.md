# AWSome Scripts

Scripts for comfortable management of AWS services from command line. The idea is to store repeated configuration in
configuration files called "accounts". Then, communication with AWS services can be made very simple.

## Supported AWS services:

- EMR
- MWAA
- CodeArtifact
- more TBD

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

## Building & Local testing

List of prerequisites:

- https://python-poetry.org/
- https://github.com/mtkennerly/poetry-dynamic-versioning

Building:
```
poetry build
```

Local installation in a virtual environment:

```
poetry install
```

Publishing to PyPi:

```
poetry publish
```

## Usage

### Set up your "accounts"

Script `aws-accounts` allows you to manage so-called "accounts" used by AWSome scripts.
An account is a configuration profile for one or more AWS services stored in a single file.
The accounts can be used for:
- multiple real AWS accounts
- multiple VPCs
- multiple custom use cases, custom services or pipelines

Accounts are stored in user home directory, e.g. account `myaccount` is stored in: `~/.aws-scripts/accounts/myaccount.json`. 
A default account is determined by a symlink `~/.aws-scripts/accounts/.default.json`. This symlink is fully managed
by the `aws-accounts` script. If the link does not exist, no default account is set up.

The account file content is a single JSON object with keys representing AWS services, e.g.:

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

CRUD of AWSome accounts and setting the default account is fully managed by `aws-accounts` script. Only use case for 
manual file editing is to fill up the template values in the accounts. The AWS service templates, stored in the account
are also managed by the script. For example, if you want to create AWS EMR configuration template,
run:

```
aws-accounts -a myaccount -c emr
```

This will create AWS EMR template in the `~/.aws-scripts/accounts/myaccount.json` file. It however keeps the previous
values if the EMR service is already there. Then, a usual next step is to manually edit the account file to fill the
real values in the template. This setup is required to be done for most of the supported AWS services

Script `aws-accounts` can autofill the configuration for some AWS services, if you provide a sample. For example,
in order to autofill AWS EMR configuration from the existing cluster, type:

```
aws-accounts -a myaccount -cemr j-D9OAIJX09SJ3
```

## Usage

The following sections describe the usage of the scripts for supported AWS services.

### EMR

List of available scripts:

- `emr-start` - Starts a new cluster
- `emr-submit-spark` - Submits a Spark step (JAR or Python) using spark-submit command
- `emr-terminate` - Terminates a cluster
- `emr-is-idle` - Determines if a cluster is idle

### MWAA

List of available scripts:

- `mwaa` - Executes Airflow CLI command remotely on any MWAA environment

### CodeArtifact

List of available scripts:

- `codeartifact` - Logs in/logs out to CodeArtifact: optionally configures `pip` and `twine` tools




[cli-install]: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html
[cli-config]: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html
[pip]: https://packaging.python.org/tutorials/installing-packages/