# Serverless REST API

A CRUD REST API built with AWS Lambda, API Gateway, and DynamoDB (tested locally via LocalStack).

## Architecture
- **API Gateway**: HTTP endpoint routing (/notes, /notes/{id})
- **Lambda**: Business logic handling Create, Read, Update, Delete operations
- **DynamoDB**: NoSQL storage for note records

## Endpoints
- POST /notes - Create a note
- GET /notes/{id} - Read a note
- PUT /notes/{id} - Update a note
- DELETE /notes/{id} - Delete a note

