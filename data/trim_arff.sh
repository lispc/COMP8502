if [ "$#" -ne 1 ]; then
	echo "usage:"$0" <arff_file_name>"
fi
fname=`echo "$1"|cut -d'.' -f1`
newname="${fname}_trimmed.arff"
sed  "s|'.*',||" < "$1" > $newname
sed -i 3d $newname #remove string cos python.scipy.io.arff cannot handle it
