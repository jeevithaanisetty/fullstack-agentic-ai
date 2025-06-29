
import torch
from transformers import GPT2LMHeadModel,GPT2Tokenizer

prompt="Python is a programming language and it is dynamically typed language"

head_model=GPT2LMHeadModel.from_pretrained("gpt2")
#base_model=GPT2Model.from_pretrained("gpt2")
tokenizer=GPT2Tokenizer.from_pretrained("gpt2")



inputs=tokenizer.encode(prompt,return_tensors="pt")  #---> input_ids (text gen models needs i/p ids only)
output_ids=head_model.generate(
                                inputs,
                                do_sample=True,
                                max_length=500,
                                temperature=0.8,
                                num_return_sequences=3,# if u don't mention it u'll get only one as default and output_ids[1]
                                pad_token_id=tokenizer.eos_token_id   #we have to add padding   `                                                                                                                       `
                            )                                         
#print(output_ids)
#now to generate text we need to decode these o/p ids 
text_generated1=tokenizer.decode(output_ids[0],skip_special_tokens=True)
text_generated2=tokenizer.decode(output_ids[1],skip_special_tokens=True)
#print(f"\n{prompt}\n")
print(f"generated text: {text_generated1}")
print(f"\ngenerated text: {text_generated2}")










































































































































