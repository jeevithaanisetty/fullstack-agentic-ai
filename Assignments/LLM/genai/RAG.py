import google.generativeai as genai
import numpy as numpy
import faiss
import PyPDF2
import os  

genai.configure(api_key=os.getenv("GEMINI-API-KEY"))
model=genai.GenerativeModel("gemini-2.5-pro")

def extract_text_from_pdf(pdf_path):
    text=""
    with open (pdf_path,"rb") as f:
        reader=PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() +"\n"
    return text

def chunk_text(text,chunk_size=500,overlap=50):
    chunks=[]
    while text:
        chunk = text[:chunk_size]
        chunks.append(chunk)
        text = text[chunk_size - overlap:]
    return chunks

def get_embedding(text):
    response=genai.embed_content(model="models/embedding-001",content=text)
    return np.array(response["embedding"])

def retrieve(query,chunks,index,chunk_embeddings,top_k=3):
    query_emb=get_embedding(query)
    query_emb=np.array([query_emb])
    distances,indices=index.search(query_emb,top_k)
    return [chunks[i] for i in indices[0]]

def generate_answer(query,retrieved_chunks):
    context="\n".join(retrieved_chunks)
    prompt=f"Answer the question based on this context below:{context} \n\nQuestion:{query}\n\nAnswer: "
    response=model.generate_content(prompt)
    return response.text

print("=======GEMINI PDF RAG CHATBOT WITH FAISS=========")
print("type exit to quit")
while True:
    query=input("You: ")
    if query.lower()=="exit":
        break

    pdf_text= extract_text_from_pdf("sample.pdf")
    chunks= chunk_text(pdf_text)
    chunk_embeddings=[get_embedding(chunk) for chunk in chunks]

    embedding_dim=len(chunk_embedding[0])
    index=faiss.IndexFlatL2(embedding_dim)
    index.add(np.array(chunk_embeddings))

    relavant_chunks=retrieve(query,chunks,index,chunk_embeddings,top_k=3)
    answer=generate_answer(query,relavant_chunks)
    print("Bot: ",answer)

    




