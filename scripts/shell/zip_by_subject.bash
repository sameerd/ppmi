#!/bin/bash

# Zip up files by subject and remove the subject directory

set -x

# Execute this in the ./data_collection/PPMI directory

# Echo version
for dir in ./*/
do 
   dir=${dir%*/}
   echo "Processing $dir"
   tar cf - $dir | pigz --fast -p 8 > "${dir}".tar.gz && rm -r "$dir"
done
