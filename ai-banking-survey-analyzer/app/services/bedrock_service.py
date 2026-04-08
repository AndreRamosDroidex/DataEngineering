import boto3
import json
from app.core.config import settings

class BedrockService:

    def __init__(self):
        self.client = boto3.client(
            "bedrock-runtime",
            region_name=settings.aws_region
        )

    def analyze_survey(self, text: str):

        prompt = f"""
You are an AI specialized in banking analytics.

Analyze the following customer feedback:

"{text}"

Return strictly in JSON format with:
- sentiment
- summary
- main_topics (list)
- recommendations
"""

        body = {
            "messages": [
                {
                    "role": "user",
                    "content": [{"text": prompt}]
                }
            ]
        }

        response = self.client.invoke_model(
            modelId=settings.bedrock_text_model_id,
            body=json.dumps(body)
        )

        raw = json.loads(response["body"].read())

        # 👇 EXTRAER TEXTO REAL DEL MODELO
        text_output = raw["output"]["message"]["content"][0]["text"]

        return {
            "raw_response": text_output
        }