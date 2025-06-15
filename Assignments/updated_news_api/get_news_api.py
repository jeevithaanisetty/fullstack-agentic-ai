import requests
from transformers import GPT2Tokenizer,GPT2Model,GPT2LMHeadModel

# simple way of fetching/calling web api
# news_api=requests.get("https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=224aed70fc5e450e93a7b2c745e7efd9")
# print(news_api.json().get("articles",[]))

NEWS_API_URL="https://newsapi.org/v2/top-headlines"
API_KEY="224aed70fc5e450e93a7b2c745e7efd9"
count=3

news_api=requests.get(
                       NEWS_API_URL,
                       params={
                           "apikey":API_KEY,
                           "country":"us",
                           "count":count
                       }
                       )
news_api.raise_for_status()  #raises an http error if request fails
news_articles=news_api.json().get("articles",[])
print(news_articles)


# USING METHOD 

# def get_news_articles(api_key,Count):
#     news_api=requests.get(NEWS_API_URL,
#                         params={
#                             "country":"us",
#                             "apikey":api_key,
#                             "count":Count
#                             })
#     news_api.raise_for_status()
#     news_article=news_api.json().get("articles",[])  #getting only articles from news json if not articles present return empty list
#     # print(news_article)

# if __name__=="__main__":
#     articles=get_news_articles(API_KEY,count)