from jobs.events_processed import extract_start_date, extract_sales, extract_image_urls
from pyspark.sql import Row


def test_extract_start_date(spark_session):
    """Validate column expression"""

    data = [{"dates": {"start": {"local_date": "2000-01-01"}}}]

    df = spark_session.createDataFrame(data)

    df = df.select(extract_start_date())

    assert df.collect()[0] == Row(start_date="2000-01-01")


def test_extract_sales(spark_session):
    """Should create new column called sales_start_date_time"""
    data = [{"sales": {"public": {"start_date_time": "2000-01-01"}}}]

    df = spark_session.createDataFrame(data)

    df = df.select(extract_sales(attr="start_date_time"))

    assert df.collect()[0] == Row(sales_start_date_time="2000-01-01")


def test_extract_image_urls(spark_session):
    """Given a list of of image structs, should return a list of image urls"""
    data = [{"images": [{"url": "s3://test"}]}]

    df = spark_session.createDataFrame(data)

    df = df.select(extract_image_urls())

    assert df.collect()[0] == Row(image_urls=["s3://test"])
