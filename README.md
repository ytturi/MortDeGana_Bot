> WIP: This bot is on WIP and does not even have a 0.X version. :persevere:

# Mel De Bot

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
