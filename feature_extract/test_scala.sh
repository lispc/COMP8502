#scala -cp /usr/share/java/weka.jar validate_and_predict.scala test.arff weka.classifiers.bayes.NaiveBayes ""| tee scala.log
#java -cp .:/usr/share/java/weka.jar:/usr/share/scala/lib/scala-library.jar Test test.arff weka.classifiers.bayes.NaiveBayes ""| tee scala.log
java -cp ./final.jar Test test.arff weka.classifiers.bayes.NaiveBayes ""| tee scala.log
