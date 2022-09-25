from pyspark.ml.regression import LinearRegression
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, SQLTransformer, VectorAssembler
from pyspark.ml.evaluation import RegressionEvaluator, MulticlassClassificationEvaluator
from pyspark.ml.classification import LogisticRegression, DecisionTreeClassifier


def pre_steps(columns):
    indexer = StringIndexer(inputCol="subreddit_name", outputCol="subreddit_name_index")
    vectorize = SQLTransformer(
        statement='SELECT *, vectorize_udf(post_text_em) '
                  'as text_embedding_vectorize FROM __THIS__'
    )
    indexer_NSFW = SQLTransformer(
        statement='SELECT *, int(belongs_to_NSFW) '
                  'as belongs_to_NSFW_index FROM __THIS__'
    )
    assembler = VectorAssembler(
        inputCols=columns,
        outputCol="features")
    return indexer, vectorize, assembler, indexer_NSFW


def linear_regression(train, test):
    indexer, vectorize, assembler, indexer_NSFW = \
        pre_steps(["text_embedding_vectorize", "subreddit_name_index", "number_votes", "num_of_comments", "belongs_to_NSFW_index"])
    lr = LinearRegression(featuresCol="features", labelCol="text_len")
    pipeline = Pipeline(stages=[indexer, indexer_NSFW, vectorize, assembler, lr])
    lr_model = pipeline.fit(train)

    pred_test = lr_model.transform(test)
    pred_train = lr_model.transform(train)

    evaluator = RegressionEvaluator(
        labelCol="text_len", predictionCol="prediction", metricName="rmse")
    rmse_test = evaluator.evaluate(pred_test)
    rmse_train = evaluator.evaluate(pred_train)

    return rmse_test, rmse_train


def binary_classification(train, test):
    indexer, vectorize, assembler, indexer_NSFW = \
    pre_steps(["text_embedding_vectorize", "subreddit_name_index", "number_votes", "num_of_comments"])
    lr = LogisticRegression(featuresCol="features", labelCol="belongs_to_NSFW_index", family="binomial")
    pipeline = Pipeline(stages=[indexer, indexer_NSFW, vectorize, assembler, lr])
    lr_model = pipeline.fit(train)
    predictions = lr_model.transform(test)
    evaluator = MulticlassClassificationEvaluator(
        labelCol="belongs_to_NSFW_index", predictionCol="prediction", metricName="f1")
    return evaluator.evaluate(predictions)


def multiclass_classification(train, test):
    indexer, vectorize, assembler, indexer_NSFW = \
        pre_steps(["text_embedding_vectorize", "number_votes", "num_of_comments", "belongs_to_NSFW_index"])
    dt = DecisionTreeClassifier(featuresCol="features", labelCol="subreddit_name_index")
    pipeline = Pipeline(stages=[indexer, indexer_NSFW, vectorize, assembler, dt])
    dt_model = pipeline.fit(train)
    predictions = dt_model.transform(test)
    evaluator = MulticlassClassificationEvaluator(
        labelCol="subreddit_name_index", predictionCol="prediction", metricName="f1")
    return evaluator.evaluate(predictions)