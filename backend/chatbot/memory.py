from dotenv import load_dotenv
import os
from pinecone import Pinecone, ServerlessSpec
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

# Load environment variables
load_dotenv()

# Initialize Pinecone client (new method)
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

index_name = "mental-health-memory"

# Create the index if it doesn't exist
if index_name not in [index.name for index in pc.list_indexes()]:
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

# Initialize embeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Connect LangChain to Pinecone
vectorstore = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)