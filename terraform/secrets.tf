# Create a secret for the Ticketmaster API key
resource "aws_secretsmanager_secret" "ticketmaster_api_key" {
  name = "ticketmaster-api-key-${var.environment}"
}
