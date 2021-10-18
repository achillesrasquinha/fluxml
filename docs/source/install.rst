.. _install:

### Installation

#### Installation via pip

The recommended way to install **fluxml** is via `pip`.

```shell
$ pip install fluxml
```

For instructions on installing python and pip see “The Hitchhiker’s Guide to Python” 
[Installation Guides](https://docs.python-guide.org/starting/installation/).

#### Building from source

`fluxml` is actively developed on [https://github.com](https://github.com/achillesrasquinha/fluxml)
and is always avaliable.

You can clone the base repository with git as follows:

```shell
$ git clone https://github.com/achillesrasquinha/fluxml
```

Optionally, you could download the tarball or zipball as follows:

##### For Linux Users

```shell
$ curl -OL https://github.com/achillesrasquinha/tarball/fluxml
```

##### For Windows Users

```shell
$ curl -OL https://github.com/achillesrasquinha/zipball/fluxml
```

Install necessary dependencies

```shell
$ cd fluxml
$ pip install -r requirements.txt
```

Then, go ahead and install fluxml in your site-packages as follows:

```shell
$ python setup.py install
```

Check to see if you’ve installed fluxml correctly.

```shell
$ fluxml --help
```