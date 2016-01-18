#!/bin/sh

CMDNAME=`basename $0`
if [ $# -ne 1 ]; then
  echo "Usage: $CMDNAME number"
  exit 1
fi

i=0
start_time=`date +%s`
while [ $i -ne $1 ]
do
  i=`expr $i + 1`
  python GenerateText.py 1 > title.txt
  python GenerateText.py 20 > body.txt
  python post-hatena.py title.txt body.txt
done

end_time=`date +%s`
time=$((end_time - start_time))

echo $time
