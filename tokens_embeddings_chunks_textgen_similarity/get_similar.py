
from transformers import GPT2Tokenizer,GPT2Model
import torch.nn.functional as F
import torch

tokenizer=GPT2Tokenizer.from_pretrained("gpt2")
model=GPT2Model.from_pretrained("gpt2")

news_article= """The United States and India recently announced 
a rollback of certain tariffs imposed during previous trade disputes. 
The move is expected to boost bilateral trade, particularly in sectors 
like agriculture, electronics, and manufacturing. Economists believe 
this step will enhance market access and reduce costs for exporters on 
both sides, while signaling improved geopolitical alignment between the 
two democracies."""
 
possible_headlines=[
    "US and India remove tariffs to boost trade ties",
    "India launches lunar probe to explore moon's south pole",
    "Tariff rollback improves US-India manufacturing access",
    "Stock markets dip amid inflation concerns in Asia",
    "Improved trade relations could strengthen US-India alliance",
    "India bans certain Chinese tech products from ports"
]

def get_mean_embeddings(input_text):
    tokens=tokenizer(input_text,return_tensors="pt")
    with torch.no_grad():
        output=model(**tokens) #these also embeddings
        embeddings=output.last_hidden_state
        mean_embeddings=embeddings.mean(dim=1)
    return mean_embeddings

news_article_embeddings=get_mean_embeddings(news_article)

result=[]

for headline in possible_headlines:
    headlines_embeddings=get_mean_embeddings(headline)
    score= F.cosine_similarity(news_article_embeddings,headlines_embeddings ).item()
    result.append((headline,score))

result.sort(key=lambda x:x[1],reverse=True)

print("\n Top 3 similr headlines are:\n")

for i in range(3):
    headline, score = result[i]  #for top headlines and score 1st,2nd,3rd
    print  (f"{i + 1} - {headline} - Score {score}")

# getting all headlines and scores in descending order
for headline, score in result:
    print (f"{score: .4f} -> {headline}")

