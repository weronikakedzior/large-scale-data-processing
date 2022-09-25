from flask import Flask
from flask import request
from pymagnitude import Magnitude
import numpy as np
from pyspark import SparkContext
from pyspark.ml import PipelineModel
from pyspark.sql import SQLContext
from pyspark.ml.linalg import Vectors, VectorUDT
from pyspark.sql.functions import udf

app = Flask(__name__)
sc = SparkContext('local')
sqlContext = SQLContext(sc)

model_reg = PipelineModel.load('models/liner_regression')

model_multiclass = PipelineModel.load("models/multiclass")
model_binary_class = PipelineModel.load("models/binary")
vectors = Magnitude("GoogleNews.magnitude")


@app.route('/linearregression')
def linear_regression():
    text = request.args.get("text")
    text = create_embedding(text)
    subreddit_name = request.args.get("subreddit")
    number_votes = request.args.get("number_votes")
    num_of_comments = request.args.get("num_of_comments")
    belongs_to_NSFW_ind = request.args.get("belongs_to_NSFW_ind")

    df = sqlContext.createDataFrame([(text, subreddit_name, int(number_votes), int(num_of_comments), str(belongs_to_NSFW_ind))],
                                    ["post_text_em", "subreddit_name", "number_votes", "num_of_comments", "belongs_to_NSFW_index"])
    df = df.select(
        df["subreddit_name"],
        df['number_votes'],
        df['num_of_comments'],
        df['belongs_to_NSFW_index'],
        list_to_vector_udf(df["post_text_em"]).alias("text_embedding_vectorize")
    )
    pred = model_reg.transform(df)
    result = str(pred.collect()[0]['prediction'])
    return result


@app.route('/multiclass')
def multiclass():
    text = request.args.get("text")
    text = create_embedding(text)
    number_votes = request.args.get("number_votes")
    num_of_comments = request.args.get("num_of_comments")
    belongs_to_NSFW_ind = request.args.get("belongs_to_NSFW_ind")
    df = sqlContext.createDataFrame(
        [(text,  int(number_votes), int(num_of_comments), str(belongs_to_NSFW_ind))],
        ["post_text_em",  "number_votes", "num_of_comments", "belongs_to_NSFW_index"])
    df = df.select(
        df['number_votes'],
        df['num_of_comments'],
        df['belongs_to_NSFW_index'],
        list_to_vector_udf(df["post_text_em"]).alias("text_embedding_vectorize")
    )
    pred = model_multiclass.transform(df)
    result = str(pred.collect()[0]['prediction'])
    return result


@app.route('/binary')
def binary():
    text = request.args.get("text")
    text = create_embedding(text)
    subreddit_name = request.args.get("subreddit")
    number_votes = request.args.get("number_votes")
    num_of_comments = request.args.get("num_of_comments")
    df = sqlContext.createDataFrame(
        [(text, int(number_votes), int(num_of_comments), subreddit_name)],
        ["post_text_em", "number_votes", "num_of_comments", "subreddit_name"])
    df = df.select(
         df["subreddit_name"],
        df['number_votes'],
        df['num_of_comments'],
        list_to_vector_udf(df["post_text_em"]).alias("text_embedding_vectorize")
    )
    pred = model_binary_class.transform(df)
    result = str(pred.collect()[0]['prediction'])
    return result

list_to_vector_udf = udf(lambda l: Vectors.dense(l), VectorUDT())
def create_embedding(text):
    embeddings = vectors.query(text.split())
    embeddings = np.mean(embeddings, axis=0)
    toappend = 300 - len(embeddings)
    embedding = np.append(embeddings, np.array([0]*toappend))
    return embedding.tolist()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)