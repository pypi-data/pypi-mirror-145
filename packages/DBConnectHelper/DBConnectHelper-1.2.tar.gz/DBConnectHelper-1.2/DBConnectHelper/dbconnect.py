from typing import Any, Tuple, Callable
from pyspark.sql import SparkSession, DataFrame
from pyspark.dbutils import DBUtils
import IPython as ip


def _check_is_databricks() -> bool:
    if ip.get_ipython() is None:
        return False
    else:
        user_ns = ip.get_ipython().user_ns
        return "displayHTML" in user_ns


def _get_spark() -> SparkSession:
    if ip.get_ipython() is None:
        spark = SparkSession.builder.getOrCreate()
        return spark
    else:
        user_ns = ip.get_ipython().user_ns
        print(user_ns)
        if "spark" in user_ns:
            print("Inside user_ns")
            return user_ns["spark"]
        else:
            print("Inside Else condition")
            spark = SparkSession.builder.getOrCreate()
            user_ns["spark"] = spark
            return spark


def _get_dbutils(spark: SparkSession):
    try:
        dbutils = DBUtils(spark)
    except ImportError:
        import IPython
        dbutils = IPython.get_ipython().user_ns.get("dbutils")
        if not dbutils:
            print("could not initialise dbutils!")
    return dbutils


# initialise Spark variables
#ipythontest = ip.get_ipython()
#print(ipythontest)
is_databricks: bool = _check_is_databricks()
spark: SparkSession = _get_spark()
dbutils = _get_dbutils(spark)
