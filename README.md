# RAG
Rag (Retreival Augmented Generation) Python solution with llama3 in a Flask API based solution

## Set Up
Install Requirements

```
pip install -r requirements.txt
```

Run App

```
python3 app.py
```

The app will run at http://127.0.0.1:8081

## Available Endpoints

### Document Upload

Enables uploading documents to the model context
- _The server currently only supports uploading csv documents via the /pdf endpoint_

URL: http://127.0.0.1:8081/pdf

Request Body
```
{
  "file": <file_upload>
}
```

Response Body
```
{
  "status": "Successfully Uploaded",
  "filename": "<file_name>",
  "doc_len": <document_length>,
  "chunks": <number_of_chunks>,
}
```

### User Queries

Provides responses to user queries based on the uploaded documents.

URL: http://127.0.0.1:8081/ask_pdf

Request Body
```
{
  "query": "<user_query>"
}
```

Response Body
```
{
  "answer": "<llm_response>"
}
```
