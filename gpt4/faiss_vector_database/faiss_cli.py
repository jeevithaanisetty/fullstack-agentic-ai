import os
import faiss
import pickle
from openai import OpenAI
import numpy as np

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
FAISS_DB="text_index.faiss"
LABEL_MAP_FILE="text_pickle.pk1"
VECTOR_DIM=1536

client=OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

if os.path.exists(FAISS_DB):
    index=faiss.read_index(FAISS_DB)
else:
    index=faiss.IndexFlatL2(VECTOR_DIM)

if os.path.exists(LABEL_MAP_FILE):
    with open (LABEL_MAP_FILE,"rb") as f:
        label_map=pickle.load(f)
else:
    label_map={}

def get_embeddings(Text:str):
    response=client.embeddings.create(model="text-embedding-3-small",input=Text)
    return response.data[0].embedding

def add_vectors_to_faiss_index():
    text=input("enter text to find vector and add to faiss db: ")
    label=input("enter label to index: ")

    text_embeddings=get_embeddings(text)
    vector=np.array([text_embeddings]).astype("float32")

    index_id=index.ntotal
    index.add(vector)

    label_map[index_id]=label
    save_index()

def save_index():
    faiss.write_index(index,FAISS_DB)
    with open(LABEL_MAP_FILE,"wb")as f:
        pickle.dump(label_map,f)

def list_lables():
    for idx,label in label_map.items():
        print(f"{idx} : {label}")
        
def compare_labels():
    first_label=input("enter first label: ")
    second_label=input("enter second label: ")
    
    v1=v2=None  #initially we've to define v1 and v2 as none to avoid err

    for idx,label in label_map.items():
        if label==first_label:
            v1=index.reconstruct(idx)
        if label==second_label:
            v2=index.reconstruct(idx)
    if v1 is None or v2 is None:
        print("first or second label is not found....")
    
    v1,v2=np.array(v1),np.array(v2)

    similarity=(np.dot(v1,v2)/(np.linalg.norm(v1) * np.linalg.norm(v2)))
    print(f"similarity for {first_label} and {second_label} is: {similarity}")
        

def menu():
    while True:
        print("\n----------------FAISS CLI--------------------")
        print("1.Add Vector to index")
        print("2.List Labels")
        print("3.Compare Labels(Similarity)")
        print("4.Exit")
        choice=int(input("enter choice: "))

        if choice==1:
            add_vectors_to_faiss_index()
        elif choice==2:
            list_lables()
        elif choice==3:
            compare_labels()
        elif choice==4:
            break
        else:
            print("Invalid Choice....")

if __name__=="__main__":
    menu()


