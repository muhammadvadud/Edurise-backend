file=/tmp/db-$(/usr/bin/date +\%Y-%m-%d-%H:%M:%S).sqlite3
cp db.sqlite3 $file
mc cp $file b2/edusystem-database
rm $file
