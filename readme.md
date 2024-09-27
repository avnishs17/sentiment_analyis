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
8. [Troubleshooting](#troubleshooting)
9. [Contributing](#contributing)
10. [License](#license)
11. [Acknowledgments](#acknowledgments)

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

Note: The `model/model_cache` folder containing the pre-trained model is not included in the repository due to its large size. You can generate it using `model_save.py`.

## Prerequisites

- Windows 10 or later
  - For Hyper-V: Windows 10/11 Pro, Enterprise, or Education
  - For systems without Hyper-V: Windows 10/11 Home or other versions
- NVIDIA GPU with updated drivers
- Docker Desktop with Kubernetes support
- Conda (for local development)

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

3. Install NVIDIA GPU drivers on Windows:
   - Download and install the latest drivers from [NVIDIA's website](https://www.nvidia.com/Download/index.aspx)

4. Install Docker Desktop with WSL2 backend:
   - Download from [Docker's website](https://www.docker.com/products/docker-desktop)
   - During installation, ensure "Use WSL 2 instead of Hyper-V" is selected
   - After installation, go to Settings > Resources > WSL Integration and enable Ubuntu

5. Install NVIDIA Container Toolkit in WSL2 Ubuntu:
   ```bash
   distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
   curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
   curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
   sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
   ```

6. Enable Kubernetes in Docker Desktop:
   - Go to Settings > Kubernetes
   - Check "Enable Kubernetes"
   - Click "Apply & Restart"

7. Install Conda:
   ```bash
   wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
   bash Miniconda3-latest-Linux-x86_64.sh
   ```

8. Create and activate Conda environment:
   ```bash
   conda create -n sentiment python=3.9
   conda activate sentiment
   ```

9. Install project dependencies:
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

3. Install Docker Desktop:
   - Download Docker Desktop from [Docker's website](https://www.docker.com/products/docker-desktop)
   - During installation, ensure "Install required Windows components for WSL 2" is selected
   - After installation, open Docker Desktop settings
   - Go to "Resources" > "WSL Integration"
   - Enable integration with your Ubuntu distro

4. Follow steps 3-9 from the Hyper-V section above.

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

1. Build the Docker image:
   ```bash
   docker build -t sentiment-analysis-gpu .
   ```

2. Run the Docker container:
   ```bash
   docker run -p 8000:8000 --gpus all sentiment-analysis-gpu
   ```

3. Test the containerized application:
   - Open a web browser and go to `http://localhost:8000`
   - Or use curl:
     ```bash
     curl -X POST "http://localhost:8000/predict" -H "Content-Type: application/json" -d '{"text":"I love this product!"}'
     ```

4. Push to Docker Hub:
   ```bash
   docker tag sentiment-analysis-gpu:latest yourusername/sentiment-analysis-gpu:latest
   docker push yourusername/sentiment-analysis-gpu:latest
   ```

5. Pull from Docker Hub:
   ```bash
   docker pull yourusername/sentiment-analysis-gpu:latest
   ```

6. Test the pulled image:
   ```bash
   docker run -p 8000:8000 --gpus all yourusername/sentiment-analysis-gpu:latest
   ```

   Test again using the methods in step 3 to ensure the pulled image works correctly.

## Kubernetes Deployment

1. Apply NVIDIA device plugin:
   ```bash
   kubectl create -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.13.0/nvidia-device-plugin.yml
   ```

2. Update the `kubernetes/deployment.yaml` file to use your Docker Hub image:
   ```yaml
   spec:
     containers:
     - name: sentiment-analysis
       image: yourusername/sentiment-analysis-gpu:latest
   ```

3. Deploy the application:
   ```bash
   kubectl apply -f kubernetes/deployment.yaml
   kubectl apply -f kubernetes/hpa.yaml
   kubectl apply -f kubernetes/service.yaml
   ```

4. Verify the deployment:
   ```bash
   kubectl get pods
   kubectl get services
   kubectl get hpa
   ```

5. Get the NodePort:
   ```bash
   kubectl get services sentiment-analysis-service
   ```

6. Access the service at `http://localhost:<NodePort>`

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

Additional Notes:
- If you're using Windows 10/11 Home, you won't have access to Hyper-V. In this case, Docker Desktop will use WSL2 backend by default.
- For systems without Hyper-V, ensure that virtualization is enabled in your BIOS settings.
- Remember to test the application after each major step (local setup, Docker build, Kubernetes deployment) to ensure everything is working as expected.
- Adjust these steps according to your specific PC or laptop specifications and the version of Windows you're using.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc

