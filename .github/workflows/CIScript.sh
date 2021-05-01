#!/bin/bash 

# Created by Stevan Gavrilovic, NHERI SimCenter, University of California, Berkeley

echo "::set-output name=some_output::My output ($1)"

echo "The current path in the shell is: " $PWD

cd .github/workflows

python3 fileSubmit.py


