'''
AWS CDK setups up a Custom Resource via Cloud Formation which sets the AWS IAM Account Alias

# P6Namer

## LICENSE

[![License](https://img.shields.io/badge/License-Apache%202.0-yellowgreen.svg)](https://opensource.org/licenses/Apache-2.0)

## Other

[![Gitpod ready-to-code](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/p6m7g8/p6-cdk-namer) ![Sonarcloud Status](https://sonarcloud.io/api/project_badges/measure?project=p6m7g8_p6-cdk-namer&metric=alert_status) ![GitHub commit activity](https://img.shields.io/github/commit-activity/y/p6m7g8/p6-cdk-namer) ![GitHub commit activity](https://img.shields.io/github/commit-activity/m/p6m7g8/p6-cdk-namer)

## Usage

```python
...

import { P6Namer } from 'p6-cdk-namer';

new P6Namer(this, 'AccountAlias', {
  accountAlias: 'THE-ALIAS',
});
```

## Architecture

![./assets/diagram.png](./assets/diagram.png)

## Author

Philip M. Gollucci [pgollucci@p6m7g8.com](mailto:pgollucci@p6m7g8.com)
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk
import constructs


@jsii.interface(jsii_type="p6-cdk-namer.IP6NamerProps")
class IP6NamerProps(typing_extensions.Protocol):
    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="accountAlias")
    def account_alias(self) -> builtins.str:
        ...

    @account_alias.setter
    def account_alias(self, value: builtins.str) -> None:
        ...


class _IP6NamerPropsProxy:
    __jsii_type__: typing.ClassVar[str] = "p6-cdk-namer.IP6NamerProps"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="accountAlias")
    def account_alias(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountAlias"))

    @account_alias.setter
    def account_alias(self, value: builtins.str) -> None:
        jsii.set(self, "accountAlias", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IP6NamerProps).__jsii_proxy_class__ = lambda : _IP6NamerPropsProxy


class P6Namer(
    aws_cdk.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="p6-cdk-namer.P6Namer",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        props: IP6NamerProps,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -
        '''
        jsii.create(self.__class__, self, [scope, id, props])


__all__ = [
    "IP6NamerProps",
    "P6Namer",
]

publication.publish()
