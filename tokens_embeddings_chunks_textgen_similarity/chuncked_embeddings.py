from transformers import GPT2Tokenizer,GPT2Model
import torch  # module having math operations belongs to tensors
import csv

# 1. Read the Input file
# 2. Get the  Tokens (Assume we have 1000 tokens)
# 2. Set Chunk Size = 100
# 3. Get First 100 Tokens (Remaining  900)
# 4. Get the  Ids
# 5. Send to Model 
# 6. Get the Embedding  for first 100
# 7. Process them or Save or print or bla bla bla 
# 8. Goto Step 3

with open("data.txt","r",encoding="utf-8") as f:
    file_text=f.read().strip()   # read all the file content and remove L and T spaces
print(f"file content is:\n{file_text}\n")

tokenizer=GPT2Tokenizer.from_pretrained("gpt2")
model=GPT2Model.from_pretrained("gpt2")

tokens=tokenizer.encode(file_text)  #list of tokens i.e may be 10000 (no format and not in dict)
print(f"\nencoded tokens are:{tokens}")

print(f"\nlen of tokens:{len(tokens)}")
chunk_size=100

#devide tokens based on chunk_size and give aech batch as i/p to model
for i in range(0,len(tokens),chunk_size):
    chuncked_tokens=tokens[i:i+chunk_size]  #100 tokens batch
    
    input=torch.tensor([chuncked_tokens])  # model understand i/p in form of tensors only
    print(input)

    with torch.no_grad():
        output=model(input)                 #no unpacking i/p is not in dict
        embeddings=output.last_hidden_state
        print(f"last_hidden:{embeddings}")#full embeddings(having 768 embeddings for each token)--->shape[1,5,768]

        mean_embeddings=embeddings.mean(dim=1) #768 tokens for all tokens-->shape[1,768]
        print(f"average embeddings:{mean_embeddings}")

        #getting back text from chuncked tokens
        chuncked_text=tokenizer.decode(chuncked_tokens)   #encode-->no format tokens    decode-->text format from nos
        print(f"decoded chunks are:{chuncked_text}")








