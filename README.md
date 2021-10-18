# Mel De Bot

<img src="https://travis-ci.org/ytturi/MortDeGana_Bot.svg?branch=master" alt="build:">


## Commands available


### Party Poll

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


### Mel!

Just send a random GIF. It uses a 100 random seed with one of the following search words (decided randomly): "honey, party, smile, laugh, crash, fall, funny"

```
/mel
```


### Flute

Send a random YouTube video with a shitty flute cover.

```
/flute
```


### Haces cosas

Send a random text within the mosth famous phrases in the Mort de gana group.

```
/hacescosas
```


### Moto

Send a motorbike crash gif from giphy.

```
/moto
```


### Tu qui ets

Send a fine-tuned name of a random member of the Mort de gana group.

```
/tuquiets
```


### Did you mean?

Sends a _Did you mean?_ message replying to a message, properly fixing what the writer actually meant.

To use, reply to a message using:

```
/s <TEXT_FROM_ORIGINAL_MSG>/<TEXT_TO_BE_REPLACED_WITH>
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

Unittests: `python setup.py test`
