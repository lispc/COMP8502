#scala -cp /usr/share/java/weka.jar validate_and_predict.scala test.arff weka.classifiers.bayes.NaiveBayes ""| tee scala.log
#java -cp .:/usr/share/java/weka.jar:/usr/share/scala/lib/scala-library.jar Test test.arff weka.classifiers.bayes.NaiveBayes ""| tee scala.log
#java -cp ./final.jar Test ../data/test.arff weka.classifiers.bayes.NaiveBayes ""| tee scala.log
java -cp final.jar Test ../data/test.arff weka.classifiers.functions.SMO "-C 1.0 -L 0.001 -P 1.0E-12 -N 0 -V -1 -W 1 -K \"weka.classifiers.functions.supportVector.PolyKernel -C 250007 -E 1.0\""
