from pyspark.ml.regression import LinearRegression
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, SQLTransformer, VectorAssembler
from pyspark.ml.evaluation import RegressionEvaluator, MulticlassClassificationEvaluator
from pyspark.ml.classification import LogisticRegression, DecisionTreeClassifier


def pre_steps(columns):
    indexer = StringIndexer(inputCol="subreddit_name", outputCol="subreddit_name_index")
    indexerNSFW = StringIndexer(inputCol="belongs_to_NSFW_index", outputCol="belongs_to_NSFW_ind")

    assembler = VectorAssembler(
        inputCols=columns,
        outputCol="features")
    return indexer, assembler, indexerNSFW


def linear_regression(train, test):
    indexer = StringIndexer(inputCol="subreddit_name", outputCol="subreddit_name_index")
    indexerNSFW = StringIndexer(inputCol="belongs_to_NSFW_index", outputCol="belongs_to_NSFW_ind")
    assembler = VectorAssembler(
        inputCols=["text_embedding_vectorize", "subreddit_name_index", "number_votes", "num_of_comments", "belongs_to_NSFW_ind"],
        outputCol="features")
    #indexer, assembler, indexerNSFW = \
    #    pre_steps(["text_embedding_vectorize", "subreddit_name_index", "number_votes", "num_of_comments", "belongs_to_NSFW_ind"])
    lr = LinearRegression(featuresCol="features", labelCol='text_len')
    pipeline = Pipeline(stages=[indexer, indexerNSFW, assembler, lr])
    lr_model = pipeline.fit(train)

    #lr_model.serializeToBundle("jar:file:/app/linear_regression.zip", lr_model.transform(train))
    pred_test = lr_model.transform(test)
    pred_train = lr_model.transform(train)
    lr_model.save("liner_regression")
    evaluator = RegressionEvaluator(
        labelCol="text_len", predictionCol="prediction", metricName="rmse")
    rmse_test = evaluator.evaluate(pred_test)
    rmse_train = evaluator.evaluate(pred_train)

    return rmse_test, rmse_train


def binary_classification(train, test):
    indexer, assembler, indexerNSFW = \
    pre_steps(["text_embedding_vectorize", "subreddit_name_index", "number_votes", "num_of_comments"])
    lr = LogisticRegression(featuresCol="features", labelCol="belongs_to_NSFW_ind", family="binomial")
    pipeline = Pipeline(stages=[indexer, indexerNSFW, assembler, lr])
    lr_model = pipeline.fit(train)
    lr_model.save("binary")
    #lr_model.serializeToBundle("jar:file:/app/binary_classification.zip", lr_model.transform(train))
    predictions = lr_model.transform(test)
    evaluator = MulticlassClassificationEvaluator(
        labelCol="belongs_to_NSFW_ind", predictionCol="prediction", metricName="f1")
    return evaluator.evaluate(predictions)


def multiclass_classification(train, test):
    indexer,  assembler, indexerNSFW = \
        pre_steps(["text_embedding_vectorize", "number_votes", "num_of_comments", "belongs_to_NSFW_ind"])
    dt = DecisionTreeClassifier(featuresCol="features", labelCol="subreddit_name_index")
    pipeline = Pipeline(stages=[indexer, indexerNSFW, assembler, dt])
    dt_model = pipeline.fit(train)
    dt_model.save("multiclass")
    #dt_model.serializeToBundle("jar:file:/app/multiclass_classification.zip", dt_model.transform(train))
    predictions = dt_model.transform(test)
    evaluator = MulticlassClassificationEvaluator(
        labelCol="subreddit_name_index", predictionCol="prediction", metricName="f1")
    return evaluator.evaluate(predictions)