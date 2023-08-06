# Mite CLI

A command line tool to create a new [mite](https://github.com/sky-uk/mite/) project. 

## Installation

```bash
pip install mite-cli
```

## Usage

```
Usage:
    mite-cli new <project_dir> [options]

Options:
    --log-level=LEVEL       Set logger level: DEBUG, INFO, WARNING, ERROR, CRITICAL [default: INFO]
    -n --novenv             Don't create a python virtual environment
```

### Create new mite project

Create a new project and a virtual environment setup

```bash
mite-cli new my_project_dir
```

You can activate your new virtual environment with `source ~/.virtualenvs/my_project_dir/bin/activate`
This gives you access to the mockserver, mite, etc.

To run your first test, with the virtual environment activated and from within your new project, run:

```bash
./run_test.sh
```

### Installing dependancies

Fedora
```bash
sudo dnf install libcurl-devel
```
Ubuntu
```bash
sudo apt install libcurl4 libcurl4-openssl-dev
```