"""Kubernetes Service Binding Library for Python Applications

The Service Binding Specification (https://github.com/k8s-service-bindings/spec)
for Kubernetes standardizes exposing backing service secrets to applications.
This project provides a Python module to consume the bindings projected into the
container.  The Application Projection section of the spec describes how the
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

In the above example, there are two bindings under the `SERVICE_BINDING_ROOT`
directory.  The `account-database` and `transaction-event-system` are the names
of the bindings.  Files within each bindings directory has a special file named
`type`, and you can rely on the value of that file to identify the type of the
binding projected into that directory.  In certain directories, you can also see
another file named `provider`.  The provider is an additional identifier to
narrow down the type further.  This module use the `type` field and, optionally,
`provider` field to look up the bindings.

The `ServiceBinding` object can be instantiated like this:

    from pyservicebinding import binding
    try:
        sb = binding.ServiceBinding()
    except binding.ServiceBindingRootMissingError as msg:
        # log the error message and retry/exit
        print("SERVICE_BINDING_ROOT env var not set")

To get bindings for a specific `type`, say `postgresql`:

    bindings_list = sb.bindings("postgresql")

To get bindings for a specific `type`, say `mysql`, and `provider`, say
`mariadb`:

    bindings_list = sb.bindings("mysql", "mariadb")

To get all bindings irrespective of the `type` and `provider`:

    bindings_list = sb.all_bindings()

"""

import os
import typing

class ServiceBindingRootMissingError(Exception):
    pass


class ServiceBinding:

    def __init__(self):
        """
        - raise ServiceBindingRootMissingError if SERVICE_BINDING_ROOT env var not set
        """
        try:
            self.root = os.environ["SERVICE_BINDING_ROOT"]
        except KeyError as msg:
            raise ServiceBindingRootMissingError(msg)


    def all_bindings(self) -> typing.List[typing.Dict[str, str]]:
        """Get all bindings as a list of dictionaries

        - return empty list if no bindings found
        """
        root = self.root
        l = []
        for dirname in os.listdir(root):
            if not os.path.isdir(os.path.join(root, dirname)):
                continue
            b = {}
            for filename in os.listdir(os.path.join(root, dirname)):
                if not os.path.isfile(os.path.join(root, dirname, filename)):
                    continue
                b[filename] = open(os.path.join(root, dirname, filename)).read().strip()

            l.append(b)

        return l

    def bindings(self, _type: str, provider: typing.Optional[str] = None) -> typing.List[typing.Dict[str, str]]:
        """Get filtered bindings as a list of dictionaries

        - return empty dictionary if no binding found
        - filter the result with the given _type input
        - if provider input is given, filter bindings using the given type and provider
        """
        root = self.root
        l = []
        if provider:
            for dirname in os.listdir(root):
                if not os.path.isdir(os.path.join(root, dirname)):
                    continue
                typepath = os.path.join(root, dirname, "type")
                providerpath = os.path.join(root, dirname, "provider")
                if os.path.exists(typepath):
                    typevalue = open(typepath).read().strip()
                    if typevalue != _type:
                        continue
                    if os.path.exists(providerpath):
                        providervalue = open(providerpath).read().strip()
                        if providervalue != provider:
                            continue

                        b = {}
                        for filename in os.listdir(os.path.join(root, dirname)):
                            if not os.path.isfile(os.path.join(root, dirname, filename)):
                                continue
                            b[filename] = open(os.path.join(root, dirname, filename)).read().strip()

                        l.append(b)
        else:
            for dirname in os.listdir(root):
                if not os.path.isdir(os.path.join(root, dirname)):
                    continue
                typepath = os.path.join(root, dirname, "type")
                if os.path.exists(typepath):
                    typevalue = open(typepath).read().strip()
                    if typevalue != _type:
                        continue

                    b = {}
                    for filename in os.listdir(os.path.join(root, dirname)):
                        if not os.path.isfile(os.path.join(root, dirname, filename)):
                            continue
                        b[filename] = open(os.path.join(root, dirname, filename)).read().strip()

                    l.append(b)

        return l
