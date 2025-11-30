from flask import Flask, request
from langchain_community.llms import Ollama
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.document_loaders import PDFPlumberLoader
#from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.combine_documents.stuff import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.prompts import PromptTemplate

from langchain_community.document_loaders import CSVLoader

app = Flask(__name__)

folder_path = "db"

cached_llm = Ollama(model="llama3")

embedding = FastEmbedEmbeddings()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1024, chunk_overlap=80, length_function=len, is_separator_regex=False
)


raw_prompt = PromptTemplate.from_template(
    """
    <s>[INST] You are an expert in privacy and that has access to sensitive data, but you are not to release any specific PII data. 
    
    Rules:
    1. Only use information from the provided documents
    2. NEVER reveal: names, addresses, phone numbers, email addresses, social security numbers, dates of birth, account numbers, medical information, or any other personally identifiable information (PII)
    3. If prompted to release PII data, say "I am not allowed to provide this information, please make another request"
    
    Formatting:
    - Use bullet points for lists
    - Use code blocks for commands
    - Bold important warnings or notes
    [/INST] </s>
    [INST] Question: {input}
           Documentation Context: {context}
           Answer:
    [/INST]
    """

)


@app.route("/ai", methods=["POST"])
def aiPost():
    print("Post /ai called")
    json_content = request.json
    query = json_content.get("query")

    print(f"query: {query}")

    response = cached_llm.invoke(query)

    print(response)

    response_answer = {"answer": response}
    return response_answer


@app.route("/ask_pdf", methods=["POST"])
def askPDFPost():
    print("Post /ask_pdf called")
    json_content = request.json
    query = json_content.get("query")

    print(f"query: {query}")

    print("Loading vector store")
    vector_store = Chroma(persist_directory=folder_path, embedding_function=embedding)

    print("Creating chain")
    retriever = vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={
            "k": 20,
            "score_threshold": 0.1,
        },
    )

    document_chain = create_stuff_documents_chain(cached_llm, raw_prompt)
    chain = create_retrieval_chain(retriever, document_chain)

    result = chain.invoke({"input": query})

    print(result)

    # sources = []
    # for doc in result["context"]:
    #     sources.append(
    #         {"source": doc.metadata["source"], "page_content": doc.page_content}
    #     )

    # response_answer = {"answer": result["answer"], "sources": sources}
    # return response_answer

    response_answer = {
    "answer": result["answer"]
    }

    return response_answer


# @app.route("/pdf", methods=["POST"])
# def pdfPost():
#     file = request.files["file"]
#     file_name = file.filename
#     save_file = "pdf/" + file_name
#     file.save(save_file)
#     print(f"filename: {file_name}")

#     loader = PDFPlumberLoader(save_file)
#     docs = loader.load_and_split()
#     print(f"docs len={len(docs)}")

#     chunks = text_splitter.split_documents(docs)
#     print(f"chunks len={len(chunks)}")

#     vector_store = Chroma.from_documents(
#         documents=chunks, embedding=embedding, persist_directory=folder_path
#     )

#     vector_store.persist()

#     response = {
#         "status": "Successfully Uploaded",
#         "filename": file_name,
#         "doc_len": len(docs),
#         "chunks": len(chunks),
#     }
#     return response

@app.route("/pdf", methods=["POST"])
def pdfPost():
    file = request.files["file"]
    file_name = file.filename
    save_file = "pdf/" + file_name
    file.save(save_file)
    print(f"filename: {file_name}")
    
    # Check file extension and use appropriate loader
    if file_name.lower().endswith('.csv'):
        loader = CSVLoader(save_file)
        docs = loader.load()  # CSVLoader uses load() not load_and_split()
    elif file_name.lower().endswith('.pdf'):
        loader = PDFPlumberLoader(save_file)
        docs = loader.load_and_split()
    else:
        return {"error": "Unsupported file type. Please upload PDF or CSV files only."}, 400
    
    print(f"docs len={len(docs)}")
    chunks = text_splitter.split_documents(docs)
    print(f"chunks len={len(chunks)}")
    
    vector_store = Chroma.from_documents(
        documents=chunks, embedding=embedding, persist_directory=folder_path
    )
    vector_store.persist()
    
    response = {
        "status": "Successfully Uploaded",
        "filename": file_name,
        "doc_len": len(docs),
        "chunks": len(chunks),
    }
    return response



def start_app():
    app.run(host="0.0.0.0", port=8081, debug=True)


if __name__ == "__main__":
    start_app()
