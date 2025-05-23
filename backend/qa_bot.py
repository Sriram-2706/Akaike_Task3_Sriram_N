from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from transformers import pipeline
import os

def build_qa_bot(text_path: str):
    loader = PyPDFLoader(text_path)
    docs=loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    index_dir="backend/vectorstore"
    os.makedirs(index_dir,exist_ok= True)
    
    db_path = os.path.join(index_dir, "faiss_index")
    
    if os.path.exists(db_path+".faiss") and os.path.exists(db_path+".pkl"):
        vectorstore=FAISS.load_local(db_path,embeddings)
        vectorstore.add_documents(chunks)
    else:
        vectorstore=FAISS.from_documents(chunks,embeddings)
        vectorstore.save_local(db_path)
    
    hf_pipeline = pipeline("text2text-generation", model="google/flan-t5-large", max_length=512)
    llm = HuggingFacePipeline(pipeline=hf_pipeline)

    retriever = vectorstore.as_retriever()
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    sample_qns = [
 "According to the document, what services does the company offer?",
"Summarize the company’s mission and core values based on the document.",
"What solutions are mentioned in the document for customer engagement?",
"What industries or sectors does the company focus on?",
"Based on the document, what are the company’s strategic goals or future plans?"
]
    for q in sample_qns:
        print(f"Question:{q}")
        print(f"✅ Answer: {qa_chain.run(q)}\n")
    return qa_chain