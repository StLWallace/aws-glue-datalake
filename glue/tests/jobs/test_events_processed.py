from jobs.events_processed import extract_start_date
from pyspark.sql import Row


def test_extract_start_date(spark_session):
    """Validate column expression"""

    data = [{"dates": {"start": {"local_date": "2000-01-01"}}}]

    df = spark_session.createDataFrame(data)

    df = df.select(extract_start_date())

    assert df.collect()[0] == Row(start_date="2000-01-01")
