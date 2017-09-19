
FREEPLAYCFG="/boot/freeplaycfg.txt"

if [ -f $FREEPLAYCFG ]
then
  source $FREEPLAYCFG
  if [[ "$FREEPLAYSTARTUP" == "RUNPY" && -n "$STARTUPPY" ]]
  then
    echo "Starting python "$STARTUPCMD
    python $STARTUPPY
    exit 0
  elif [[ "$FREEPLAYSTARTUP" == "RUNCMD" && -n "$STARTUPCMD" ]]
  then
    echo "Starting "$STARTUPCMD
    $STARTUPCMD
    exit 0
  elif [ "$FREEPLAYSTARTUP" == "CMDLINE" ]
  then
    echo "Starting up shell command prompt"
    exit 0
  elif [ "$FREEPLAYSTARTUP" == "EMULATIONSTATION" ]
  then
    echo "Starting EmulationStation"
  else
    echo "Unknown FREEPLAYSTARTUP "$FREEPLAYSTARTUP
  fi
else
  echo "File not found "$FREEPLAYCFG
fi

emulationstation #auto