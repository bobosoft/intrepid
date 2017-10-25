#!/bin/bash

if [[ $# -ne 1 ]]
then
    echo "Usage: $0 <inputfile>"
    exit
fi

echo "Creating Parser"
java org.antlr.v4.Tool ST.g4 -visitor -no-listener
echo "Compiling Java classes"
javac ST*.java
echo "Parsing and viewing"
cat $1 | java org.antlr.v4.gui.TestRig ST pou_decl -gui
echo "Cleaning"
rm *.class *.java
echo "Making parser"
./make_parser.sh
