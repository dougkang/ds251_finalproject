package ds251

import scala.util.Try
import scala.collection.mutable.ArrayBuffer

import org.apache.spark._
import org.apache.spark.sql._
import org.apache.spark.mllib.feature.PCA
import org.apache.spark.mllib.linalg.{Vector, Vectors}

case class SongPCAConfig(
  inputs: Seq[String] = Seq.empty,
  output: String = "",
  loudnessKeypoints: Int = 100,
  pitchesKeypoints: Int = 100,
  timbreKeypoints: Int = 100,
  k: Int = 100,
  delim: String = "",
  subDelim: String = "",
  subSubDelim: String = ""
)

case class Song(
  artistId: String,
  artistMbId: String,
  songId: String,
  track7DigitalId: String,
  trackId: String,
  features: Vector
) {
  lazy val toCSV: String = 
    s"$artistId,$artistMbId,$songId,$track7DigitalId,$trackId,${features.toArray.mkString(",")}"
}

object Util {

  def interpolate(xs: Array[(Double, Double)], numKeypoints: Int): Array[Double] = {
    var xsSorted = xs.sortBy { case (t, v) => t }
    val (xStart, _) = xsSorted.head
    val (xEnd, _) = xsSorted.last
    val duration = xEnd - xStart
    val period = duration / numKeypoints
    val keypoints = (xStart to xEnd by period).toArray

    val res = new ArrayBuffer[Double](numKeypoints)
    var currXs = 1
    var currKp = 0
    while(currXs < xsSorted.length && currKp < keypoints.length) {
      val (x1, y1) = xsSorted(currXs)
      val (x2, y2) = xsSorted(currXs-1)

      while(currKp < keypoints.length && keypoints(currKp) < x2) {
        val x = keypoints(currKp)
        val m = (y2 - y1) / (x2 - x1)
        res += m * x + x1
        currKp = currKp + 1
      }
      currXs = currXs + 1
    }

    while(currKp < numKeypoints) {
      res += 0.0
      currKp = currKp + 1
    }

    res.toArray
  }

  def interpolate(xs: Array[(Double, Array[Double])], numDim: Int, numKeypoints: Int): Array[Double] = {
    (0 until numDim).toArray
      .foldLeft(Array.empty[Double]) { (acc, i) => 
        acc ++ interpolate(xs.map { case (t, vs) => (t, vs(i)) }, numKeypoints) 
      }
  }

  def parseOpt(line: String, cfg: SongPCAConfig): Option[Song] = {
    line.split(cfg.delim).toList match {
      case _ :: artistId :: artistMbId :: _ :: songId :: track7DigitalId :: trackId :: year :: danceability ::
           duration :: energy :: key :: avgLoudness :: mode :: _ :: segmentsStart :: segmentsLoudnessMax :: 
           segmentsPitches :: segmentsTimbre :: tempo :: timeSignature :: Nil => Option {

        val starts = segmentsStart.split(cfg.subDelim).map { _.toDouble }
        val loudness = segmentsLoudnessMax.split(cfg.subDelim).map { _.toDouble }
        val pitches = segmentsPitches.split(cfg.subDelim).map { _.split(cfg.subSubDelim).map { _.toDouble } }
        val timbres = segmentsTimbre.split(cfg.subDelim).map { _.split(cfg.subSubDelim).map { _.toDouble } }

        val features = Array[Double](
          year.toDouble,
          danceability.toDouble,
          duration.toDouble,
          energy.toDouble,
          key.toDouble,
          avgLoudness.toDouble,
          mode.toDouble,
          tempo.toDouble,
          timeSignature.toDouble
        ) ++
          interpolate(starts.zip(loudness), cfg.loudnessKeypoints) ++
          interpolate(starts.zip(pitches), 12, cfg.pitchesKeypoints) ++
          interpolate(starts.zip(timbres), 12, cfg.timbreKeypoints)

        Song(
          artistId = artistId.trim(),
          artistMbId = artistMbId.trim(),
          songId = songId.trim(),
          track7DigitalId = track7DigitalId.trim(),
          trackId = trackId.trim(),
          features = Vectors.dense(features)
        )
      }
      case x => 
        println(s"ERROR: expecting 21 fields, got ${x.length}")
        None
    }
      
  }
}

object SongPCA extends App {

  // Create our argparser
  val parser = new scopt.OptionParser[SongPCAConfig]("song-pca-trainer") {
    head("Song PCA Trainer", "0.1")
    opt[Int]("k") optional() action { (x, c) =>
      c.copy(k = x) } text("value for k (default: 100)")
    opt[Int]("lkp") optional() action { (x, c) =>
      c.copy(loudnessKeypoints = x) } text("value for loudness keypoints (default: 10)")
    opt[Int]("pkp") optional() action { (x, c) =>
      c.copy(pitchesKeypoints = x) } text("value for pitches keypoints (default: 10)")
    opt[Int]("tkp") optional() action { (x, c) =>
      c.copy(timbreKeypoints = x) } text("value for timber keypoints (default: 10)")
    help("help") text("prints this usage text")
    arg[Seq[String]]("<input>") required() action { (x, c) =>
      c.copy(inputs = x) } text("paths to input")
    arg[String]("<output>") required() action { (x, c) =>
      c.copy(output = x) } text("path to output")
  }

  parser.parse(args, SongPCAConfig()) match {
    case Some(cfg) =>
      // Create the Spark Context
      val sparkConf = new SparkConf()
      val sc = new SparkContext(sparkConf)
      val sqlc = SQLContext.getOrCreate(sc)

      import sqlc.implicits._

      val inRDD = sc.union(cfg.inputs.map { x => sc.textFile(x) })

      println(s"Found ${inRDD.count()} documents")

      val songRDD = inRDD.flatMap { x => Util.parseOpt(x, cfg) }

      println(s"Found ${songRDD.count()} valid documents")
      
      // Run the tf vector through PCA to lower the dimensions
      val pca = new PCA(cfg.k).fit(songRDD.map { _.features } )

      println(s"Applying PCA transform")

      songRDD
        .map { x => x.copy(features = pca.transform(x.features)).toCSV }
        .saveAsTextFile(cfg.output)
       
    case None =>
      System.exit(1)
  }
  
}
