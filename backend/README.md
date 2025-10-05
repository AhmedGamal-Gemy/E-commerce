# E-commerce website backend

This is a basic backend for E-commerce website with automatic Posting (Facebook and Instagram) 

## Requirements

- Python 3.12 or later

#### How to install python using MiniConda 

1. Download and install MiniConda from [here](https://www.anaconda.com/docs/getting-started/miniconda/install#quickstart-install-instructions)

2. Create a new environment using the following command : 
```bash
$ conda create -n e-commerce
```

3.Activate the new environment using the following command :
```bash
$ conda activate e-commerce
```

### (Optional) Setup your command line interface for better readability

```bash
$ export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$ "
```  
## Installation

### Install required packages

```bash
$ pip install -r requirements.txt
```

### Setup the environment variables

```bash
cp .env.example .env
```

Set your environment variables in the `.env` file. like the api keys

## Run Docker Compose Services

### Secure the secrets inside docker

```bash
$ cd docker
$ cp .env.example .env 
```

- Update `.env` with your credentials


### How to run the docker services

```bash
$ sudo docker compose up -d
```

## Run the server 

```bash
$ uvicorn main:app --reload --port 8001 --host 0.0.0.0
```

- uvicorn is the server and must be installed in the system using the requirements.
- main:app is FastAPI app inside the main.py file. The starting point.
- --reload is argument for detecting changes and auto restart the app instead of manually restarting it.
- --port is which port to serve.
- --host is what IPs that can access the server. 0.0.0.0 is like saying all IPs can enter

