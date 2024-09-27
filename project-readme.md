# Sentiment Analysis Project Deployment Guide

This guide walks through the process of deploying a Sentiment Analysis application using Docker and Kubernetes (Minikube).

## Prerequisites

- Docker installed
- Minikube installed
- kubectl installed
- Python 3.x installed

## 1. Dockerfile and .dockerignore Setup

### Create Dockerfile

Create a file named `Dockerfile` in your project root:

```dockerfile
FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TRANSFORMERS_CACHE=/app/model_cache

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/model_cache

RUN python -m unittest discover tests

EXPOSE 8000

RUN useradd -m myuser
USER myuser

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Create .dockerignore

Create a file named `.dockerignore`:

```
env/
*.cfg
.git
.cache
__pycache__
*.pyc
*.pyo
*.pyd
.ipynb_checkpoints
*.log
```

## 2. Build and Push Docker Image

```bash
docker build -t avnishsingh17/sentiment-analysis:v1 .
# to run docker image to test it's working
docker run -p 8000:8000 avnishsingh17/sentiment-analysis:v1

docker push avnishsingh17/sentiment-analysis:v1
```

## 3. Kubernetes Deployment

### Create deployment.yaml

Create `kubernetes/deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sentiment-analysis
  labels:
    app: sentiment-analysis
spec:
  replicas: 3
  selector:
    matchLabels:
      app: sentiment-analysis
  template:
    metadata:
      labels:
        app: sentiment-analysis
    spec:
      containers:
      - name: sentiment-analysis
        image: avnishsinghs17/sentiment-analysis:v1
        ports:
        - containerPort: 8000
        resources:
          limits:
            memory: "512Mi"
            cpu: "500m"
          requests:
            memory: "256Mi"
            cpu: "250m"
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 15
          periodSeconds: 10
```

### Create service.yaml

Create `kubernetes/service.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: sentiment-analysis-service
spec:
  selector:
    app: sentiment-analysis
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: LoadBalancer
```

## 4. Deploy to Minikube

Start Minikube:
```bash
minikube start
```
pull from docker hub or use the image you built locally
```bash
minikube ssh docker pull avnishsingh17/sentiment-analysis:v2
```
```to load local image
minikube image load avnishsingh17/sentiment-analysis:v1

apiVersion: v1
kind: Service
metadata:
  name: sentiment-analysis-service
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "8000"
    prometheus.io/path: "/metrics"
spec:
  selector:
    app: sentiment-analysis
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: LoadBalancer

Apply Kubernetes configurations:
```bash     
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
```

## 5. Testing the Deployment

Check pod status:
```bash
kubectl get pods
```

Get service URL:
```bash
minikube service sentiment-analysis-service
```

Test the service:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"text": "I love this product!"}' http://http:/127.0.0.1:50879/predict
```

## Troubleshooting

If facing issues:

1. Check pod logs:
   ```bash
   kubectl logs <pod-name>
   ```

2. Describe the pod:
   ```bash
   kubectl describe pod <pod-name>
   ```

3. Port-forward to test directly:
   ```bash
   kubectl port-forward service/sentiment-analysis-service 8000:80
   ```

4. Access via `http://localhost:8000` in your browser

## Cleanup

To stop and delete the Minikube cluster:
```bash
minikube stop
minikube delete
```

