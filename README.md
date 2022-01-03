# AWSome Scripts

Scripts bringing up opinionated convention and simplification of **manual** work with AWS services from command line.

For example, the whole setup of the scripts and then start an EMR cluster (nothing else is needed):

```
aws-accounts -a my-emr -d -cemr j-D9OAIJX09SJ3
emr-start -n "My cluster" -c 5 -i "r5.xlarge" -S
```

## Project goals

### Functional goals

- the scripts should allow reusing various configurations of AWS services
  - by having multiple profiles/accounts stored in files
- the scripts should simplify using AWS services from command line
  - starting/stopping EMR clusters / EC2 instances
  - logging in/out from codeartifact, 
  - sending a message to SQS queue
  - bypass Airflow commands though MWAA HTTP calls
  - etc.
- the scripts should allow to run a pipeline file written using a DSL language.
  - the pipeline should be able to use "templates" stored elsewhere
  - the DSL should allow to use variables
  - the DSL should allow to use loops, date range generation, file copying
  - the DSL should allow to replace values from external configuration file (e.g. typesafe HOCON) using
    some templating language (JINJA??) 
- the scripts should track progress of work
- the scripts should allow to interrupt/resume work
  - transactional work if possible

### Non-functional goals

- it should be possible to use the scripts as Python library
- it should be possible to use command line version of the scripts
- the scripts should be published to public PyPy.
- the scripts should be versioned semantically, best by integrating with git tags (pbr)

### Non-goals

- AWSome scripts is not "resisent" application. It means no scheduling capability or active monitoring will be supported

## Supported AWS services:

Current focus is on the following services:

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

Prerequisites:

```
pip install --upgrade pip
pip install --upgrade setuptools
pip install pbr
pip install mypy
pip install flake8
pip install twine
```

Build:

```
# static types check
mypy aws-scripts/awsscripts/

# style check
flake8 --max-line-length 120 aws-scripts/awsscripts/

# build AWSome Scripts
cd aws-scripts/; python setup.py sdist bdist_wheel

# distribution check
twine check aws-scripts/dist/*
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

## For Developers

### Conventions

Script file names should be composed of words separated with plain dashes, in format: `[service]-[function]`,
e.g. `emr-start`. 

Source code file names should be composed of words separated with underscores, in format: `[service]_[function].py`,
e.g. `emr_start.py`. 



[cli-install]: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html
[cli-config]: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html
[pip]: https://packaging.python.org/tutorials/installing-packages/