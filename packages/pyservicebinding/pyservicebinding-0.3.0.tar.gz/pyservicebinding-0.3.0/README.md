# pyservicebinding
> **Kubernetes Service Binding Library for Python Applications**

![PyPI - Downloads](https://img.shields.io/pypi/dm/pyservicebinding)
![Release](https://img.shields.io/pypi/v/pyservicebinding)
![Supported Python Versions](https://img.shields.io/pypi/pyversions/pyservicebinding)
[![CI](https://github.com/baijum/pyservicebinding/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/baijum/pyservicebinding/actions/workflows/ci.yml)

The [Service Binding Specification][spec] for Kubernetes standardizes exposing
backing service secrets to applications.  This project provides a Python module
to consume the bindings projected into the container.  The [Application
Projection][application-projection] section of the spec describes how the
bindings are projected into the application.  The primary mechanism of
projection is through files mounted at a specific directory.  The bindings
directory path can be discovered through `SERVICE_BINDING_ROOT` environment
variable.  The operator must have injected `SERVICE_BINDING_ROOT` environment to
all the containers where bindings are created.

Within this service binding root directory, there could be multiple bindings
projected from different Service Bindings.  For example, suppose an application
requires to connect to a database and cache server. In that case, one Service
Binding can provide the database, and the other Service Binding can offer
bindings to the cache server.

Let's take a look at the example given in the spec:

```
$SERVICE_BINDING_ROOT
├── account-database
│   ├── type
│   ├── provider
│   ├── uri
│   ├── username
│   └── password
└── transaction-event-stream
    ├── type
    ├── connection-count
    ├── uri
    ├── certificates
    └── private-key
```

In the above example, there are two bindings under the `SERVICE_BINDING_ROOT`
directory.  The `account-database` and `transaction-event-system` are the names
of the bindings.  Files within each bindings directory has a special file named
`type`, and you can rely on the value of that file to identify the type of the
binding projected into that directory.  In certain directories, you can also see
another file named `provider`.  The provider is an additional identifier to
narrow down the type further.  This module use the `type` field and, optionally,
`provider` field to look up the bindings.

## Installation

You can install this package using pip:

```bash
pip install pyservicebinding
```

## Usage

The `ServiceBinding` object can be instantiated like this:
```python
from pyservicebinding import binding
try:
    sb = binding.ServiceBinding()
except binding.ServiceBindingRootMissingError as msg:
    # log the error message and retry/exit
    print("SERVICE_BINDING_ROOT env var not set")
```

To get bindings for a specific `type`, say `postgresql`:

```python
bindings_list = sb.bindings("postgresql")
```

To get bindings for a specific `type`, say `mysql`, and `provider`, say `mariadb`:

```python
bindings_list = sb.bindings("mysql", "mariadb")
```

To get all bindings irrespective of the `type` and `provider`:

```python
bindings_list = sb.all_bindings()
```

This is the complete API of the module:
```python

class ServiceBindingRootMissingError(Exception):
    pass


class ServiceBinding:

    def __init__(self):
        """
        - raise ServiceBindingRootMissingError if SERVICE_BINDING_ROOT env var not set
        """

    def all_bindings(self) -> list[dict[str, str]]:
        """Get all bindings as a list of dictionaries

        - return empty list if no bindings found
        """

    def bindings(self, _type: str, provider: typing.Optional[str] = None) -> list[dict[str, str]]:
        """Get filtered bindings as a list of dictionaries

        - return empty dictionary if no binding found
        - filter the result with the given _type input
        - if provider input is given, filter bindings using the given type and provider
        """
```

[spec]: https://github.com/k8s-service-bindings/spec
[application-projection]: https://github.com/k8s-service-bindings/spec#application-projection
