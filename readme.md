# Diabetic Retinopathy Detection ![Hugging Face](https://img.shields.io/badge/Hugging%20Face-FFD21E?logo=huggingface&logoColor=000) ![Django](https://img.shields.io/badge/Django-%23092E20.svg?logo=django&logoColor=white) ![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff) ![Azure](https://img.shields.io/badge/azure-%230072C6.svg?style=for-the-badge&logo=microsoftazure&logoColor=white) ![Microsoft](https://img.shields.io/badge/Microsoft-0078D4?style=for-the-badge&logo=microsoft&logoColor=white)

## Introduction
This repository contains the AI Ambassadors Project of Microsoft Learn Student Ambassadors and Hacksagon @ IIITM Gwalior. The project is about Diabetic Retinopathy Image Detection Model. The project is divided into two parts:

- An EfficientB5 Model trained on the [APTOS 2019 dataset](https://www.kaggle.com/competitions/aptos2019-blindness-detection/). Achieved a Cohen Kappa Score of 0.96 on the complete dataset.
  [DR Detection Model | Huggingface](https://huggingface.co/sakshamkr1/ResNet50-APTOS-DR) 

- A Web application, powered by Django to detect diabetic retinopathy from retinal fundus images using the trained ResNet50 model on HuggingFace. Hosted on Azure Web Apps.



## Presentation

The presentation for the project can be found at: [Oculus SA - Diabetic Retinopathy Detection](https://stdntpartners-my.sharepoint.com/:p:/g/personal/saksham_kumar_studentambassadors_com/EX07rzghefdLnovuAoaJKPgBXie2R0X-knxrClYhKMmX4A?e=WKjC4o). (Access restricted to Microsoft Learn Student Ambassadors)


## Usage

1. Clone the repository and change directory :
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

For production deployment, configure Azure Web Apps or your preferred host.

## Contributors (Team Oculus)

- [Saksham Kumar](https://github.com/Polymath-Saksh)
- [Rhythm Narang](https://github.com/rhythmnarang1)
- [Hitesh Khatwani](https://github.com/Insane-HK)
- [Vaishnavi Ahire](https://github.com/VaishnaviAhire)
- [Aloukik Joshi](https://github.com/aloukikjoshi)

## Acknowledgments

- [EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks](https://arxiv.org/abs/1905.11946#) by Mingxing Tan, Quoc V. Le, 2019.

## License

This project is licensed under the [Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0)](LICENSE), which permits others to share and adapt the material for non-commercial purposes, provided that appropriate credit is given to the original author.
