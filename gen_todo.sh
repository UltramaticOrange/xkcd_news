#!/bin/bash

TODO="TODO.txt"
echo > $TODO # empty out the file

ls *.py | while read "fname"
do
  echo "$fname:" >> $TODO
  cat "$fname" | grep -Eio '# ?TODO:?.+' >> $TODO
  echo -e "\n" >> $TODO
done
