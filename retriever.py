from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader, JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.tools import tool
import os

# Initialize the vector database at module level for reuse
_vector_db = None
PERSIST_DIRECTORY = "chroma_db"

def initialize_vector_db():
    """Initialize the vector database by loading and processing documents."""
    
    try:
        # Create a persistent directory for ChromaDB
        os.makedirs(PERSIST_DIRECTORY, exist_ok=True)
        
        # Initialize embeddings
        embeddings = GoogleGenerativeAIEmbeddings(model='models/text-embedding-004')
        
        # Check if DB already exists on disk
        if os.path.exists(os.path.join(PERSIST_DIRECTORY, "chroma.sqlite3")):
            print("Loading existing ChromaDB from disk...")
            # Load existing DB instead of recreating
            _vector_db = Chroma(
                persist_directory=PERSIST_DIRECTORY,
                embedding_function=embeddings
            )
            return _vector_db
        
        print("Creating new ChromaDB...")
        # If DB doesn't exist, create it from documents
        loader = DirectoryLoader("docs", glob='code_genral.txt', loader_cls=TextLoader)
        documents = loader.load()
        
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,  
            chunk_overlap=0,    
            separators=["---"]
        )
        docs = text_splitter.split_documents(documents)
        
        # Create vector database with ChromaDB instead of FAISS
        _vector_db = Chroma.from_documents(
            documents=docs, 
            embedding=embeddings,
            persist_directory=PERSIST_DIRECTORY
        )
        
        return _vector_db
    except Exception as e:
        print(f"Error initializing vector DB: {e}")

@tool
def building_code_retriever(query: str):
    """Retrieves building code information per room.
    
    Args:
        query (str): The name of room you want to get building code for it 
        
    Returns:
        str: room building code
    """
    
    # Make sure the vector database is initialized
    global _vector_db
    if _vector_db is None:
        _vector_db = initialize_vector_db()
        
    # Retrieve similar documents
    results = _vector_db.similarity_search(query, k=1)
    
    if results:
        return "\n\n".join([doc.page_content for doc in results])
    else:
        return "No matching information found."