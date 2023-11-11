from glue.jobs.venues_processed import format_address
from jobs.venues_processed import format_address, extract_markets
from pyspark.sql import Row


def test_format_address(spark_session):
    """Given the expected input format, this should return a reshaped address struct"""
    data = [
        {
            "address": {"line1": "test line 1"},
            "city": {"name": "test city"},
            "state": {"name": "test state", "state_code": "TS"},
            "country": {"name": "test country", "country_code": "TC"},
            "postal_code": "00000",
        }
    ]
    df = spark_session.createDataFrame(data)

    df = df.select(format_address())

    assert df.collect()[0] == Row(
        address=Row(
            street="test line 1",
            city="test city",
            state={"name": "test state", "state_code": "TS"},
            postal_code="00000",
            country={"name": "test country", "country_code": "TC"},
        )
    )


def test_extract_markets(spark_session):
    """Given a list of market structs, this should return a flattened list of markets"""
    data = [{"markets": [{"id": 1}]}]

    df = spark_session.createDataFrame(data)

    df = df.select(extract_markets())

    assert df.collect()[0] == Row(markets=[1])
