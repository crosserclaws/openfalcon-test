# openfalcon-test

Automated testing for Open-Falcon API in Python 3.

## Getting started

### PYTHONPATH
Add the path of */pyfalcon* into *PYTHONPATH*.
```bash
export PYTHONPATH=$PYTHONPATH:PATH_TO_OPENFALCON-TEST/pyfalcon
```

or

Use the *path.sh* when ***pwd*** is in */pyfalcon*

```bash
source ./path.sh
```

### Dependency library
Install dependencies through ***pip***.
```bash
pip install -r PATH_TO_OPENFALCON-TEST/pyfalcon/requirements.txt
```

### Config setting
Remember to set the ***host address*** of server and ***login account*** for testing in the **config.json** of each module directory.
```json
{
    "host": "10.20.30.40",
    "http": 1234,
    "api": {
        "authLogin": "/auth/login",
        "rootCreate": "/root",
        "teamCreate": "/me/team/c",
        "userCreate": "/me/user/c",
        "userDelete": "/target-user/delete",
        "userQuery": "/user/query"
    },
    "login": {
        "url": "http://10.20.30.40:1234/auth/login",
        "auth": {
            "name": "root",
            "password": "root"
        }
    }
}
```


## Usage examples
Simply run any test suite in module directory through python.
```bash
python3 fe_00.py
```

You could get more messages with cmd flag.
```bash
python3 fe_00.py -v
```

Help message.
```bash
python3 fe_00.py -h
```
