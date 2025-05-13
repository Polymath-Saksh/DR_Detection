from django.shortcuts import render
from django.conf import settings
import os
import tempfile
import torch
from torchvision import transforms
from PIL import Image
from huggingface_hub import hf_hub_download
import shutil

# Load model from HuggingFace Hub
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# Replace with your actual HuggingFace repo ID and filename
repo_id = "sakshamkr1/ResNet50-APTOS-DR"
model_filename = hf_hub_download(repo_id=repo_id, filename="diabetic_retinopathy_full_model.pth")
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

            # Save uploaded image to the application's temp directory
            image_file = request.FILES["image"]
            image_path = os.path.join(temp_image_dir, image_file.name)
            with open(image_path, "wb+") as f:
                for chunk in image_file.chunks():
                    f.write(chunk)

            # Get prediction
            probs = predict(image_path)
            predicted_class = int(probs.argmax())

            # Generate URL for uploaded image
            uploaded_image_url = f"/static/{image_file.name}"
            os.makedirs(static_dir, exist_ok=True)
            static_image_path = os.path.join(static_dir, image_file.name)
            shutil.move(image_path, static_image_path)  # Force replace if file exists
        except Exception as e:
            error = str(e)
    # Render template with result or error
    context = {"predicted_class": predicted_class, "error": error, "uploaded_image_url": uploaded_image_url}
    return render(request, "detector/detector.html", context)

