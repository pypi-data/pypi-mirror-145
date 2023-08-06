# Pokemon Stream Tools

To install:

`pip install pokemonStreamTools`

## Current Programs

### Shiny Odds
This program will produce plot and text files for OBS that show the current odds* to have encountered a shiny mon.

To run:
```
usage: shinyOdds [-h] [--nShinies [NSHINIES]] Encounters.txt Odds

Time to shiny Hunt.

positional arguments:
  Encounters.txt        The file location for the number of encounters
  Odds                  The odds to find a shiny (i.e. 1/4096)

optional arguments:
  -h, --help            show this help message and exit
  --nShinies [NSHINIES]
                        The number of shinies you're hunting for
```

This will produce 3 files: a plot of your current shiny odds, a text file that has your current odds, and a text file that has the number of encounters until you reach your next percentage milestone. 
These files are located in the same directory as Encounters.txt.

The Encounters.txt file will be processed with regex to get the first numeric sequence. 

*The proper phrasing is x% of people at N encounters have gotten a shiny. 

### Steam Ender
This program will auto end stream if Encounters.txt has not been updated in a certain time. 
Useful for when using automatic hunters and you do not want your stream to run hours after it is found. 

To run:
```

usage: streamEnder [-h] [--password [PASSWORD]] [--timeout [TIMEOUT]] [--EndStreamTime [ENDSTREAMTIME]]
                   [--EndStreamName ENDSTREAMNAME]
                   Encounters.txt OBS_IP PORT

Stream Ender.

positional arguments:
  Encounters.txt        The file location for the number of encounters
  OBS_IP                The IP of the OBS instance
  PORT                  The port for the OBS instance

optional arguments:
  -h, --help            show this help message and exit
  --password [PASSWORD]
                        The password for the OBS instance
  --timeout [TIMEOUT]   The time (in seconds) to start the "End Stream" screen
  --EndStreamTime [ENDSTREAMTIME]
                        The time (in seconds) to wait on the end screen
  --EndStreamName ENDSTREAMNAME
                        The name for the end stream scene

```

You must set up OBS in the way described [here](https://github.com/Elektordi/obs-websocket-py).


### Twitch Bot
A twitch bot for chat commands. 
Look at the README in the twitch bot folder for more details.