from langchain_google_genai import ChatGoogleGenerativeAI
#from langchain_community.chains import LLMChain   (no longer a part of langchain-removed)
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm=ChatGoogleGenerativeAI(model="gemini-2.5-pro")
prompt=PromptTemplate.from_template(f"Explain {topic} simply")
# chain=LLMChain(llm=llm,prompt=prompt)
# response=chain.run("AI")

chain=prompt|llm|StrOutputParser()
response=chain.invoke({"topic":"AI"})

print(response)


"""LangChain 0.3.x (August–October 2024 onwards) migrated everything to a new Runnable-based system, which replaced LLMChain.
That means you now build chains using RunnableSequence or the pipe (|) operator."""