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
	def getData(fname:String): Instances = 
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
	def testOnce(train_name: String, test_name:String, clsname: String, optionstr: String)
	{
		var testData = getData(test_name)
		var cls = AbstractClassifier.forName(clsname,Utils.splitOptions(optionstr))
		cls.buildClassifier(getData(train_name))
		var i = 0
		while(i<testData.numInstances())
		{
			var res = cls.classifyInstance(testData.instance(i))
			if(Math.abs(res-1.0)<=0.0001)
			{
				println("False")
			}
			else
			{
				println("True")
			}
			i=i+1
		}

	}
	def main(args: Array[String])
	{
		if(args.length!=4)
		{
			println("args length should be four")
			exit(1)
		}
		var train_name = args(0)
		var test_name = args(1)
		var clsname = args(2)
		var optionstr = args(3)
		testOnce(train_name,test_name,clsname,optionstr)
	}

}
