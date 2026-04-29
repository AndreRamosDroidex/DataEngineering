import sys
import json
import urllib.request
import boto3

from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import Row

args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

job = Job(glueContext)
job.init(args['JOB_NAME'], args)


def get_openai_key():
    client = boto3.client("secretsmanager", region_name="us-east-1")
    response = client.get_secret_value(SecretId="openai/api_key")
    secret = json.loads(response["SecretString"])
    return secret["OPENAI_API_KEY"]


OPENAI_API_KEY = get_openai_key()

input_bucket = "datascience-taller-gold"
input_key = "ventas"
input_path = f"s3://{input_bucket}/{input_key}"

output_bucket = "datascience-taller-analytics"
output_key = "ventas_ai"
output_path = f"s3://{output_bucket}/{output_key}"


def call_openai(opinion):
    if opinion is None or str(opinion).strip() == "":
        return {
            "sentiment": "unknown",
            "category": "other",
            "summary": ""
        }

    prompt = f"""
Return only valid JSON with these fields:
sentiment: positive, negative or neutral
category: delivery, product, price, service or other
summary: maximum 10 words

Opinion: {opinion}
"""

    payload = {
        "model": "gpt-4o-mini",
        "input": prompt
    }

    req = urllib.request.Request(
        "https://api.openai.com/v1/responses",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))

        text = result["output"][0]["content"][0]["text"]
        return json.loads(text)

    except Exception as e:
        return {
            "sentiment": "error",
            "category": "other",
            "summary": str(e)[:100]
        }


df_gold = spark.read.parquet(input_path)

# Para demo: solo 20 filas para no gastar créditos
rows = df_gold.limit(20).collect()

enriched_rows = []

for row in rows:
    row_dict = row.asDict()

    opinion = row_dict.get("Opinion", "")
    ai = call_openai(opinion)

    row_dict["sentiment"] = ai.get("sentiment", "unknown")
    row_dict["category"] = ai.get("category", "other")
    row_dict["summary"] = ai.get("summary", "")

    enriched_rows.append(Row(**row_dict))


df_ai = spark.createDataFrame(enriched_rows)

df_ai.write.mode("overwrite").parquet(output_path)

spark.sql(f"""
CREATE EXTERNAL TABLE IF NOT EXISTS `datascience-taller-analytics`.ventas_ai(
    InvoiceNo string,
    StockCode string,
    Description string,
    Quantity int,
    InvoiceDate string,
    UnitPrice double,
    CustomerID string,
    Country string,
    Opinion string,
    TotalAmount double,
    sentiment string,
    category string,
    summary string
)
STORED AS PARQUET
LOCATION '{output_path}'
""")

job.commit()
