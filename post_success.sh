#!/bin/bash
export EXIT=""
for python_file in $(ls *py)
   do 
	   echo $python_file
	   pylint $python_file || export EXIT="Failed: $EXIT $python_file"
	   echo $EXIT
done
if [ -z "$EXIT" ] ; then
   echo success
else
   echo $EXIT
   exit 1
fi   
