package ds251

import scala.util.Try
import scala.collection.mutable.ArrayBuffer

import org.apache.spark._
import org.apache.spark.storage._
import org.apache.spark.sql._
import org.apache.spark.mllib.feature.PCA
import org.apache.spark.mllib.linalg.{Vector, Vectors}

case class SongSimConfig(
  input: String = "",
  output: String = ""
)

object SongSim extends App {

  // Create our argparser
  val parser = new scopt.OptionParser[SongSimConfig]("song-sim-scorer") {
    head("Song Similarity Scorder", "0.1")
    help("help") text("prints this usage text")
    arg[String]("<input>") required() action { (x, c) =>
      c.copy(input = x) } text("paths to input")
    arg[String]("<output>") required() action { (x, c) =>
      c.copy(output = x) } text("path to output")
  }

  parser.parse(args, SongSimConfig()) match {
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
        .map { x => (x(3), x.drop(5).map(_.toDouble)) }

      inRDD.persist(StorageLevel.MEMORY_AND_DISK_SER)

      inRDD.cartesian(inRDD)
        .map { case ((kx, vx), (ky, vy)) => (kx, (vx, ky, vy)) }
        .aggregateByKey(Array.empty[(String, Double)])(
          { case (acc, (vx, ky, vy)) =>
            val dist = math.sqrt(
              vx.zip(vy)
                .map { case (x, y) => math.pow(x - y, 2.0) }
                .sum)
            Array((ky, dist))
          },      
          { case (x, y) => (x ++ y).sortBy(_._2).take(100) }
         )      
        .map { case (k, vs) => s"""$k,${vs.map(_._1).mkString(",")}""" }
        .saveAsTextFile(cfg.output)
            
    case None =>
      System.exit(1)
  }     
      
}
