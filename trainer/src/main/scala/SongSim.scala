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
        // We only need the 7Digital id, so just use that as a key
        .map { x => (x(1).toInt, (x(0).toInt, x.drop(2).map(_.toDouble))) }

      inRDD.persist(StorageLevel.MEMORY_AND_DISK_SER)

      inRDD.groupByKey()
        .map { case (group, vs) => 
          val ls = vs.toList
          if (ls.length <= 10) (-1, ls)
          else (group, ls)
        }
        .reduceByKey { case (acc, vs) => acc ++ vs }
        .flatMap { case (group, vs) =>
          vs.map { case (kx, vx) =>
            val top = vs.map { case (ky, vy) =>
              val dist = math.sqrt(
                vx.zip(vy)
                  .map { case (x, y) => math.pow(x-y, 2.0) }
                  .sum)
              (ky, dist)
            }.sortBy(_._2).take(100)
            s"""$kx,${top.map(_._1).mkString(",")}"""
          }
        }
        .saveAsTextFile(cfg.output)
            
    case None =>
      System.exit(1)
  }     
      
}
