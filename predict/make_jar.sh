wekapath="/usr/share/java/weka.jar"
scalapath="/usr/share/scala/lib/scala-library.jar"
temppath=`mktemp -d`
cp $scalapath $temppath 
cp $wekapath $temppath
scalac -cp $wekapath predict.scala
ttdir="${temppath}/tmp"
mkdir $ttdir
classfile=$(ls |grep class)
cp $classfile $ttdir 
d=$(pwd)
cd $ttdir
jar -xf ../scala-library.jar
jar -xf ../weka.jar
cd ..
jar -cf final.jar -C tmp .
cp final.jar $d
cd $d
rm $classfile
rm -R $temppath
#./test_scala.sh
