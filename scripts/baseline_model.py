import datetime
import mlflow
import numpy as np
import pandas as pd
import scipy.sparse as sparse
import time
import warnings

from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity
from tempfile import NamedTemporaryFile
from mlxtend.frequent_patterns import apriori, association_rules
from pyspark.ml.fpm import FPGrowth
from pyspark.ml.feature import StringIndexer
from pyspark.ml import Pipeline
from pyspark.ml.recommendation import ALS
from pyspark.sql import functions as F


warnings.filterwarnings("ignore", category=DeprecationWarning)


# Cosine Similarity Recommendations
def generate_cosine_sim_recs(df, filename, rows='user_session', cols='product_id', quantity='product_quantity', top=11):
    """
    Generate recommendations using cosine similarity.
    Tracks metrics and artifacts with MLflow.
    """
    with mlflow.start_run(run_name="Cosine Similarity Recommendations"):
        try:
            # Start time tracking
            start_time = time.time()

            # Prepare data
            orders = list(sorted(set(df[rows])))
            products = list(sorted(set(df[cols])))
            quantities = list(df[quantity])

            rs = pd.Categorical(df[rows], categories=orders).codes
            cs = pd.Categorical(df[cols], categories=products).codes

            # Create sparse matrix
            sparse_matrix = sparse.csr_matrix((quantities, (rs, cs)), shape=(len(orders), len(products)))

            # Log sparsity
            matrix_size = sparse_matrix.shape[0] * sparse_matrix.shape[1]
            num_purchases = len(sparse_matrix.nonzero()[0])
            sparsity = round(100 * (1 - (float(num_purchases) / matrix_size)), 2)
            mlflow.log_metric("sparsity", sparsity)

            # Compute cosine similarity
            similarities = cosine_similarity(sparse_matrix.T)
            df_sim = pd.DataFrame(similarities, index=products, columns=products)
            mlflow.log_metric("cosine_similarity_calculation_time", round(time.time() - start_time, 2))

            # Generate recommendations
            start_time = time.time()
            df_match = pd.DataFrame(index=products, columns=[f'Rec {i}' for i in range(1, top)])
            df_score = pd.DataFrame(index=products, columns=[f'Score {i}' for i in range(1, top)])

            for i in range(len(products)):
                top_recs = df_sim.iloc[:, i].sort_values(ascending=False)
                top_recs = top_recs[top_recs.index != df_sim.index[i]]
                num_recs = min(top - 1, len(top_recs), df_match.shape[1])

                df_match.iloc[i, :num_recs] = top_recs.iloc[:num_recs].index
                df_score.iloc[i, :num_recs] = top_recs.iloc[:num_recs].values

            # Combine recommendations and scores
            df_new = df_match.merge(df_score, how="inner", left_index=True, right_index=True)
            df_new.index.names = ['product_id']

            # Save recommendations to file
            df_new.to_csv(filename)
            mlflow.log_artifact(filename)

            mlflow.log_metric("recommendation_generation_time", round(time.time() - start_time, 2))
            print("Cosine similarity recommendations generated.")
            return df_new

        except Exception as e:
            mlflow.log_param("error", str(e))
            raise e

# FP-Growth
def run_fp_growth(df, min_support=0.001, min_confidence=0.1):
    """
    Run FP-Growth on the input PySpark DataFrame to generate frequent itemsets and association rules.
    Tracks metrics and artifacts with MLflow.
    Args:
        df (DataFrame): Input PySpark DataFrame with 'user_session' and 'cosmeticProductId' columns.
        min_support (float): Minimum support for frequent itemsets.
        min_confidence (float): Minimum confidence for association rules.
    Returns:
        frequent_itemsets (DataFrame): Frequent itemsets generated by FP-Growth.
        association_rules (DataFrame): Association rules generated by FP-Growth.
    """
    with mlflow.start_run(run_name="FP-Growth"):
        try:
            # Prepare data: Group items by user_session
            fp_data = df.groupBy("user_session").agg(F.collect_set("cosmetic_product_id").alias("items"))

            # Train FP-Growth model
            fp_growth = FPGrowth(itemsCol="items", minSupport=min_support, minConfidence=min_confidence)
            model = fp_growth.fit(fp_data)

            # Get frequent itemsets
            frequent_itemsets = model.freqItemsets.toPandas()
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            frequent_itemsets_filename = f"frequent_itemsets.csv"
            frequent_itemsets.to_csv(frequent_itemsets_filename, index=False)
            mlflow.log_artifact(frequent_itemsets_filename)
            mlflow.log_metric("frequent_itemsets_count", len(frequent_itemsets))

            # Get association rules
            association_rules = model.associationRules.toPandas()
            association_rules_filename = f"association_rules.csv"
            association_rules.to_csv(association_rules_filename, index=False)
            mlflow.log_artifact(association_rules_filename)
            mlflow.log_metric("association_rules_count", len(association_rules))

            print("FP-Growth completed successfully.")
            return frequent_itemsets, association_rules

        except Exception as e:
            mlflow.log_param("error", str(e))
            raise e
    
def run_als_recommender(
    spark_df, 
    user_col='user_session', 
    item_col='cosmetic_product_id', 
    rating_col='product_quantity',
    rank=10, 
    maxIter=10, 
    regParam=0.1
):
    """
    Trains an ALS recommender on a PySpark DataFrame and logs outputs via MLflow.
    Returns the trained model and top-N user/item recommendations.
    """
    with mlflow.start_run(run_name="ALS-Recommender"):
        try:
            # Start timer
            start_time = time.time()

            # Prepare data: Convert string user_session to numeric index
            user_indexer = StringIndexer(inputCol=user_col, outputCol="user_session_index", handleInvalid="skip")
            pipeline = Pipeline(stages=[user_indexer])
            indexed_df = pipeline.fit(spark_df).transform(spark_df)

            # Train ALS model
            als = ALS(
                userCol="user_session_index",
                itemCol=item_col,
                ratingCol=rating_col,
                rank=rank,
                maxIter=maxIter,
                regParam=regParam,
                implicitPrefs=True,
                coldStartStrategy="drop"
            )
            model = als.fit(indexed_df)

            # Log ALS parameters
            mlflow.log_param("rank", rank)
            mlflow.log_param("maxIter", maxIter)
            mlflow.log_param("regParam", regParam)

            # Generate recommendations
            user_recs = model.recommendForAllUsers(10).toPandas()
            item_recs = model.recommendForAllItems(10).toPandas()

            # Save and log user recommendations as Parquet
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            user_recs_filename = f"user_recommendations.parquet"
            user_recs.to_parquet(user_recs_filename, index=False)
            mlflow.log_artifact(user_recs_filename)
            mlflow.log_metric("user_recommendations_count", len(user_recs))

            # Save and log item recommendations as Parquet
            item_recs_filename = f"item_recommendations.parquet"
            item_recs.to_parquet(item_recs_filename, index=False)
            mlflow.log_artifact(item_recs_filename)
            mlflow.log_metric("item_recommendations_count", len(item_recs))

            # Log training time
            training_time = round(time.time() - start_time, 2)
            mlflow.log_metric("training_time", training_time)

            print("ALS model training completed successfully.")
            return model, user_recs, item_recs

        except Exception as e:
            mlflow.log_param("error", str(e))
            raise e
