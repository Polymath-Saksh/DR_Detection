from django.shortcuts import render
from django.conf import settings
import os
import torch
from torchvision import transforms
from PIL import Image
import shutil
from azure.storage.blob import BlobServiceClient, ContentSettings
from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv
import tempfile
import mimetypes
# Load environment variables from a .env file
load_dotenv()


# Load model from HuggingFace Hub
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Replace with your actual HuggingFace repo ID and filename
repo_id = "sakshamkr1/ResNet50-APTOS-DR"
model_filename = hf_hub_download(repo_id=repo_id, filename="diabetic_retinopathy_full_model.pth")
# model_filename = os.path.join(BASE_DIR, "model","diabetic_retinopathy_full_model.pth")  # Local path to the model file
model = torch.load(model_filename, map_location=device, weights_only=False)
model.eval()

# Define image transforms
transform = transforms.Compose([
    transforms.Resize((224, 224)),  # Resize image to match input size
    transforms.ToTensor(),  # Convert image to tensor
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),  # Normalize using ImageNet stats
])

def predict(image_path):
    # Load and preprocess the input image
    image = Image.open(image_path).convert("RGB")
    input_tensor = transform(image).unsqueeze(0).to(device)

    # Perform inference
    with torch.no_grad():
        outputs = model(input_tensor)
        probabilities = torch.nn.functional.softmax(outputs, dim=1)

    # Return probabilities as numpy array
    return probabilities.cpu().numpy()[0]

# Define a temporary folder within the application for storing images
temp_image_dir = os.path.join(settings.BASE_DIR, "temp_images")
os.makedirs(temp_image_dir, exist_ok=True)

def detector(request):
    predicted_class = None
    error = None
    uploaded_image_url = None
    if request.method == "POST" and request.FILES.get("image"):
        try:
            # Delete all files in the static directory
            static_dir = os.path.join(settings.BASE_DIR, "static")
            if os.path.exists(static_dir):
                for file_name in os.listdir(static_dir):
                    file_path = os.path.join(static_dir, file_name)
                    if os.path.isfile(file_path):
                        os.remove(file_path)


            # Use BlobServiceClient to upload image to Azure Blob Storage
            image_file = request.FILES["image"]
            blob_name = f"{image_file.name}"
            # Get Azure connection string
            connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
            if not connection_string:
                raise ImproperlyConfigured("AZURE_STORAGE_CONNECTION_STRING environment variable is not set")
            container_name = os.getenv("AZURE_CONTAINER", "static")
            blob_service_client = BlobServiceClient.from_connection_string(connection_string)
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

            # Upload the image with proper content settings
            image_bytes = image_file.read()
            content_type, _ = mimetypes.guess_type(image_file.name)
            cs = ContentSettings(content_type=content_type) if content_type else None
            blob_client.upload_blob(image_bytes, overwrite=True, content_settings=cs)
            print(f"[Azure Upload] Image uploaded to Azure Blob Storage: {blob_name}")

            # Generate the blob URL
            account_name = blob_service_client.account_name
            # Generate a read-only SAS token so the blob can be accessed publicly
            from azure.storage.blob import generate_blob_sas, BlobSasPermissions
            from datetime import datetime, timedelta
            # Extract account key from connection string
            account_key = connection_string.split("AccountKey=")[1].split(";")[0]
            sas_token = generate_blob_sas(
                account_name=account_name,
                account_key=account_key,
                container_name=container_name,
                blob_name=blob_name,
                permission=BlobSasPermissions(read=True),
                expiry=datetime.utcnow() + timedelta(hours=1)
            )
            image_url = (
                f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}"
            )

            # Download the image temporarily for prediction
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(image_file.name)[1]) as temp_img:
                download_stream = blob_client.download_blob()
                temp_img.write(download_stream.readall())
                temp_img_path = temp_img.name
            print(f"[Azure Download] Image pulled from Azure Storage to: {temp_img_path}")

            # Get prediction
            probs = predict(temp_img_path)
            predicted_class = int(probs.argmax())

            # Set uploaded image URL to Azure blob URL
            uploaded_image_url = image_url
        except Exception as e:
            error = str(e)
    # Render template with result or error
    context = {"predicted_class": predicted_class, "error": error, "uploaded_image_url": uploaded_image_url}
    return render(request, "detector/detector.html", context)

