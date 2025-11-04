# Breast Cancer Classification with Docker

Train a Random Forest classifier for breast cancer detection using Docker.

## Dataset

- 569 breast tumor samples with 30 features
- 2 classes: Malignant and Benign
- Accuracy: ~96%

## Quick Start

### Build and Run

```sh
docker build -t cancer-classifier:v1 .
docker run cancer-classifier:v1
```

**Expected output:**

```
Breast cancer classification model trained successfully
Accuracy: 96.49%
```

## Files

```
├── Dockerfile          # Container configuration
├── requirements.txt    # Python dependencies
├── main.py            # Training script
└── README.md
```

## Useful Commands

```sh
# View images
docker images

# View containers
docker ps -a

# Remove image
docker rmi cancer-classifier:v1

# Clean up
docker system prune -a
```

## Troubleshooting

**Docker not found?** Install from [docker.com](https://www.docker.com/products/docker-desktop/)

**Permission denied?** Start Docker Desktop and ensure it's running

**Save model locally?**

```sh
docker run -v $(pwd)/output:/app cancer-classifier:v1
```
