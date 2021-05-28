# QRisq Docker Image

## Build docker image
```sh
docker build -f Dockerfile.production -t qrisq_api .
```

## Run Docker image locally on port 8000
```sh
docker run -it --name qrisq_api -p 8000:8000 --rm qrisq_api
```