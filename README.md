# Mel De Bot

<img src="https://travis-ci.org/ytturi/MortDeGana_Bot.svg?branch=master" alt="build:">

Mel de bot covers poll needs from a bot. It has 2 funcs by the moment and 1 todo:

DONE:

- Party Poll
- Mel gif

TODO: Spam prevention

## Party Poll

Makes the question: "Who is coming?". The user may add extra text befor sending the poll. The options are: 

- "Mel!", which is an afirmative answer. By default it will add the user as "MEL". 
  - More than one? Use the "Mel+1!" button.
  - Did you press it more than once? use the "Mel-1" to undo it or use the "Mel!" to go back to one.  
- "Moto!", which is a negative answer. This one also sends a motorbike crash gif from giphy.

_Usage:_

```
/poll [extra text]
```

>TODO: ADD a GIF showing usage

## Mel!

Just send a random GIF. It uses a 100 random seed with one of the following search words (decided randomly): "honey, party, smile, laugh, crash, fall, funny"

```
/mel
```

## TODO: Spam prevention

In order to avoid spam by other bot commands, repeated messages will be erased. Also warns the admins of this behaviour.


----

## Bot usage

```
Usage: meldebot [OPTIONS]

Options:
  -c, --config TEXT  Use config file
  -i, --init-config  Initialize config file
  -v, --verbose      Override verbosity level for the logger to INFO
  -d, --debug        Override verbosity level for the logger to DEBUG
  -t, --token TEXT   Set telegram token instead of using a config file
  --help             Show this message and exit.
```

### Installation

1. Clone from repo
2. Install as a package (`pip install .`)

### Tests

Integrity test: `python setup.py test`
Functionallity test:
```
pip install -r dev_requirements.txt
mamba spec/test_*
```
