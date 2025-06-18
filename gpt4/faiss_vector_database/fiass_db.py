from openai import OpenAI
import numpy as np
import os
import faiss   
import pickle

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")   # Loads OpenAI API key from environment variables for security.
FAISS_DB_FILE="text_index.faiss"             # faiss db (File path where the FAISS index is stored.)
LABEL_MAP_FILE="text_label.pk1"              # pickle file(heatmap:menu)--->File path for storing label mappings using pickle.
VECTOR_DIM=1536                              # dim of embedding vectors return by model (768+768)

client= OpenAI (api_key=os.getenv("OPENAI_API_KEY"))  # creating OpenAI client using API_KEY

if os.path.exists(FAISS_DB_FILE):            # load faiss db if not exists creates db with max L2 vector distance 
    index=faiss.read_index(FAISS_DB_FILE) 
else:
    index=faiss.IndexFLatL2(VECTOR_DIM)

if os.path.exists(LABEL_MAP_FILE):           # loads labelmap i.e a dict having (index :label)
    with open(LABEL_MAP_FILE,"rb") as f:
        label_map=pickle.load(f)
else:
    label_map={}

def get_embeddings(Text:str):                 # in gpt4 for text, embedding model is text-embedding-3-small.
    response=client.embeddings.create(model="text-embedding-3-small",input=Text)
    return response.data[0].embedding         #returns list of 1536 float vectors

def add_embeddings_to_index():
    text=input("enter text to add to faiss database: ")
    label=input("enter label to text: ")

    text_embeddings=get_embeddings(text)
    print(text_embeddings)

    vectors=np.array([text_embeddings]).astype("float32")  # Converts the embedding into a NumPy array (2D) of type float32 (required by FAISS)
    print(vectors)

    index_id=index.ntotal                     #current vector index_id--->as a new vector_id
    #print(f"index_id:{index_id}")
    index.add(vectors)                        #Adds the new embedding to the FAISS index.
    label_map[index_id]=label                 # index_id : label ---->add label to the current index_id
    save_index()

def save_index():
    faiss.write_index(index,FAISS_DB_FILE)
    with open (LABEL_MAP_FILE,"wb") as f:
        pickle.dump(label_map,f)              #  index_id : label dumps this in pickle(like menu)

def list_labels():
    for idx,label in label_map.items():
        print(f"{idx} : {label}")

if __name__=="__main__":
    add_embeddings_to_index()
    list_labels()
