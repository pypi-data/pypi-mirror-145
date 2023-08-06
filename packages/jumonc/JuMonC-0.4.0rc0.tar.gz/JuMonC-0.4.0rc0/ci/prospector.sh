#!/bin/bash

# Create Log file
touch prospector_output.txt

# Create initial badge
anybadge -l Code\ Analysis -v Unknown -c gray -f prospector.svg

# Counter for errors
containsErrors=0

# Run Prospector
for directory in $( cat ci/src_directories.txt ); do
    echo Checking $directory
    prospector $directory --profile ci/prospector_profile.yaml >> prospector_output.txt 2>> prospector_err.txt
    if [[ $( cat prospector_err.txt | wc -l ) -gt 0 ]]
    then
        echo "Errors while running prospector!!!"
        cat prospector_err.txt
        exit 1
    fi

    tail -n 10 prospector_output.txt
    
    
    containsErrors=$(( ${containsErrors} + $( tail -n 2 prospector_output.txt | awk '{print $3}') ))
done

if [[ "$containsErrors" == "0" ]]; then
    echo "Prospector exited with 0 errors"
    
    # Create new Badge
	rm prospector.svg
    anybadge -l Code\ Analysis -v Success -c green -f prospector.svg
    
    exit 0
else
    echo "Prospector found errors in the code. You might want to check your code again"
    echo "Maybe take a look at prospector_output.txt"
    
    cat prospector_output.txt
    
    # Create new Badge
	rm prospector.svg
    anybadge -l Code\ Analysis -v Failed -c red -f prospector.svg
    
    exit 1
fi
