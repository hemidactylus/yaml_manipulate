PRESCR_BLOB_1 = '''keyA=123
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
deleted2.subdeleted='''

PRESCR_RESULT_TREE_JSON_1 = '''{
  "deleted1": null,
  "deleted2": {
    "subdeleted": null
  },
  "keyA": 123,
  "keyP": {
    "keyQ": {
      "keyR": false
    }
  },
  "listA": [
    "mmm",
    "nnn"
  ],
  "objlistA": [
    {
      "x": "ics",
      "y": "ipsilon"
    }
  ],
  "objlistB": [
    "bah",
    "beh",
    "bih"
  ],
  "objsublistA": [
    [
      "item1",
      "item2"
    ]
  ],
  "objsublistB": [
    {
      "attr": [
        "item1",
        "item2"
      ]
    }
  ],
  "sublistA": {
    "subkey": [
      1119,
      1121.1211
    ]
  }
}
'''

SRC_YAML_1 = '''deleted1: this_goes_away
deleted2:
  subdeleted: this_also_goes_away
keyA: 999
keyP:
  keyQ:
    keyR: true
listA:
- zzz
- www
objlistA:
- x: zcs
  y: zpsilon
objlistB:
- Zbah
- Zbeh
- Zbih
objsublistA:
- - Ztem1
  - Ztem2
objsublistB:
- attr:
  - Ztem1
  - Ztem2
sublistA:
  subkey:
  - 9999
  - 9999.9
untouched: ZYeah
unharmed:
  subuntouched: 9
unscathedlist:
- zbim
- zbam
- zboom
'''

RESULT_YAML_1 = '''keyA: 123
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
unharmed:
  subuntouched: 9
unscathedlist:
- zbim
- zbam
- zboom
untouched: ZYeah
'''