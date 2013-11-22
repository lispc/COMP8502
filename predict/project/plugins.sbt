resolvers += Resolver.url(
  "sbt-plugin-releases", 
    new URL("http://scalasbt.artifactoryonline.com/scalasbt/sbt-plugin-releases/")
)(Resolver.ivyStylePatterns)

addSbtPlugin("com.github.retronym" % "sbt-onejar" % "0.7")

addSbtPlugin("org.scala-sbt.plugins" % "sbt-onejar" % "0.8")
