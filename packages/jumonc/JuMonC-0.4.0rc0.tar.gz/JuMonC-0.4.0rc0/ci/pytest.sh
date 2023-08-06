#!/bin/bash

# Create Log file
touch pytest_output.txt

# Create initial badge
anybadge -l Unit\ Testing -v Unknown -c gray -f pytest.svg

# Counter for errors
containsErrors=0
pytestFailed=0


export PYTHONPATH=${PYTHONPATH}:$( awk '{print $1}' ci/src_directories.txt | paste -s -d: - )
# Run Pytest
for directory in $( cat ci/test_directories.txt ); do
    echo Checking $directory
    pytest $directory --disable-warnings >> pytest_output.txt
	
	containsErrors=$?
    echo "Pytest in $directory exited with code $containsErrors"
    echo $( cat pytest_output.txt | tail -1)
	
	if [[ $containsErrors != 0 ]]; then
        pytestFailed=1
    fi
done

if [[ $pytestFailed == 0 ]]; then
    echo "Pytest exited with 0 errors"
    
    # Create new Badge
	rm pytest.svg
    anybadge -l Unit\ Testing -v Success -c green -f pytest.svg
    
    exit 0
else
    echo "Pytest found errors in the code. You might want to check your code again"
    echo "Maybe take a look at pytest_output.txt"
    
    cat pytest_output.txt
    
    # Create new Badge
	rm pytest.svg
    anybadge -l Unit\ Testing -v Failed -c red -f pytest.svg
    
    exit 1
fi
