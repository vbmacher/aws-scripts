# AWSome Scripts

A tool for convenient calling of AWS CLI. It brings:

- an opinionated simplification over **manual** user-AWS interaction,
- it saves and reuses repeated AWS service configuration.

For example, in order to start an EMR cluster with configuration similar to already existing cluster:

```
# Creates sketch "mysketch", makes it default and configures it with EMR copied from existing cluster
awss s -s mysketch -d -cemr j-D9OAIJX09SJ3

# Starts new EMR cluster, using config from the now-default sketch "mysketch"
# and hardware: 1 on-demand master node and 5 spot core nodes of type r5.xlarge
awss emr start -n "My cluster" -c 5 -i "r5.xlarge" -S
```

## Project goals

### Functional goals

- ~~the scripts should allow reusing various configurations of AWS services~~
    - ~~by having multiple "sketches" stored in files~~
- the scripts should simplify using AWS services from command line
    - ~~starting/stopping EMR clusters~~
    - starting/stopping EC2 instances
    - ~~logging in/out from codeartifact~~
    - sending a message to SQS queue
    - ~~bypass Airflow commands though MWAA HTTP calls~~
    - etc.
- the scripts should allow to run a pipeline file written using a DSL language.
    - the pipeline should be able to use "sketch items" stored in existing sketches
    - the DSL should allow to use variables
    - the DSL should allow to use loops, date range generation, file copying
    - the DSL should allow to replace values from external configuration file (e.g. typesafe HOCON) using some
      templating language (JINJA??)
- the scripts should track progress of work
- the scripts should allow to interrupt/resume work
    - transactional work if possible

### Non-functional goals

- it should be possible to use the scripts as Python library
- it should be possible to use command line version of the scripts
- the scripts should be published to public PyPy.
- the scripts should be versioned semantically, best by integrating with git tags (pbr)

### Non-goals

- AWSome scripts is not "resident" application. It means no scheduling capability or active monitoring will be supported

## Supported AWS services:

Current focus is on the following services:

- EMR
- EC2
- MWAA
- CodeArtifact

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
- `.aws/credentials`: AWS key and secret of the AWS account. For more information,
  visit [AWS CLI configuration][cli-config].

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

### Set up your "sketches"

Command: `awss s`

A sketch is a configuration file for one or more AWS services ("sketch items"). The sketches can be used for:

- real AWS accounts
- VPCs
- custom use cases, custom services or pipelines

Sketches are stored in user home directory, e.g. sketch `mysketch` is stored in: `~/.aws-scripts/sketches/mysketch.json`
. A default sketch is determined by a symlink `~/.aws-scripts/sketches/.default.json`. This symlink is fully managed by
the `awss s` command. If the link does not exist, no default sketch is set up.

The sketch file content is a single JSON object with keys representing AWS services, e.g.:

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

CRUD of AWSome sketches and setting the default sketch is fully managed by `awss s` command. The only use case for
manual file editing is to fill up the sketch item values. The AWS service sketch items (templates), stored in a sketch,
are also managed by the command. For example, if you want to create AWS EMR configuration sketch item, run:

```
awss sketches -c emr
```

This will create AWS EMR sketch item in the `~/.aws-scripts/sketches/mysketch.json` file. It however keeps the previous
values if the EMR service is already there. Then, a usual next step is to manually edit the sketch file to fill the real
values. This setup is required to be done for most of the supported AWS services.

The command `awss s` can autofill the configuration for some AWS services, if you provide a sample. For example, in
order to autofill AWS EMR configuration from the existing cluster, type:

```
awss s -cemr j-D9OAIJX09SJ3
```

## Usage

The following sections describe the list of usable commands which correspond to particular AWS services.

### EMR

Command: `awss emr`

List of available subcommands:

- `start` - Starts a new cluster
- `submit` - Submits a Spark step (JAR or Python) using spark-submit command
- `terminate` - Terminates a cluster
- `isidle` - Determines if a cluster is idle

### MWAA

Command: `awss mwaa`

Executes Airflow CLI command remotely on any MWAA environment

### CodeArtifact

Command: `awss ca`

List of available subcommands:

- `login` - Logs in to CodeArtifact: optionally configures `pip` and `twine` tools
- `logout` - Logs out from CodeArtifact: optionally configures `pip` tool

[cli-install]: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html
[cli-config]: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html
[pip]: https://packaging.python.org/tutorials/installing-packages/