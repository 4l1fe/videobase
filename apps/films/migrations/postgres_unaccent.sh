#!/bin/bash

set -x

if [ -d /usr/share/postgresql/9.3/tsearch_data ]; then
    cd /usr/share/postgresql/9.3/tsearch_data

    if [ -f unaccent.rules ]; then
        echo "э	е" >> unaccent.rules
        echo "Э	Е" >> unaccent.rules

        service postgresql restart
    else
        echo "That file doesn't exists"
    fi
else
    echo "That directory doesn't exists"
fi
