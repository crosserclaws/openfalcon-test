# Pyfalcon
Automated testing for Open-Falcon API in Python3.

## Environment setup

### Prerequisite
Need [pip3](https://github.com/pypa/pip) and dependent packages in *requirement.txt*.

    $ pip3 install -r requirements.txt

### Configuration
Configurations are under **config/** dir, remember to set the **host address** of each components.

Specially, *global.json* recordes the info used for getting login session.
```json
{
    "login": {
        "url": "http://10.0.0.104:1234/auth/login",
        "auth": {
            "name": "login_user",
            "password": "example_password"
        }
    }
}
```

## Getting started

Simply exectute [pytest](https://github.com/pytest-dev/pytest) under project's root (i.e. **pyfalcon/**). Note that the name of the test should follow the [rules](https://pytest.org/latest/goodpractices.html#conventions-for-python-test-discovery).

* `$ py.test`: Recursively discover and run tests within ***pwd***.
* `$ py.test fe hbs`: Recursively discover and run tests within **fe/** and **hbs/** dir.
* `$ py.test fe/test_fe_001.py hbs/test_hbs_001.py`: Discover and run tests within given files.

### Frequently used options

* `-h`: Helping messages including custom options of pytest.
* `-s`: Disable capturing mode that messages are allowed to show on the screen.
* `-v`: Show more info and set the logging level into DEBUG level.
* `--dev`: Use the value in *dev.json* to override the value in each module with same key.
* `--tb=no`: Don't print traceback.

Show logging messages:

    $ py.test -vs

Use *filter.py* for concise output.

    $ py.test --tb=no | ./filter.py

With `--dev`, *dev.json* may be useful if all components are on the same machine.
```json
{
    "host": "10.20.30.40",
    "login": {
        "url": "http://10.20.30.40:1234/auth/login",
        "auth": {
            "name": "root",
            "password": "root"
        }
    }
}
```

## Documentation
Docs are auto-generated from docstrings within files by [Sphinx](http://www.sphinx-doc.org/en/stable/).

### Build and get docs
Under **doc/** dir, use *Makefile* to generate html docs.

    $ make html

Then, open ***doc/_build/html/index.html*** in the browser.

### Add new test into docs
Update new test's path into ***doc/index.rst*** then rebuild it. Take ***fe/test_fe_999*** as an example:

```rst
Welcome to pyfalcon's documentation!
====================================

Contents:

.. autosummary::
   :toctree: DIRNAME

   alarm.test_alarm_001
   fe.test_fe_001
   fe.test_fe_002
   fe.test_fe_999
   hbs.test_hbs_001
```
