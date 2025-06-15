import torch
from transformers import GPT2Tokenizer,GPT2Model
# token generation
# Tokenizer= GPT2Tokenizer.from_pretrained("gpt2")
# input_string="I am Jeevitha Anisetty"
# tokens=Tokenizer.tokenize(input_string)
# print(tokens)

# embeddings generation from tokens
Tokenizer= GPT2Tokenizer.from_pretrained("gpt2")
model= GPT2Model.from_pretrained("gpt2")

input_string="i am sri,i am 4 years old"
tokens=Tokenizer.tokenize(input_string)   # tokens=text format
inputs_constructor=Tokenizer(input_string,return_tensors="pt")  # tokens in pytorch tensors with input_ids and attention mask
INPUTS_encode=Tokenizer.encode(input_string) #just only input_ids not attension mask.if we use encode later we've to use torch.tensor to convert them into pt tensors
print(f"tokens are:  {tokens}  ")
print(f"inputs_constructer are:{inputs_constructor}")
print(f"encode :  {INPUTS_encode}")

#ids r in dict so we have to unpack and give as i/p to model---->o/p
with torch.no_grad():
    output=model(**inputs_constructor)

#outer layer representation of t/f
embeddings=output.last_hidden_state
print(embeddings)

#to see 768 embeddings for each token
for i,token in enumerate (tokens):
    print(f"token:{token}")
    print(f"embedding 768 values:{embeddings[0][i]}")
    print("--------------------------------------------------------------------")
