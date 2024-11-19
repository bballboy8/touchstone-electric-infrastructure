from diagrams import Diagram, Cluster
from diagrams.gcp.compute import ComputeEngine
from diagrams.custom import Custom
from diagrams.onprem.client import Client
from diagrams.onprem.ci import GithubActions
from diagrams.saas.communication import Twilio

# Define the diagram
with Diagram("Chatbot Infrastructure", filename="chatbot_infrastructure", show=False, direction="TB"):
    # FastAPI Workflow Vertical
    with Cluster("FastAPI Workflow"):
        # Input Layer
        message_history = Custom("Chat History\n[message 1, message 2, ...]", "images/chat_history.png")
        
        # Processing Layer
        fastapi_app = ComputeEngine("FastAPI Application")
        github_actions = GithubActions("GitHub Actions (CI/CD)")
        
        # Output Layer
        next_message = Custom("Next Message\n(Chatbot Response)", "images/next_message.png")
        twilio_sms = Twilio("Twilio (SMS/Chatbot)")
        
    # Standalone Embedding Workflow Vertical
    with Cluster("Standalone Embedding Workflow"):
        # Input Layer
        documents = Custom("Company Documents", "images/documents.png")
        
        # Processing Layer
        document_script = Client("Standalone Embedding Script")
        
        # Output Layer
        pinecone_db_embedding = Custom("Pinecone DB", "images/pinecone.png")

    # Third-Party APIs (Separate for Each Workflow)
    with Cluster("Third-Party APIs"):
        # FastAPI Workflow APIs
        openai_api_chat = Custom("OpenAI API Chat Completion", "images/openai.png")
        pinecone_db_fastapi = Custom("Pinecone DB", "images/pinecone.png")
        salesforce = Custom("Service Titan", "images/service_titan.png")

        # Standalone Embedding Workflow APIs
        openai_api_embedding = Custom("OpenAI API Embedding", "images/openai.png")

    # FastAPI Relationships
    message_history >> fastapi_app  # Input to FastAPI
    fastapi_app >> next_message  # Generate chatbot response
    next_message >> twilio_sms  # Send via Twilio or to chatbot
    github_actions >> fastapi_app  # CI/CD Pipeline for FastAPI
    fastapi_app << openai_api_chat  # Query OpenAI API for chat completion
    fastapi_app << pinecone_db_fastapi  # Query Pinecone for retrieval
    fastapi_app << salesforce  # Query Salesforce

    # Standalone Embedding Relationships
    documents >> document_script  # Input to Embedding Script
    document_script << openai_api_embedding  # Use OpenAI for embeddings
    document_script >> pinecone_db_embedding  # Store embeddings in Pinecone
