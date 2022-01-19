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

## License

This project is released under the [MIT License][mit-license].

<a href="https://www.buymeacoffee.com/vbmacher" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>


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

The following sections describe the list of usable commands which correspond to particular AWS services.

### Sketches

Command: `awss s`

A sketch is a configuration file for one or more AWS services ("sketch items").

Sketch files are stored in user home directory, e.g. `~/.aws-scripts/sketches/mysketch.json`.
A default sketch is determined by a symlink `~/.aws-scripts/sketches/.default.json`.

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

Sketches can be fully or partially managed with `awss s` command, but you're encouraged to fill them manually. The
command won't remove or replace your changes, only if explicitly advised to do so.

Some examples:
- creating AWS EMR sketch item: `awss s -c emr`
- auto-configure AWS EMR sketch item: `awss s -cemr j-D9OAIJX09SJ3`

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
[mit-license]: https://opensource.org/licenses/MIT