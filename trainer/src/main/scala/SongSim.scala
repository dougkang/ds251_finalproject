package ds251

import scala.util.Try
import scala.collection.mutable.ArrayBuffer

import org.apache.spark._
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
      val sc = new SparkContext(sparkConf)
      val sqlc = SQLContext.getOrCreate(sc)

      import sqlc.implicits._

      val inRDD = sc.textFile(cfg.input)
        .map { x => x.split(",") }
        .filter { _.length > 5 }
        // We only need the 7Digital id, so just use that as a key
        .map { x => (x(3), x.drop(5).map(_.toDouble)) }

      println(s"Found ${inRDD.count()} documents")
      inRDD.cache()

      val songRDD = inRDD.cartesian(inRDD)
        .map { case ((kx, vx), (ky, vy)) => 
          val dist = math.sqrt(
            vx.zip(vy)
              .map { case (x, y) => math.pow(x * y, 2.0) }
              .sum
          )
          (kx, (ky, dist))
        }

      songRDD.cache()
      println(s"Found ${songRDD.count()} combinations")

      println(s"Finding similar songs")

      val matchesRDD = songRDD
        .groupByKey
        .map { case (id, matches) =>
           val topMatches = matches
             .toList
             .sortBy { _._2 } 
             .take(10)
             .map { case (id, score) => s"$id|$score"  }

          id :: topMatches
        }

      matchesRDD
        .map { x => x.mkString(",") }
        .saveAsTextFile(cfg.output)
       
    case None =>
      System.exit(1)
  }
  
}
