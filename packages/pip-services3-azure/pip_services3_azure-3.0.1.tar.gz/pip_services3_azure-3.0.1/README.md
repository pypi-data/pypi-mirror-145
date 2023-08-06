# <img src="https://uploads-ssl.webflow.com/5ea5d3315186cf5ec60c3ee4/5edf1c94ce4c859f2b188094_logo.svg" alt="Pip.Services Logo" width="200"> <br/> Azure specific components for Python

This module is a part of the [Pip.Services](http://pip.services.org) polyglot microservices toolkit.

Contains packages used to create containers and services that do operations via the Azure cloud.

The module contains the following packages:
- **Clients** - client components for working with Azure cloud Functions.
- **Connect** - components for installation and connection settings.
- **Containers** - contains classes that act as containers to instantiate and run components.
- **Services** - contains interfaces and classes used to create services that do operations via the Azure Function protocol.

<a name="links"></a> Quick links:

* [Configuration Pattern](http://docs.pipservices.org/toolkit/getting_started/configurations/) 
* [API Reference](https://pip-services3-python.github.io/pip-services3-azure-python/index.html)
* [Change Log](CHANGELOG.md)
* [Get Help](http://docs.pipservices.org/get_help/)
* [Contribute](http://docs.pipservices.org/toolkit/contribute/)

## Use

Install the Python package as
```bash
pip install pip-services3-azure
```

## Develop

For development you shall install the following prerequisites:
* Python 3.6+
* Visual Studio Code or another IDE of your choice
* Docker

Install dependencies:
```bash
pip install -r requirements.txt
```

Run automated tests:
```bash
python test.py
```

Generate API documentation:
```bash
./docgen.ps1
```

Before committing changes run dockerized build and test as:
```bash
./build.ps1
./test.ps1
./clear.ps1
```

## Contacts

The library is created and maintained by:
- **Sergey Seroukhov**
- **Danil Prisiazhnyi**
