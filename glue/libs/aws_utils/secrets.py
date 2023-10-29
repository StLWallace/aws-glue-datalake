from typing import Any
import boto3
import json


def get_secret_value(secret_id: str, secrets_client: Any = None) -> dict:
    """Gets a secret value from AWS Secrets Manager
    Args:
        secret_id - the name of the secret to retrieve
        secrets_client - a boto3 SecretsManager client

    Returns:
        A dictionary containing the secret value
    """
    if secrets_client is None:
        secrets_client = boto3.client("secretsmanager")

    response = secrets_client.get_secret_value(SecretId=secret_id)

    secret_dict = json.loads(response["SecretString"])

    return secret_dict
