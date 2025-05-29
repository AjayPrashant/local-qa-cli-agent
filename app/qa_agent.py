'''from app.retriever import search
from transformers import pipeline

qa = pipeline("question-answering", model="distilbert-base-uncased", tokenizer="distilbert-base-uncased")

def answer_question(query: str) -> str:
    results = search(query)
    context = "\n".join([r.get("text", "") for r in results if "text" in r])

    print("Context Sample:", context[:300])  # Debug print (optional)

    if not context.strip():
        return "Sorry, I couldn't find anything relevant."

    answer = qa(question=query, context=context[:1000])  # Truncate if needed
    return answer['answer']
'''

'''from app.retriever import search
from transformers import pipeline

qa = pipeline("question-answering", model="distilbert-base-uncased", tokenizer="distilbert-base-uncased")'''

'''
def answer_question(query: str) -> str:
    results = search(query)

    print("\n[DEBUG] Retrieved Results:")
    for r in results:
        print(r)  # Print metadata from retriever

    context = "\n".join([r.get("text", "") for r in results if "text" in r])
    print("\n[DEBUG] Context Sample:\n", context[:500])  # Show first 500 chars of context

    if not context.strip():
        return "Sorry, I couldn't find anything relevant."

    answer = qa(question=query, context=context[:1000])
    return answer['answer'] # Debug Fix again 

def answer_question(query: str) -> str:
    results = search(query)

    print("\n[DEBUG] Retrieved:")
    for i, r in enumerate(results):
        print(f"\n--- Result {i+1} ---")
        print(r)

    context = "\n".join([r.get("text", "") for r in results if "text" in r])
    print("\n[DEBUG] Context:\n", context[:500])

    if not context.strip():
        return "Sorry, I couldn't find anything relevant."

    answer = qa(question=query, context=context[:1000])
    return answer['answer']
    '''

from app.retriever import search
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document

# Connect to your local LLaMA 3.2 model
# llm = Ollama(model="llama3.2")
llm = Ollama(model="llama3.2", base_url="http://host.docker.internal:11434")


def answer_question(query: str) -> str:
    # Get the top chunks as LangChain Documents
    results = search(query)
    docs = [Document(page_content=r["text"], metadata={"source": r["source"]}) for r in results if "text" in r]

    if not docs:
        return "Sorry, I couldn't find anything relevant."

    context = "\n\n".join(doc.page_content for doc in docs)
    full_prompt = f"""Use the following context to answer the question:\n\n{context}\n\nQuestion: {query}"""

    return llm(full_prompt)
