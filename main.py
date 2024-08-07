from llama_index.core import (
        VectorStoreIndex, 
        SimpleDirectoryReader, 
        Settings, 
        PromptTemplate, 
        get_response_synthesizer
)
from llama_index.llms.ollama import Ollama
from llama_index.readers.file import (PDFReader, CSVReader)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import PromptTemplate
from mis.utils.custom_csv_reader import CustomCSVReader
from pathlib import Path
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.core.retrievers import VectorIndexRetriever

# Setting the llm
Settings.llm = Ollama(model="llama3.1", request_timeout=1000.0, max_tokens=1000, num_ctx=4096)
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

parser = CustomCSVReader()

file_path: Path = Path("./db_data/mis/student_data.csv")

csv_prefixes = [
    ("My name is ", ". I am a student at Vasireddy Venkatadri Institute of Technology.\n"),
    ("My roll no is ", ". \n"),
    ("My nptel status is ", ".\n"),
    ("My mobile no is ", ".\n"),
    ("I am pursuing B.tech in branch ", ".\n"),
    ("I am in section ", ".\n")
]


documents = parser.load_data(
        file=file_path,
        csv_prefixes=csv_prefixes
        )

index = VectorStoreIndex.from_documents(documents)

retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=5
)


text_qa_template_str = (
    "Context information is"
    " below.\n---------------------\n{context_str}\n---------------------\nUsing"
    " both the context information and also using your own knowledge, answer"
    " the question: {query_str}\n"
    "Only use simple words that any 5 year old can understand."
    "Answer straight to the user query and don't say anything else."
)

text_qa_template = PromptTemplate(text_qa_template_str)

refine_template_str = (
    "The original question is as follows: {query_str}\nWe have provided an"
    " existing answer: {existing_answer}\nWe have the opportunity to refine"
    " the existing answer (only if needed) with some more context"
    " below.\n------------\n{context_msg}"
    "only use the existing context update or repeat the existing answer.\n"
    "Only use simple words that any 5 year old can understand."
    "Answer straight to the user query and don't say anything else."
)
refine_template = PromptTemplate(refine_template_str)

query_engine = RetrieverQueryEngine( 
        retriever=retriever,
        response_synthesizer=get_response_synthesizer()
)

while True:
    user_query: str = input(">>> ")
    if user_query == "/bye":
        break

    response = query_engine.query(user_query)
    print(response)
