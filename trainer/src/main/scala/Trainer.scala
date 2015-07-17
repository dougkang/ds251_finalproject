package ds251

import org.apache.spark._
import org.apache.spark.mllib.feature.{HashingTF, PCA}

case class Config(
  input: String = "",
  output: String = "",
  k: Int = 100,
  delim: String = "\t"
)

object PCATrainer extends App {

  // Create our argparser
  val parser = new scopt.OptionParser[Config]("pca-trainer") {
    head("pca-trainer", "0.1")
    opt[Int]("k") optional() action { (x, c) =>
      c.copy(k = x) } text("value for k (default: 100)")
    opt[String]("delim") optional() action { (x, c) =>
      c.copy(delim = x) } text("value for input delimiter (default: \\t)")
    help("help") text("prints this usage text")
    arg[String]("<input>") required() action { (x, c) =>
      c.copy(input = x) } text("path to input")
    arg[String]("<output>") required() action { (x, c) =>
      c.copy(output = x) } text("path to output")
  }

  parser.parse(args, Config()) match {
    case Some(cfg) =>
      // Create the Spark Context
      val sparkConf = new SparkConf()
      val sc = new SparkContext(sparkConf)

      val in = sc.textFile(cfg.input)
        // Split the incoming string by delim.  We assume that the first row
        // is the id.
        .map { _.split(cfg.delim).toSeq } 
        .filter { _.length > 1 }

      val cnt = in.count()

      println(s"Found $cnt documents")

      // Extract the id column
      val ids = in.map { _.head }
      val feats = in.map { _.tail }

      // We compute TF.  Since each entry has at most one instance of each
      // word, we basically get a bitset.
      // 5000 was chosen because we have 3502 genres and it was large enough 
      val hashingTF = new HashingTF(5000)
      val tf = hashingTF.transform(feats)
      tf.cache()

      println(s"Found ${tf.first().size} features")
        
      // Run the tf vector through PCA to lower the dimensions
      val pca = new PCA(cfg.k).fit(tf)

      // Retrieve and store the principal components
      println(s"Outputting principal components...")
      val pcm = pca.pc
      val shape = (pcm.numRows, pcm.numCols)
      sc.makeRDD(pcm.toArray.grouped(pcm.numCols).toSeq)
        .map { _.mkString(",") }
        .saveAsTextFile(s"${cfg.output}/pcm")

      // Reduce dimensionality of our documents using the PCA model we
      // just trained and store the output
      println(s"Outputting results...")
      val out = pca.transform(tf)
      ids.zip(out)
        .map { case (id, vec) => (id +: vec.toArray.map { _.toString }).mkString(",") }
        .saveAsTextFile(s"${cfg.output}/out")
       
    case None =>
      System.exit(1)
  }
}
