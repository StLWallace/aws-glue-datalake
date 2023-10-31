import pytest
from pyspark.context import SparkContext
from pyspark.sql import SparkSession
import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT_DIR)


@pytest.fixture
def spark_session() -> SparkSession:
    sc = SparkContext.getOrCreate()
    spark = SparkSession(sc)

    yield spark
