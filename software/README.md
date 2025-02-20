# Software

This directory contains the software and associated testing infrastructure.

## Dependencies/Setup

It is easiest to do everything in a virtual environment. Once you are in the
`software` directory, run the following:

```bash
python3 -m venv env
source ./env/bin/activate
pip3 install -r requirements.lock.txt
```

Then your environment will be setup and you will have all the relevant
packages for local development.

## Mock

The firmware mock is used for testing the software. To start it, run the
following command:

```bash
flask --app firmware_mock run
```

## Software

```bash
flask --app software run
```

