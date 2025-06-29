import os
import fitz
import faiss
import openai
from dotenv import load_dotenv
import numpy as np
import sys

load_dotenv()
openai.api_key=os.getenv("OPEN_API_KEY")

def get_text_from_pdf(pdf_file_path):
    pdf_pages=fitz.open(pdf_file_path)
    pdf_text="\n".join([p.get_text() for p in pdf_pages])
    return pdf_text

def chuck_pdf_text(text,chunk_size):
    words=text.split()  # tokens--->chunks likewise text-->words(tokens)-->chunks
    chunked_text=" ".join([words[i:i+chunk_size] for i in range(0,len(text),chunk_size)])
    return chunked_text

def vectors_to_chunks(text):
    embeddings=openai.embeddings.create(model="text-embedding-3-small",input=text)
    vectors=np.array([e for e in embeddings]).astype("float32")    #np.array( [e.embedding for e in embeddings.data]).astype("float32")
    return vectors

def search_faiss_index(index,query_vector):
    distance,indices=index.search(query_vector,5)
    return indices[0]

def ask_gpt4(Context,Query):
    context = "\n".join(Context)

    system_prompt={
        "you are an expert assistant.Answer ONLY based on the provided context"
        "if the answer is not found,say no information available"
    }
    messages=[
        {"role":"system","content":system_prompt},
        {"role":"user","content":f"context:\n{context} \n Question :{Query}"}
    ]
    response=openai.chat.completions.create(
        model="gpt4",
        messages=messages,
        temperature=0.2
    )
    return response.choices[0].message.content.strip()

def main():

    # if len(sys.argv) < 2:
    #     print ("Tool Usage  : python gpt4-cli-bot.py <PDF Filepath>")
    #     sys.exit(1)
    pdf_file_path = sys.argv[1]
    
    print (f"Loading the PDF File {pdf_file_path}")
    if not os.path.exists(pdf_file_path):
        print ("Source PDF file is not available.")
        sys.exit(1)
    
    pdf_text=get_text_from_pdf(pdf_file_path)
    chunks=chuck_pdf_text(pdf_text,100)
    vectors=vectors_to_chunks(chunks)

    index=faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)

    while True:
        query=input("ask your question to chat bot and enter exit to close the application")
        if query.lower()=="exit":
            print("closing the application")
            break
        query_embedding=openai.embeddings.create("text-embedding-3-small",query)
        query_vector=np.array(query_embedding).astype("float32")  #np.array([query_emdedding.data[0].embedding], dtype = 'float32')
        
        top_indices=search_faiss_index(index,query_vector)

        context =  [chunks[i] for i in top_indices]

        answer=ask_gpt4(context,query)
        print(f"Answer is: {answer}")

if __name__=="__main__":
    main()

    