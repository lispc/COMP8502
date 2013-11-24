

// Set the project name to the string 'My Project'
name := "Predictor"
 
// The := method used in Name and Version is one of two fundamental methods.
// The other method is <<=
// All other initialization methods are implemented in terms of these.
version := "0.0"
//Add Repository Path
//resolvers += "db4o-repo" at "http://source.db4o.com/maven"
// Add a single dependency
//libraryDependencies += "junit" % "junit" % "4.8" % "test"

resolvers += Resolver.url("sbt-plugin-releases",new URL("http://scalasbt.artifactoryonline.com/scalasbt/sbt-plugin-releases/"))(Resolver.ivyStylePatterns)

mainClass in oneJar := Some("Test")

libraryDependencies += "commons-lang" % "commons-lang" % "2.6"
//libraryDependencies += "com.db4o" % "db4o-full-java5" % "8.1-SNAPSHOT"

libraryDependencies += "nz.ac.waikato.cms.weka" % "weka-dev" % "3.7.5"
           
//libraryDependencies += "nz.ac.waikato.cms.weka" % "weka-stable" % "3.6.6"
// add compile dependencies on some dispatch modules
//libraryDependencies ++= Seq(
//  "com.github.scala-incubator.io" %% "core"             % "0.1.1",
//  "com.github.scala-incubator.io" %% "file"             % "0.1.1",
//  "org.jsoup"                     %  "jsoup"            % "1.6.1"
//)
 
//settings = settings ++ SbtOneJar.oneJarSettings 

// Use the project version to determine the repository to publish to.
//publishTo <<= version { (v: String) =>
//  if(v endsWith "-SNAPSHOT")
//    Some(ScalaToolsSnapshots)
//  else
//    Some(ScalaToolsReleases)
//}
seq(com.github.retronym.SbtOneJar.oneJarSettings: _*)
