# Diabetic Retinopathy Detection

A Django web application to detect diabetic retinopathy from retinal fundus images using a pretrained ResNet50 model on HuggingFace.

## Live Application: [DR Detection | Azure](https://dr-huggingface-hwaeeth7hhetd9cb.eastus2-01.azurewebsites.net)

## Features

- Upload a retinal fundus image for inference
- Pretrained model: [ResNet50-APTOS-DR](https://huggingface.co/sakshamkr1/ResNet50-APTOS-DR)

## Usage

1. Clone the repository:
   ```powershell
   git clone https://github.com/Polymath-Saksh/DR_Detection.git
   cd DR_Detection
   ```
2. Set up environment variables:

   Create a `.env` file in the root directory and add the following variables.

   ```powershell
   # then edit .env with:
   AZURE_ACCOUNT_KEY=<your_account_key>
   AZURE_ACCOUNT_NAME=<your_account_name>
   AZURE_CONTAINER=<your_container_name>
   AZURE_STORAGE_CONNECTION_STRING=<your_connection_string>
   AZURE_URL=<your_url>
   DEBUG=<your_debug_value>
   SECRET_KEY=<your_secret_key>
   USE_AZURE_STORAGE=<your_use_azure_storage_value>
   ```

3. Create a virtual environment and install dependencies:
   ```powershell
   python -m venv venv
   venv\Scripts\Activate
   pip install -r requirements.txt
   ```
4. Apply migrations and run locally:
   ```powershell
    python manage.py migrate
    python manage.py collectstatic
    python manage.py runserver
   ```

For production deployment, configure Azure Web App or your preferred host.

## Collaborators

- [Saksham Kumar](https://github.com/Polymath-Saksh)
- [Rhythm Narang](https://github.com/rhythmnarang1)
- [Hitesh Khatwani](https://github.com/Insane-HK)
- [Vaishnavi Ahire](https://github.com/VaishnaviAhire)
