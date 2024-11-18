from diagrams import Diagram, Cluster
from diagrams.custom import Custom
from diagrams.gcp.storage import Storage
from diagrams.onprem.ci import GithubActions
from diagrams.gcp.compute import ComputeEngine
from diagrams.onprem.client import User

# Define the diagram
with Diagram("Invoice and Packing Slip Processing Infrastructure", filename="invoice_packing_slip_comparison_infrastructure", show=False, direction="TB"):
    # User at the top
    user = User("User")

    # React Frontend Workflow
    with Cluster("React Frontend Workflow"):
        # Input Layer
        pdf_invoice = Custom("\n\nPDF Invoice", "images/invoice.png")
        packing_slip_image = Custom("Packing Slip Image", "images/packing_slip.png")
        
        # Hosted React Frontend
        react_frontend = Custom("React Frontend", "images/react.png")
        cloud_storage = Storage("Cloud Storage (Hosting)")
        github_actions_frontend = GithubActions("GitHub Actions (CI/CD)")

    # FastAPI Backend Workflow
    with Cluster("FastAPI Backend Workflow"):
        # Processing Layer
        fastapi_app = ComputeEngine("FastAPI Application")
        github_actions_backend = GithubActions("GitHub Actions (CI/CD)")
        
        # Output Layer
        comparison_result = Custom("\n\nComparison Result\n(Differences)", "images/file_comparison.png")

    # Third-Party APIs
    with Cluster("Third-Party APIs"):
        openai_image_api = Custom("OpenAI API (Image Processing)", "images/openai.png")
        openai_summary_api = Custom("\nOpenAI API (Summary)", "images/openai.png")

    # User Relationships
    user >> pdf_invoice  # User provides PDF Invoice
    user >> packing_slip_image  # User provides Packing Slip Image

    # React Frontend Relationships
    pdf_invoice >> react_frontend  # User uploads PDF Invoice
    packing_slip_image >> react_frontend  # User uploads Packing Slip Image
    react_frontend >> cloud_storage  # React is hosted on cloud storage
    github_actions_frontend >> cloud_storage  # CI/CD deploys React app to cloud storage

    # FastAPI Backend Relationships
    fastapi_app << react_frontend  # Backend receives data from Frontend
    fastapi_app << openai_image_api  # FastAPI queries OpenAI API for packing slip image processing
    fastapi_app << openai_summary_api  # FastAPI queries OpenAI API for summarizing differences
    fastapi_app >> comparison_result  # Backend outputs the comparison result
    github_actions_backend >> fastapi_app  # CI/CD for FastAPI Backend
