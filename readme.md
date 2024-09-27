# Sentiment Analysis Project with GPU Support on Kubernetes

## Table of Contents
1. [Project Overview](#project-overview)
2. [Project Structure](#project-structure)
3. [Prerequisites](#prerequisites)
4. [Environment Setup](#environment-setup)
   - [With Hyper-V (Windows 10/11 Pro or Enterprise)](#with-hyper-v-windows-1011-pro-or-enterprise)
   - [Without Hyper-V (Windows 10/11 Home)](#without-hyper-v-windows-1011-home)
5. [Local Development and Testing](#local-development-and-testing)
6. [Docker Build and Deployment](#docker-build-and-deployment)
7. [Kubernetes Deployment](#kubernetes-deployment)
   - [Using Docker Desktop Kubernetes](#using-docker-desktop-kubernetes)
   - [Using Minikube](#using-minikube)
8. [Troubleshooting](#troubleshooting)


## Project Overview

This project is a sentiment analysis application that uses deep learning to classify the sentiment of text inputs. It's designed to run on Kubernetes with GPU support for improved performance. The application is built using Python, FastAPI for the web framework, and PyTorch for the machine learning model.

## Project Structure

```
sentiment-analysis/
├── Dockerfile
├── .dockerignore
├── main.py
├── model.py
├── model_save.py
├── requirements.txt
├── tests/
│   └── test_sentiment.py
├── kubernetes/
│   ├── deployment.yaml
│   ├── hpa.yaml
│   └── service.yaml
├── templates/
│   └── index.html
└── static/
    └── (empty folder for future static files)
```

Note: The `model/model_cache` folder containing the pre-trained model is not included in the repository due to its large size. You can generate it using `model_save.py` before that create the folder folder `model/model_cache` through `os.makedir` or directly through IDE. Create `static` folder too.

## Prerequisites

- Windows 10 or later
  - For Hyper-V: Windows 10/11 Pro, Enterprise, or Education
  - For systems without Hyper-V: Windows 10/11 Home or other versions
- NVIDIA GPU with updated drivers
- Docker Desktop with Kubernetes support or Minikube
- Conda (for local development)
- Also make sure that wsl ubuntu version is same as we use in Dockerfile and use same cuda version too as in requirements.txt and Dockerfile.
## Environment Setup

### With Hyper-V (Windows 10/11 Pro or Enterprise)

1. Enable Hyper-V:
   - Open PowerShell as Administrator and run:
     ```
     Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All
     ```
   - Restart your computer when prompted

2. Install WSL2 with Ubuntu:
   ```
   wsl --install -d Ubuntu
   ```
   - Restart your computer after the installation is complete
   - After restart, a new window will open automatically to set up Ubuntu:
     - Enter a new UNIX username when prompted
     - Enter and confirm a new password
   - Once setup is complete, you'll be at the Ubuntu command prompt

3. Access WSL Ubuntu:
   - You can access WSL Ubuntu at any time by:
     - Opening the Start menu and typing "Ubuntu", then clicking on the Ubuntu app
     - Or opening a Command Prompt or PowerShell and typing `wsl`

4. Update and upgrade Ubuntu packages:
   ```bash
   sudo apt update
   sudo apt upgrade -y
   ```

5. Install necessary packages:
   ```bash
   sudo apt install -y curl wget git
   ```

6. Install NVIDIA GPU drivers on Windows:
   - Download and install the latest drivers from [NVIDIA's website](https://www.nvidia.com/Download/index.aspx)
   - Restart your computer after installation

7. Install Docker Desktop with WSL2 backend:
   - Download from [Docker's website](https://www.docker.com/products/docker-desktop)
   - During installation, ensure "Use WSL 2 instead of Hyper-V" is selected
   - After installation, go to Settings > Resources > WSL Integration and enable Ubuntu
   - Click "Apply & Restart" to restart Docker Desktop

8. Install NVIDIA Container Toolkit in WSL2 Ubuntu:
   ```bash
   distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
   curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
   curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
   sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
   ```
   - Restart Docker Desktop after installation

9. Enable Kubernetes in Docker Desktop:
   - Go to Settings > Kubernetes
   - Check "Enable Kubernetes"
   - Click "Apply & Restart"
   - Wait for Kubernetes to be ready (this may take several minutes)

10. Install Conda:
    ```bash
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    bash Miniconda3-latest-Linux-x86_64.sh
    ```
    - Close and reopen your terminal after installation

11. Create and activate Conda environment:
    ```bash
    conda create -n sentiment python=3.9
    conda activate sentiment
    ```

12. Install project dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Without Hyper-V (Windows 10/11 Home)

1. Install WSL2:
   - Open PowerShell as Administrator and run:
     ```
     wsl --install
     ```
   - Restart your computer when prompted

2. Install Ubuntu from Microsoft Store:
   - Open Microsoft Store
   - Search for "Ubuntu"
   - Click "Get" to install Ubuntu
   - Once installed, click "Launch"
   - A new window will open to set up Ubuntu:
     - Enter a new UNIX username when prompted
     - Enter and confirm a new password
   - Once setup is complete, you'll be at the Ubuntu command prompt

3. Access WSL Ubuntu:
   - You can access WSL Ubuntu at any time by:
     - Opening the Start menu and typing "Ubuntu", then clicking on the Ubuntu app
     - Or opening a Command Prompt or PowerShell and typing `wsl`

4. Update and upgrade Ubuntu packages:
   ```bash
   sudo apt update
   sudo apt upgrade -y
   ```

5. Install necessary packages:
   ```bash
   sudo apt install -y curl wget git
   ```

6. Follow steps 6-12 from the Hyper-V section above.

After completing the setup, it's recommended to restart your computer to ensure all changes take effect.

## Local Development and Testing

1. Download the pre-trained model:
   ```bash
   python model_save.py
   ```

2. Run the FastAPI application:
   ```bash
   python main.py
   ```

3. Test the application:
   - Open a web browser and go to `http://localhost:8000`
   - Or use curl:
     ```bash
     curl -X POST "http://localhost:8000/predict" -H "Content-Type: application/json" -d '{"text":"I love this product!"}'
     ```

4. Run unit tests:
   ```bash
   python -m unittest discover tests
   ```

## Docker Build and Deployment

1. Ensure Docker Desktop is running and WSL2 is properly configured

2. Log in to Docker Hub:
   ```bash
   docker login
   ```
   Enter your Docker Hub username and password when prompted.

3. Build the Docker image (with version):
   ```bash
   docker build -t sentiment-analysis-gpu:v1.0.0 .
   ```

4. Run the Docker container:
   ```bash
   docker run -p 8000:8000 --gpus all sentiment-analysis-gpu:v1.0.0
   ```

5. Test the containerized application:
   - Open a web browser and go to `http://localhost:8000`
   - Or use curl:
     ```bash
     curl -X POST "http://localhost:8000/predict" -H "Content-Type: application/json" -d '{"text":"I love this product!"}'
     ```

6. Push to Docker Hub:
   ```bash
   docker tag sentiment-analysis-gpu:v1.0.0 yourusername/sentiment-analysis-gpu:v1.0.0
   docker push yourusername/sentiment-analysis-gpu:v1.0.0
   ```

7. Pull from Docker Hub:
   ```bash
   docker pull yourusername/sentiment-analysis-gpu:v1.0.0
   ```

8. Test the pulled image:
   ```bash
   docker run -p 8000:8000 --gpus all yourusername/sentiment-analysis-gpu:v1.0.0
   ```

   Test again using the methods in step 5 to ensure the pulled image works correctly.

If you encounter any issues during the Docker build or run process, try restarting Docker Desktop and your WSL2 instance:

- Restart Docker Desktop from the system tray icon
- Restart WSL2 by opening PowerShell and running:
  ```
  wsl --shutdown
  ```
  Then relaunch your Ubuntu WSL2 instance.

## Kubernetes Deployment

You can deploy this application using either Docker Desktop's built-in Kubernetes or Minikube. Choose the method that best suits your setup.

### Using Docker Desktop Kubernetes

1. Ensure Docker Desktop is running and Kubernetes is enabled

2. Apply NVIDIA device plugin:
   ```bash
   kubectl create -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.13.0/nvidia-device-plugin.yml
   ```

3. Update the `kubernetes/deployment.yaml` file to use your Docker Hub image with version:
   ```yaml
   spec:
     containers:
     - name: sentiment-analysis
       image: yourusername/sentiment-analysis-gpu:v1.0.0
   ```

4. Deploy the application:
   ```bash
   kubectl apply -f kubernetes/deployment.yaml
   kubectl apply -f kubernetes/hpa.yaml
   kubectl apply -f kubernetes/service.yaml
   ```

5. Verify the deployment:
   ```bash
   kubectl get pods
   kubectl get services
   kubectl get hpa
   ```

6. Get the NodePort:
   ```bash
   kubectl get services sentiment-analysis-service
   ```

7. Access the service at `http://localhost:<NodePort>`

If you encounter issues, try restarting Docker Desktop and reapplying the Kubernetes configurations.

### Using Minikube

1. Install Minikube:
   ```bash
   winget install minikube
   ```

2. Start Minikube with GPU support:
   ```bash
   minikube start --driver=docker --container-runtime=docker \
     --docker-opt gpus=all \
     --addons=nvidia-gpu-device-plugin \
     --kubernetes-version=v1.26.3
   ```

3. Verify GPU support in Minikube:
   ```bash
   minikube ssh -- nvidia-smi
   ```

4. Enable the metrics-server addon for HPA to work:
   ```bash
   minikube addons enable metrics-server
   ```

5. Load your Docker image into Minikube:
   ```bash
   minikube image load yourusername/sentiment-analysis-gpu:v1.0.0
   ```

6. Update the `kubernetes/deployment.yaml` file to use the local image:
   ```yaml
   spec:
     containers:
     - name: sentiment-analysis
       image: yourusername/sentiment-analysis-gpu:v1.0.0
       imagePullPolicy: Never
   ```

7. Deploy the application:
   ```bash
   kubectl apply -f kubernetes/deployment.yaml
   kubectl apply -f kubernetes/hpa.yaml
   kubectl apply -f kubernetes/service.yaml
   ```

8. Verify the deployment:
   ```bash
   kubectl get pods
   kubectl get services
   kubectl get hpa
   ```

9. Access the service:
   ```bash
   minikube service sentiment-analysis-service
   ```

   This command will provide a URL to access your service.

If you encounter issues with Minikube, try stopping and restarting it:

```bash
minikube stop
minikube start --driver=docker --container-runtime=docker --docker-opt gpus=all --addons=nvidia-gpu-device-plugin
```

## Troubleshooting

- Check pod logs:
  ```bash
  kubectl logs <pod-name>
  ```

- Describe pods:
  ```bash
  kubectl describe pod <pod-name>
  ```

- Port-forward for direct access:
  ```bash
  kubectl port-forward service/sentiment-analysis-service 8000:80
  ```

- If you encounter issues with GPU support in Docker on Windows Home, you may need to use the WSL2 backend exclusively. You can do this by setting the following in your Docker Desktop settings:
  - Go to Settings > General
  - Ensure "Use the WSL 2 based engine" is checked
  - Restart Docker Desktop after making changes

Additional Minikube-specific troubleshooting:

- If pods are not starting in Minikube, check the logs:
  ```bash
  minikube logs
  ```

- To ssh into the Minikube VM:
  ```bash
  minikube ssh
  ```

- If you need to delete and recreate your Minikube cluster:
  ```bash
  minikube delete
  minikube start --driver=docker --container-runtime=docker --docker-opt gpus=all --addons=nvidia-gpu-device-plugin
  ```

Additional WSL-specific troubleshooting:

- If you're unable to access WSL or encounter issues, try restarting the WSL service:
  ```
  wsl --shutdown
  ```
  Then relaunch Ubuntu from the Start menu or by typing `wsl` in Command Prompt/PowerShell.

- To check the status of your WSL installations:
  ```
  wsl --list --verbose
  ```

- If you need to reset your Ubuntu WSL installation (this will delete all data in the WSL instance):
  1. Open PowerShell as Administrator
  2. Run: `wsl --unregister Ubuntu`
  3. Reinstall Ubuntu from the Microsoft Store

General troubleshooting steps:

1. Restart Docker Desktop
2. Restart WSL2:
   ```
   wsl --shutdown
   ```
3. Restart your computer
4. Ensure all software (Docker, WSL2, NVIDIA drivers) is up to date
5. Check Windows Event Viewer for any relevant error messages

Additional Notes:
- If you're using Windows 10/11 Home, you won't have access to Hyper-V. In this case, Docker Desktop will use WSL2 backend by default.
- For systems without Hyper-V, ensure that virtualization is enabled in your BIOS settings.
- Remember to test the application after each major step (local setup, Docker build, Kubernetes deployment) to ensure everything is working as expected.
- Adjust these steps according to your specific PC or laptop specifications and the version of Windows you're using.
- When updating the application, increment the version number (e.g., v1.0.0 to v1.0.1 for minor updates or v1.1.0 for feature updates) in both the Docker build and Kubernetes deployment steps.
- The steps for Docker Desktop Kubernetes and Minikube are similar, but Minikube requires a few extra setup steps.
- Minikube creates a single-node Kubernetes cluster, which is great for testing and development.
- Remember to adjust the Minikube start command based on your system's capabilities and requirements.
- When switching between Docker Desktop Kubernetes and Minikube, ensure you're using the correct context:
  ```bash
  kubectl config use-context minikube  # For Minikube
  kubectl config use-context docker-desktop  # For Docker Desktop
  ```

