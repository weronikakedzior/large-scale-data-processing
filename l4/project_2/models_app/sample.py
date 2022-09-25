from pyspark.sql import SparkSession
from pyspark.ml.linalg import Vectors, VectorUDT
from models import linear_regression, binary_classification, multiclass_classification
import os

spark = SparkSession.builder\
    .appName('appName')\
    .master('local')\
    .config("spark.mongodb.input.uri", os.environ['MONGO_URI']) \
    .config("spark.mongodb.input.database", os.environ['MONGO_DB'])\
    .config("spark.mongodb.input.collection", os.environ['MONGO_COLLECTION'])\
    .getOrCreate()

data = spark.read \
    .format("com.mongodb.spark.sql.DefaultSource") \
    .load()


def vectorize_udf(vectors):
    return Vectors.dense(vectors)


spark.udf.register("vectorize_udf", vectorize_udf, VectorUDT())
training, test = data.randomSplit([0.8, 0.2])

#Linear regression
rmse_test, rmse_train = linear_regression(training, test)
print("Result linear regression")
print(f"Linear regression rmse_test: {rmse_test}, train: {rmse_train}")

#Binary classification
f1 = binary_classification(training, test)
print("Result binary classification")
print(f"Binary classification F1 Score: {f1}")

#Binary classification
f1 = multiclass_classification(training, test)
print("Result multiclass classification")
print(f"Multiclass classification F1 Score: {f1}")