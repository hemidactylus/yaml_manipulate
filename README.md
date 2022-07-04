# Yaml Manipulator

Take an input "base YAML", a set of prescriptions in the form `key=val`,
and generate a new modified YAML.

Supports key deletion, lists, objects, list-and-object arbitrary mixed nesting,
key deletion, unspecified indexing.

Useful e.g. to parse a bunch of command-line params to `docker run` and avoid
building custom parameter logic or mounting a volume just to provide a single
configuration yaml.

## Run tests

install `PyYAML` and `pytest` (see `requirements.txt`), then:
```
pytest
```

## Examples

the tests show the two main steps: parsing the prescriptions to a tree,
and applying this tree to the base YAML.

Keys set to the empty string will be removed from the result.

### Command-line example

See comment at the end of `yaml_manipulate.py`.

## To do

The final form of the entry-point script.

Check that dependencies are universal enough with various Python versions.

Check Python 2 compatibility (it may be needed as this is built for embedding in constrained environments).

Check if PyYAML should be packaged here.
