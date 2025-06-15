import requests
import logging 
import torch
import json
from functools import wraps
import torch.nn.functional as F
from transformers import GPT2LMHeadModel, GPT2Tokenizer, GPT2Model


NEWS_API_URL = "https://newsapi.org/v2/top-headlines"
API_KEY = "224aed70fc5e450e93a7b2c745e7efd9"
article_count = 5

logging.basicConfig(
    filename="news_api.log",
    level= logging.INFO,
    format= "%(asctime)s [%(levelname)s]   %(message)s ")

def handle_exceptions(func):
    @wraps(func)
    def wrapper (*args, **kwargs):
        try:
            logging.info(f"Executing: {func.__name__}")
            return func(*args, **kwargs)
        except Exception as e:
            logging.exception(f"Error while Executing: {func.__name__} : {e}")
    return wrapper


tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
gen_model = GPT2LMHeadModel.from_pretrained("gpt2")
emb_model = GPT2Model.from_pretrained("gpt2")


tokenizer.pad_token = tokenizer.eos_token
gen_model.pad_token_id = gen_model.config.eos_token_id
emb_model.pad_token_id = emb_model.config.eos_token_id

@handle_exceptions
def get_news_articles(api_key, count) -> list[dict]:
    logging.info ("getting news articles from web....wait")
    global news_api
    news_api =  requests.get(
        NEWS_API_URL, params = {
        "apiKey" : api_key,
        "country" : "us",
        "pageSize" : count
    }
    )
    news_api.raise_for_status()
    news_articles = news_api.json().get("articles", [])
    logging.info (f"\nFetched {len(news_articles)} articles\n")
    print(f"total articles fetched:{len(news_articles)}")
    return news_articles

@handle_exceptions
def process_news_articles(Articles):
    for article in Articles:
        content = article.get("content") or ""
        title = article.get("title") or ""
        description = article.get("description") or ""

        article_text = f"{title}. {description}. {content}".strip()

        if not article_text: 
            continue

        prompt = f"Generate a headline for this news: \n {article_text} \n Headline:"
        headlines = generate_headlines(prompt) 

        article_text_embedding = get_mean_embedding(prompt)

        result = []
        for headline in headlines:  # by providing i, enumerate here we get unordered headlines after sort so avoid
            headline_mean_embedding =  get_mean_embedding(headline)
            score = F.cosine_similarity(headline_mean_embedding,article_text_embedding).item()
            logging.info("found the cosine similarity between each headline and text")
            #result.append((headline,score))
            result.append({"Headline":headline,"Score":f"{score:.4f}"})
        #result.sort(key=lambda x:x[1],reverse=True)
        result.sort(key= lambda x: x["Score"],reverse=True)

        # top_headlines=[]
        # for i,(headline,score) in enumerate(result[:5],1):
        #     result={f"{i}.Headline":f"{headline}", f"Score":f"{score:.4f}"}
        #     logging.info("listed top 5 headlines.....")
        #     top_headlines.append(result)

        article["Headlines"]=result #top 5 headlines
        logging.info("top 5 headlines are appended to each article")
    return Articles

@handle_exceptions
def get_updated_news_api(News_Api,Articles):
    updated=News_Api.json()
    updated["articles"]=Articles
    logging.info("news_api is updated with the updated Articles")

    with open("updated_news_api.json","w") as f:
        json.dump(updated,f,indent=4)
        logging.info("news_api json is updated and saved successfully")
    return updated

@handle_exceptions
def get_mean_embedding(input_text):
    input_text_tokens = tokenizer(input_text, return_tensors="pt")
    with torch.no_grad():
        embeddings = emb_model(**input_text_tokens)
    logging.info("mean embedding generated for prompt/headline")
    return embeddings.last_hidden_state.mean(dim=1) # Share [1,768] 768-d

@handle_exceptions
def generate_headlines(prompt):
    news_headline_tokens = tokenizer(prompt, return_tensors="pt").input_ids
    headlines = gen_model.generate (
        news_headline_tokens,
        num_return_sequences = 5, # Fix the issue for Greedy - Beam message
        max_new_tokens =15,
        do_sample=True,
        temperature = 0.8,
        top_k=50,
        top_p  = 0.95
    )
    logging.info("headlines generated for prompt")

    Headlines= [tokenizer.decode(headline, skip_special_tokens = True).replace(prompt, "").strip() for headline in headlines]
    if not Headlines:
        logging.info("no headlines")
    return Headlines


if __name__ == "__main__":
        articles = get_news_articles(API_KEY, article_count) 
        updated_articles=process_news_articles (articles)
        updated_news_api=get_updated_news_api(news_api,updated_articles)
        print(updated_news_api)
    