#!/bin/bash
export EXIT=0
for python_file in $(ls *py)
   do 
	   echo $python_file
	   pylint $python_file || export EXIT=1
done
echo $EXIT
exit $EXIT    
