from langchain_community.embeddings import LlamaCppEmbeddings

llama = LlamaCppEmbeddings(model_path="/path/to/model/ggml-model-q4_0.bin")

text = "This is a test document."

query_result = llama.embed_query(text)

print(query_result)