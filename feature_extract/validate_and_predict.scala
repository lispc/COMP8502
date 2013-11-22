import java.io.BufferedReader
import java.io.FileReader
import java.util.Random
import weka.filters.Filter
import weka.filters.unsupervised.attribute.Remove
import weka.core.Instances
import weka.classifiers.AbstractClassifier
import weka.classifiers.trees.J48
import weka.classifiers.bayes.NaiveBayes
import weka.classifiers.Evaluation
import weka.core.Utils
object Test{
	def getData(fname: String = "training.arff"): Instances = 
	{
	var reader = new BufferedReader(new FileReader(fname))
	var data = new Instances(reader)
	reader.close()
	data.setClassIndex(0)
	var remove = new Remove()
	remove.setOptions(Array("-R","2"))
	remove.setInputFormat(data)
	var newData = Filter.useFilter(data,remove)
	return newData
	}
	def getSchemes(): Array[Array[String]] = 
	{
		var schemes = Array(
		Array("weka.classifiers.bayes.NaiveBayes",""),
		Array("weka.classifiers.bayes.NaiveBayes","-K"),
		Array("weka.classifiers.bayes.NaiveBayes","-D"),
		Array("weka.classifiers.trees.J48","-C 0.25 -M 2"),
		Array("weka.classifiers.meta.AdaBoostM1","-P 100 -S 1 -I 10 -W weka.classifiers.trees.DecisionStump"),
		Array("weka.classifiers.meta.LogitBoost","-P 100 -F 0 -R 1 -L -1.7976931348623157E308 -H 1.0 -S 1 -I 10 -W weka.classifiers.trees.DecisionStump"))
		return schemes
	}
	def testOnce(fname: String, methodIndex: Int = 0)
	{
		var testData = getData(fname)
		var schemes = getSchemes()
		var scheme = schemes(methodIndex)
		var cls = AbstractClassifier.forName(scheme(0),Utils.splitOptions(scheme(1)))
		cls.buildClassifier(getData())
		var i = 0
		while(i<testData.numInstances())
		{
			println(cls.distributionForInstance(testData.instance(i)).mkString(" "))
			//var ins = testData.instance(i)
			//var res = cls.classifyInstance(ins)
			//var res = cls.dis
			//println(res)
			//println(cls.classifyInstance(testData.instance(i)))
			i=i+1
		}
	}
	def validateModel(){
	var prefix = "-t ./training_trimmed.arff -c 1 -o "
	var data = getData()
	var schemes = getSchemes()
	for(s <- schemes)
	{
		println("validating using model "+s(0)+" and with option "+s(1))
		var options = Utils.splitOptions(s(1))
		//println(Evaluation.evaluateModel(s(0),options))
		var eval = new Evaluation(data)
		var t0 = System.nanoTime()
		var cls = AbstractClassifier.forName(s(0),options)
		eval.crossValidateModel(cls,data,10,new Random(1))
		var t = (System.nanoTime()-t0)/Math.pow(10,9)
		println("Stat:")
		println(eval.toMatrixString())
		println(s"Time: $t s")
	}
	}
	def main(args: Array[String])
	{
		//var schemes = getSchemes().zipWithIndex
		for (i <- 0 until getSchemes().length)
		{
			println("predicting with "+(getSchemes()(i)(0)))
			testOnce("test.arff",i)
		}
	}


	/*
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
