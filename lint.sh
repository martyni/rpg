#!/bin/bash
export EXIT=""
for python_file in $(ls *py)
   do 
	   echo $python_file
	   pylint $python_file || export EXIT=" $EXIT $python_file"
done
if [ -z "$EXIT" ] ; then
   echo success
else
   echo "Failed : " $EXIT
   exit 1
fi   
