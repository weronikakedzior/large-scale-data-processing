from pyspark.sql import SparkSession, functions
from pyspark.ml.linalg import Vectors, VectorUDT
from models import linear_regression, binary_classification, multiclass_classification
from pyspark.sql.functions import udf
import os

spark = SparkSession.builder\
    .appName('appName')\
    .master('local')\
    .config("spark.mongodb.input.uri", os.environ['MONGO_URI']) \
    .config("spark.mongodb.input.database", os.environ['MONGO_DB'])\
    .config("spark.mongodb.input.collection", os.environ['MONGO_COLLECTION'])\
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.0")\
    .getOrCreate()

data = spark.read \
    .format("com.mongodb.spark.sql.DefaultSource") \
    .load()


def vectorize_udf(vectors):
    return Vectors.dense(vectors)
list_to_vector_udf = udf(lambda l: Vectors.dense(l), VectorUDT())
map_to_int = udf(lambda l: str(l))

#data = data.withColumn("post_text_em",  functions.flatten(data.post_text_em))
data = data.withColumn("post_text_em", functions.slice("post_text_em", start=1, length=300))
data = data.select(
    data["subreddit_name"],
    data['number_votes'],
    data['num_of_comments'],
    data['belongs_to_NSFW'],
    data['text_len'],
    map_to_int(data['belongs_to_NSFW']).alias("belongs_to_NSFW_index"),
    list_to_vector_udf(data["post_text_em"]).alias("text_embedding_vectorize")
)

# vec_size = udf(lambda l: len(l.toArray()), IntegerType())
# df = df.select(df['subreddit_name'], vec_size(df["post_embedding"]).alias("post_emb")).show()



spark.udf.register("vectorize_udf", vectorize_udf, VectorUDT())
training, test = data.randomSplit([0.8, 0.2])

#Linear regression
#rmse_test, rmse_train = linear_regression(training, test)
#print("Result linear regression")
#print(f"Linear regression rmse_test: {rmse_test}, train: {rmse_train}")

#Binary classification
#f1 = binary_classification(training, test)
#print("Result binary classification")
#print(f"Binary classification F1 Score: {f1}")

#Binary classification
f1 = multiclass_classification(training, test)
#print("Result multiclass classification")
#print(f"Multiclass classification F1 Score: {f1}")