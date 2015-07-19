name := "trainer"

version := "0.0.1"

scalaVersion := "2.10.4"

// additional libraries
libraryDependencies ++= Seq(
  "org.apache.spark" %% "spark-core" % "1.4.0" % "provided",
  "org.apache.spark" %% "spark-mllib" % "1.4.0" % "provided",
  "com.databricks" %% "spark-csv" % "1.1.0",
  "com.github.scopt" %% "scopt" % "3.3.0"
)
