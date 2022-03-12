#!/bin/sh
#

ABSPATH=$(perl -MCwd=realpath -e "print realpath '$0'")
SCRIPTDIR=$(dirname "$ABSPATH")

java -Xms512m -Xmx1600m -jar $SCRIPTDIR/jars/Panoply.jar "$@"

