# Import the required modules and classes
import sparknlp
from sparknlp.base import DocumentAssembler
from sparknlp.annotator import MultiDateMatcher
from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
import pyspark.sql.functions as F
from pyspark.sql.types import StringType, StructType, StructField


def shit_parse_nlp(text):
    try:
        # Start Spark Session
        spark = sparknlp.start()

        # Define the schema for the DataFrame
        schema = StructType([StructField("text", StringType(), True)])

        # Create a DataFrame with sample text data
        spark_df = spark.createDataFrame([[text]], schema)

        # Define the DocumentAssembler
        document_assembler = (
            DocumentAssembler()
            .setInputCol("text")
            .setOutputCol("document")
        )

        # Define the MultiDateMatcher
        multiDate = (
            MultiDateMatcher()
            .setInputCols("document")
            .setOutputCol("multi_date")
            .setOutputFormat("dd/MM/yyyy")
            .setSourceLanguage("de")
        )

        # Create the Pipeline
        nlpPipeline = Pipeline(stages=[document_assembler, multiDate])

        # Fit the pipeline to the DataFrame
        model = nlpPipeline.fit(spark_df)

        # Transform the DataFrame using the fitted pipeline model
        result = model.transform(spark_df)

        # Extract the raw date from the `multi_date` column
        date_df = result.withColumn("date", F.explode(F.col("multi_date.result")))

        # Collect the date from the DataFrame
        dates = date_df.select("date").collect()

        # Extract the date as a list of strings
        date_list = [date_row.date for date_row in dates]

        return date_list

    except Exception as e:
        print(f"Error occurred: {e}")
        raise


# Example usage
if __name__ == "__main__":
    text = "askdjg aslökdjg aölserjk ga lkas 10.Mrz 2023 asdf as "
    dates = shit_parse_nlp(text)
    print(dates)
