package ds251

import scala.util.Try
import scala.collection.mutable.ArrayBuffer

import org.apache.spark._
import org.apache.spark.storage._
import org.apache.spark.sql._
import org.apache.spark.mllib.clustering.KMeans
import org.apache.spark.mllib.linalg.{Vector, Vectors}

case class SongKMeansConfig(
  input: String = "",
  output: String = "",
  k: Int = 1000,
  iter: Int = 100
)

object SongKMeans extends App {

  // Create our argparser
  val parser = new scopt.OptionParser[SongKMeansConfig]("song-kmeans-scorer") {
    head("Song KMeans", "0.1")
    help("help") text("prints this usage text")
    arg[String]("<input>") required() action { (x, c) =>
      c.copy(input = x) } text("paths to input")
    arg[String]("<output>") required() action { (x, c) =>
      c.copy(output = x) } text("path to output")
    opt[Int]("k") optional() action { (x, c) =>
      c.copy(k = x) } text("k for kmeans")
    opt[Int]("n") optional() action { (x, c) =>
      c.copy(iter = x) } text("number of iterations for kmeans")
  }

  parser.parse(args, SongKMeansConfig()) match {
    case Some(cfg) =>
      // Create the Spark Context
      val sparkConf = new SparkConf()
        .set("spark.driver.maxResultSize", "10g")
      val sc = new SparkContext(sparkConf)
      val sqlc = SQLContext.getOrCreate(sc)

      import sqlc.implicits._

      val inRDD = sc.textFile(cfg.input)
        .map { x => x.split(",") }
        .filter { _.length > 5 }
        // We only need the 7Digital id, so just use that as a key
        .map { x => (x(3), Vectors.dense(x.drop(5).map(_.toDouble))) }

      inRDD.cache()

      val km = KMeans.train(inRDD.map(_._2), cfg.k, cfg.iter)

      inRDD
        .map { case (k, vs) => (km.predict(vs), k) }
        .groupByKey()
        .map { case (_, vs) => vs.mkString(",") }
        .saveAsTextFile(cfg.output)
            
    case None =>
      System.exit(1)
  }     
      
}
