<p align=center><img align=center src='docshund.png' width=500 /></p>
<h3 align=center>d o c s h u n d</h3>
<h6 align=center>simple code documentation generation</h6>
<p align=center>
<a href="https://pypi.org/project/docshund/"><img alt="PyPI" src="https://img.shields.io/pypi/v/docshund.svg?logo=python&logoColor=orange&style=for-the-badge"></a>
    <img src="https://img.shields.io/github/issues/FitMango/docshund.svg?style=for-the-badge" />
<img src="https://img.shields.io/github/license/FitMango/docshund.svg?style=for-the-badge" />
</p>

> NOTE: Docshund is in alpha and may not yet be suitable for production workloads. Please exercise caution when using. (We'll try not to break everything if you promise not to expect it not to break everything.)

# Why

We were tired of complex, long-running doc-generators. In some cases, we wanted to generate documentation for our source but didn't want to install _all_ of our libraries' dependencies just to make a small change to a README. Docshund is the answer to this problem. Docshund doesn't require pip-installation of your package and, even for large projects, runs in just a handful of milliseconds. 

On the flip-side, Docshund does not have the same featurelist as many other libraries, and Docshund also has a hard time jumping up onto your couch without help.

# Installation

```python
pip3 install docshund
```

# Usage

```shell
docshund code.py > documentation.md
```

Or document an entire module with:

```shell
docshund .
```

```shell
docshund /path/to/module
```

## What she do:

Go from this:

```python
class Foo:
    """
    This is a foo.

    Do not cross the foo streams!
    """

    def __init__(self):
        """
        Create a new foo.
        """

    def cross_streams(self, other_foo: Foo = None):
        """
        Cross the streams of this foo with another foo.

        If you do this, it will throw an error.

        Arguments:
            other_foo (Foo: None): The foo with which you'd like to cross streams

        Returns:
            None

        Raises:
            FooError: Raised if you cross the streams.

        """
        if other_foo:
            raise FooError("What did we JUST tell you?!")
```

To this markdown:

```
## *Class* `Foo`


This is a foo.

Do not cross the foo streams!


## *Function* `__init__(self)`


Create a new foo.


## *Function* `cross_streams(self, other_foo: Foo = None)`


Cross the streams of this foo with another foo.

If you do this, it will throw an error.

### Arguments
> - **other_foo** (`Foo`: `None`): The foo with which you'd like to cross streams

### Returns
    None

### Raises
> - **FooError** (`None`: `None`): Raised if you cross the streams.
```

## *Class* `Foo`


This is a foo.

Do not cross the foo streams!


## *Function* `__init__(self)`


Create a new foo.


## *Function* `cross_streams(self, other_foo: Foo = None)`


Cross the streams of this foo with another foo.

If you do this, it will throw an error.

### Arguments
> - **other_foo** (`Foo`: `None`): The foo with which you'd like to cross streams

### Returns
    None

### Raises
> - **FooError** (`None`: `None`): Raised if you cross the streams.
---

# Generating documentation for this repository

The reference documentation for this repository was generated using the following command:

```shell
docshund docshund/__init__.py > docs/Reference.md
```

You might say we... 😎 ate our own dogfood.

---

## Legal

Licensed under Apache 2.0. Reach out to opensource@fitmango.com with questions.

> Copyright 2019 FitMango.
>
> Licensed under the Apache License, Version 2.0 (the "License");
> you may not use this codebase except in compliance with the License.
> You may obtain a copy of the License at
>
> http://www.apache.org/licenses/LICENSE-2.0
>
> Unless required by applicable law or agreed to in writing, software
> distributed under the License is distributed on an "AS IS" BASIS,
> WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
> See the License for the specific language governing permissions and
> limitations under the License.

---

```
(_______________()'`;
/,               /`
\\"-------------\\
```

---

<h6 align=center>Made with ❤️ at <a href="https://github.com/fitmango">🥭</a></h6>
