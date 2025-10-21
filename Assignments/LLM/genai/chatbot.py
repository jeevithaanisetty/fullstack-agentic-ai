import google.generativeai as genai
import os

# saving Chat history in DB
client=MongoClient("mongodb://localhost:27017/")
db=client["chat_bot"]
chat_collection=db["chat_history"]

genai.configure(api_key=os.getenv("GEMINI-API-KEY"))
model=genai.GenerativeModel("gemini-2.5-pro")

# text="""In 2025, AI is expected to move from experimentation to full-scale integration, becoming an integral part of daily life and work,
# driven by advancements like multimodal capabilities and AI agents. Key trends include the evolution of AI agents for more complex tasks, 
# assistive search, the use of AI to enhance citizen experience in the public sector, and a continued focus on responsible and secure deployment. 
# The technology is also transforming industries like healthcare with improved diagnostics and customer service with more intelligent bots."""

# chat=model.start_chat(history=[])
# reply1=chat.send_message(f"Summarize this {text}")
# reply2=chat.send_message(f"Explain this summary: { reply1.content }")
# print(f"summary:{reply1.content},\n explanation:{reply2.content}")

print("=========GEMINI CHATBOT========")
print("type exit to quit chat\n\n")

chat=model.start_chat(history=[])

while True:
    user_input=input("You: ")
    if user_input.lower()=="exit":
        print("quitting........")
        break
    chat_collection.insert_one(
        {"role":"user","message":user_input}
    )
    response=chat.send_message(user_input)
    chat_collection.insert_one(
        {"role":"bot","message":response.text}
    )
    print("Bot: ",response.text)

