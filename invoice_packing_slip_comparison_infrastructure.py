from diagrams import Diagram, Cluster
from diagrams.custom import Custom
from diagrams.gcp.storage import Storage
from diagrams.gcp.compute import Functions
from diagrams.onprem.ci import GithubActions

# Define the diagram
with Diagram("Invoice and Packing Slip Processing Infrastructure", filename="invoice_packing_slip_comparison_infrastructure", show=False, direction="TB"):
    # Cloud Function Workflow
    with Cluster("Cloud Function Workflow"):
        # Processing Layer
        cloud_function = Functions("Weekly Cloud Function")
        github_actions_backend = GithubActions("GitHub Actions (CI/CD)")
        
        # Output Layer
        comparison_result = Custom("\n\nComparison Result\n(Differences)", "images/file_comparison.png")
        email_service = Custom("Email Service", "images/email_parser.png")

    # Third-Party APIs
    with Cluster("Third-Party APIs"):
        openai_image_api = Custom("OpenAI API (Image Processing)", "images/openai.png")
        openai_summary_api = Custom("\nOpenAI API (Summary)", "images/openai.png")

    # Zapier Flow
    with Cluster("Zapier Workflow"):
        zapier = Custom("Zapier", "images/zapier.png")
        email_parser = Custom("Email Parser", "images/email_parser.png")
        google_sheets_zapier = Custom("\n\nGoogle Sheets\n(Purchase Orders)", "images/google_sheets.png")

        email_parser >> zapier >> google_sheets_zapier

    # Google Form Flow
    with Cluster("Google Form Workflow"):
        google_form = Custom("\n\nGoogle Form\n(Packing Slips)", "images/google_forms.png")
        google_sheets_form = Custom("\n\nGoogle Sheets\n(Packing Slips)", "images/google_sheets.png")

        google_form >> google_sheets_form

    # Cloud Function Relationships
    cloud_function << openai_image_api  # Cloud Function queries OpenAI API for packing slip image processing
    cloud_function << openai_summary_api  # Cloud Function queries OpenAI API for summarizing differences
    cloud_function >> comparison_result  # Cloud Function outputs the comparison result
    comparison_result >> email_service  # Comparison result is sent via email
    github_actions_backend >> cloud_function  # CI/CD for Cloud Function
