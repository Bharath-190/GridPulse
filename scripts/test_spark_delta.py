from importlib.metadata import version
from pathlib import Path
from tempfile import TemporaryDirectory

from delta import configure_spark_with_delta_pip
from pyspark.sql import SparkSession


def main():
    print("PySpark:", version("pyspark"))
    print("Delta Lake:", version("delta-spark"))

    builder = (
        SparkSession.builder
        .appName("GridPulse-Delta-Smoke-Test")
        .master("local[2]")
        .config("spark.driver.host", "127.0.0.1")
        .config("spark.driver.bindAddress", "127.0.0.1")
        .config("spark.sql.shuffle.partitions", "2")
        .config(
            "spark.sql.extensions",
            "io.delta.sql.DeltaSparkSessionExtension"
        )
        .config(
            "spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog"
        )
    )

    spark = None

    try:
        spark = (
            configure_spark_with_delta_pip(builder)
            .getOrCreate()
        )

        spark.sparkContext.setLogLevel("WARN")

        print("\nSpark version:", spark.version)

        data = [
            (1, "Solar Alpha", 125.5),
            (2, "Solar Beta", 98.2),
            (3, "Solar Gamma", 143.8),
        ]

        df = spark.createDataFrame(
            data,
            ["plant_id", "plant_name", "generation_kwh"]
        )

        with TemporaryDirectory(prefix="gridpulse_delta_") as tmp:
            delta_path = str(Path(tmp) / "delta_table")

            print("\nWriting Delta table...")
            df.write.format("delta").mode("overwrite").save(delta_path)

            print("Reading Delta table...")
            result = (
                spark.read.format("delta")
                .load(delta_path)
                .orderBy("plant_id")
            )

            records = result.collect()

            assert len(records) == 3
            assert records[0]["plant_name"] == "Solar Alpha"
            assert abs(records[2]["generation_kwh"] - 143.8) < 1e-9

            print("\nDelta table schema:")
            result.printSchema()

            print("Delta table records:")
            result.show(truncate=False)

            print("SUCCESS: Delta write and read verified!")

    finally:
        if spark is not None:
            spark.stop()


if __name__ == "__main__":
    main()
