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

There are two proposals for command-line interaction,
both wrapping the same "core engine", so to speak.

#### Files as parameters

Here the syntax is:
```
python yaml_manipulate [src_yaml] [prescription_file] [out_file_must_not_exist]
```

i.e. (once directory `out` is created):
```
python yaml_manipulate.py example/src1.yaml example/prescr1.txt out/out1.yaml
```

#### Params and stdout

Input "source" yaml and then all of the key-value pairs to the command line,
result to STDOUT.

Syntax is:
```
python yaml_manipulate2 SOURCE_YAML.yaml KEY1=VALUE1 KEY2=VALUE2 KEY3=VALUE3 ...
```

Example:
```
python yaml_manipulate2.py example/src1.yaml  \
  keyA=123                                    \
  keyP.keyQ.keyR=False                        \
  listA.[0]=mmm                               \
  listA.[1]=nnn                               \
  objlistA.[0].x=ics                          \
  objlistA.[0].y=ipsilon                      \
  objlistB.[]=bah                             \
  objlistB.[]=beh                             \
  objlistB.[]=bih                             \
  objsublistA.[0].[]=item1                    \
  objsublistA.[0].[]=item2                    \
  objsublistB.[0].attr.[]=item1               \
  objsublistB.[0].attr.[]=item2               \
  sublistA.subkey.[]=1119                     \
  sublistA.subkey.[]=1121.1211                \
  deleted1=                                   \
  deleted2.subdeleted=                        \
  > out/out2.yaml
```

## To do

The final form of the entry-point script.

Check that dependencies are universal enough with various Python versions.

Check Python 2 compatibility (it may be needed as this is built for embedding in constrained environments).

Check if PyYAML should be packaged here.

## Prescriptions

- Value types are guessed.
- Using `[]` means "next item in this list".
- Dot notation is used, e.g. `key.subkey.[2].subsubkey=value`.
- Nothing after the `=` means key deletion.

Example: given the following list of prescriptions (amenable to be command-line parameters),
```
keyA=123
keyP.keyQ.keyR=False
listA.[0]=mmm
listA.[1]=nnn
objlistA.[0].x=ics
objlistA.[0].y=ipsilon
objlistB.[]=bah
objlistB.[]=beh
objlistB.[]=bih
objsublistA.[0].[]=item1
objsublistA.[0].[]=item2
objsublistB.[0].attr.[]=item1
objsublistB.[0].attr.[]=item2
sublistA.subkey.[]=1119
sublistA.subkey.[]=1121.1211
deleted1=
deleted2.subdeleted=
```

the following tree is produced (note the value types):
```
deleted1: null
deleted2:
  subdeleted: null
keyA: 123
keyP:
  keyQ:
    keyR: false
listA:
- mmm
- nnn
objlistA:
- x: ics
  y: ipsilon
objlistB:
- bah
- beh
- bih
objsublistA:
- - item1
  - item2
objsublistB:
- attr:
  - item1
  - item2
sublistA:
  subkey:
  - 1119
  - 1121.1211
```

which is then merged onto a "default tree". Finally, null values are pruned away to generate the final result.
