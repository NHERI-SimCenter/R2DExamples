#!/bin/bash

# remove currrent zip files
rm *.zip

# Loop through each directory in the current directory
for dir in */; do
    # Remove trailing slash
    dir=${dir%/}
    
    # Check if it's a directory
    if [ -d "$dir" ]; then
        # Create a zip file with the same name as the directory
        zip -r "${dir}.zip" "$dir"
        echo "Zipped $dir"
    fi
done

echo "All folders in the current directory zipped successfully"
