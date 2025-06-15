
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
                                pad_token_id=tokenizer.eos_token_id   #we have to add padding   `                                                                                                                       `
                            )                                         

#now to generate text we need to decode these o/p ids 
text_generated=tokenizer.decode(output_ids[0],skip_special_tokens=True)
print(f"\n{prompt}\n")
print(f"generated text: {text_generated}")










































































































































