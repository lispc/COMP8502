import java.io.BufferedReader
import java.io.FileReader
import java.util.Random
import weka.filters.Filter
import weka.filters.unsupervised.attribute.Remove
import weka.core.Instances
import weka.classifiers.trees.J48
import weka.classifiers.bayes.NaiveBayes
import weka.classifiers.Evaluation
import weka.core.Utils
object Test{
	def main(args: Array[String]) {
	var prefix = "-t ./training_trimmed.arff -c 1 -o "
	var schemes = Array(
		Array("weka.classifiers.bayes.NaiveBayes",""),
		Array("weka.classifiers.bayes.NaiveBayes","-K"),
		Array("weka.classifiers.bayes.NaiveBayes","-D"),
		Array("weka.classifiers.trees.J48","-C 0.25 -M 2"),
		Array("weka.classifiers.meta.AdaBoostM1","-P 100 -S 1 -I 10 -W weka.classifiers.trees.DecisionStump"),
		Array("weka.classifiers.meta.LogitBoost","-P 100 -F 0 -R 1 -L -1.7976931348623157E308 -H 1.0 -S 1 -I 10 -W weka.classifiers.trees.DecisionStump")
			)
	for(s <- schemes)
	{
		var options = Utils.splitOptions(prefix+s(1))
		println(Evaluation.evaluateModel(s(0),options))
	}



	/*
	var reader = new BufferedReader(new FileReader("training_r2.arff"))
	var data = new Instances(reader)
	reader.close()
	data.setClassIndex(0)
	var remove = new Remove()
	remove.setOptions(Array("-R","2"))
	remove.setInputFormat(data)
	var newData = Filter.useFilter(data,remove)
//get data
	var eval = new Evaluation(newData)
	var bayes = new NaiveBayes()
	eval.crossValidateModel(bayes,newData,10,new Random(1))
	println(eval.toSummaryString)
	*/
/*
	var random = new Random(0)
	newData.randomize(random)
	var folds = 10 
	newData.stratify(folds)
	for(i <- 1 to folds-1)
	{
		var train = newData.trainCV(folds,i)
		var test = newData.trainCV(folds,i)
		var bayes = new NaiveBayes()
		bayes.buildClassifier(train)
	}
*/
	}
}
