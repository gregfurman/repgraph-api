# RepGraph-API

RepGraph-API serves as the web application server for the RepGraph DMRS graph visualisation software. 

## Create a virtualenv

In Linux, write the following into terminal:

```bash
python3.7 -m venv /path/to/new/virtual/environment
```

## Installation

Activate the virtual environemnt:

```bash
source venv/bin/activate
```

And install requirements:

```bash
pip install requirements.txt
```

## Usage

Run Unit Tests:
```bash
cd src

python -m unittest
```

Run Server:
```bash
python ./src/wsgi.py
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)