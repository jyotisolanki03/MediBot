import os

from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# Step 1. Setup LLM (Mistral with HuggingFace)
HF_TOKEN=os.environ.get("HF_TOKEN")
huggingface_repo_id="mistralai/Mistral-7B-Instruct-v0.3"

def load_llm(huggingface_repo_id):
    llm=HuggingFaceEndpoint(
        repo_id=huggingface_repo_id,
        task="text-generation",
        temperature=0.5,
        model_kwargs={"token":HF_TOKEN,
                      "max_length":"512"}                 
    )
    return llm

# Step 2. Connect LLM with FAISS and Create Chain
DB_FAISS_PATH="vectorstore/db_faiss"

CUSTOM_PROMPT_TEMPLATE="""
Use the peices of information provided in the context to answer user's questions.
If you do not know the answer, just say that you don't know, don't try to make up an answer.
Don't provide anything out of the given context.

Context :{context}
Question :{question}

Start the answer directly. No small talk please.
"""

def set_custom_prompt(custom_prompt_template):
    prompt=PromptTemplate(template=custom_prompt_template, input_variables=["context","question"])
    return prompt

#Load databse
DB_FAISS_PATH="vectorstore/db_faiss"
embedding_model=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLm-L6-v2")
db=FAISS.load_local(DB_FAISS_PATH,embedding_model,allow_dangerous_deserialization=True)

#Create Q/A Chain
qa_chain=RetrievalQA.from_chain_type(
    llm=load_llm(huggingface_repo_id) ,
    chain_type= "stuff",
    retriever=db.as_retriever(search_kwargs={'k':5}) ,
    return_source_documents=True ,
    chain_type_kwargs={'prompt':set_custom_prompt(CUSTOM_PROMPT_TEMPLATE)}
  
)

#invoke with a single Query
user_query=input("Write Query Here: ")
response=qa_chain.invoke({'query':user_query})
print("RESULT: ", response["result"])
print("SOURCE DOCUMENTS: ", response["source_documents"])