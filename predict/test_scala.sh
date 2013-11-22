sbt one-jar
java -jar target/scala-2.10/predictor_2.10-0.0-one-jar.jar ../data/training.arff ../data/test.arff weka.classifiers.functions.SMO "-C 1.0 -L 0.001 -P 1.0E-12 -N 0 -V -1 -W 1 -K \"weka.classifiers.functions.supportVector.PolyKernel -C 250007 -E 1.0\""
