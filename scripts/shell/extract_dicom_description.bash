#!/bin/bash

if [ -z "$1" ]; then 
    echo "No argument supplied"
    exit 1
fi

python -c 'import sys;from lxml import etree; root=etree.parse(sys.argv[1]);print(root.findtext(".//imagingProtocol/description"))' "$1"
