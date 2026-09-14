# Azure Three-Tier Task Manager

A production-style three-tier web application built with **Flask, Docker, Microsoft Azure, and GitHub Actions**.

The project demonstrates how to deploy a containerized Python application to Azure App Service with **Azure SQL Database**, **Azure Blob Storage**, automated **CI/CD**, and application monitoring using **Application Insights and Azure Monitor**.

---

## 🏗️ Architecture

```text
                         USER
                           │
                           ▼
                    HTTPS / Internet
                           │
                           ▼
                 ┌────────────────────┐
                 │   Azure App        │
                 │   Service          │
                 │                    │
                 │   Docker Container │
                 │   Flask App        │
                 └───────┬───────┬────┘
                         │       │
                         ▼       ▼
                  ┌──────────┐ ┌──────────────┐
                  │ Azure SQL│ │ Blob Storage │
                  │ Database │ │ Task Files   │
                  └──────────┘ └──────────────┘
                         │
                         ▼
                 Application Insights
                         │
                         ▼
                   Azure Monitor
```

### CI/CD Architecture

```text
Developer
    │
    ▼
 GitHub
    │
    ▼
GitHub Actions
    │
    ├── Azure OIDC Login
    │
    ├── Docker Build
    │
    ├── Push Image
    │
    ▼
Azure Container Registry
    │
    ▼
Azure App Service
    │
    ▼
Running Application
```

---

## 🚀 Features

* Create tasks
* Add task descriptions
* Upload task attachments
* Store task information in Azure SQL Database
* Store uploaded files in Azure Blob Storage
* Delete tasks
* Containerized Flask application
* Automated Docker image builds
* Automated deployment using GitHub Actions
* Azure Container Registry integration
* Application monitoring
* Health checks
* HTTP 5xx monitoring alerts
* SQL connection resilience

---

## 🛠️ Technologies Used

### Application

* Python
* Flask
* Flask-SQLAlchemy
* Jinja2
* HTML
* CSS

### Database

* Microsoft Azure SQL Database
* SQLAlchemy
* PyODBC
* Microsoft ODBC Driver 18 for SQL Server

### Storage

* Azure Blob Storage

### Containers

* Docker
* Docker Hub-compatible container workflow
* Azure Container Registry

### Cloud

* Azure App Service
* Azure SQL Database
* Azure Storage Account
* Azure Container Registry
* Azure Application Insights
* Azure Monitor

### DevOps

* Git
* GitHub
* GitHub Actions
* OpenID Connect (OIDC)
* Azure CLI

---

## 📁 Project Structure

```text
azure-three-tier-task-app/
│
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── database.py
│   ├── blob_storage.py
│   │
│   ├── templates/
│   │   ├── index.html
│   │   └── dashboard.html
│   │
│   └── static/
│       └── style.css
│
├── .github/
│   └── workflows/
│       └── deploy.yml
│
├── Dockerfile
├── .dockerignore
├── .gitignore
├── requirements.txt
├── run.py
└── README.md
```

---

## 🗄️ Azure SQL Database

The application uses Azure SQL Database to store task information.

The `Task` model contains:

```text
id
title
description
status
file_name
```

SQLAlchemy is used as the ORM layer.

The application also uses connection-pool resilience:

```python
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_pre_ping": True,
    "pool_recycle": 1800
}
```

`pool_pre_ping` helps detect stale database connections before using them.

---

## 📦 Azure Blob Storage

Uploaded task files are stored in an Azure Blob Storage container.

```text
Storage Account
      │
      ▼
 task-files
      │
      ├── document.pdf
      ├── image.png
      └── other files
```

The application uploads files using the Azure Storage Blob SDK.

---

## 🐳 Docker

The Flask application is packaged into a Docker container.

The container includes:

* Python 3.12
* Flask application
* SQLAlchemy
* PyODBC
* UnixODBC
* Microsoft ODBC Driver 18
* Azure Storage SDK

The application listens on:

```text
5000
```

Build the image locally:

```bash
docker build -t azure-task-manager .
```

Run the container:

```bash
docker run -p 5000:5000 azure-task-manager
```

---

## ☁️ Azure Container Registry

Docker images are stored in Azure Container Registry.

Registry:

```text
taskmanageracr20260914
```

Repository:

```text
azure-task-manager
```

Images are tagged using the Git commit SHA.

Example:

```text
azure-task-manager:<commit-sha>
```

The `latest` tag is also maintained by the CI/CD pipeline.

---

## 🚢 Azure App Service

The Docker container runs on Azure App Service.

Application:

```text
fejaan-task-manager-2026
```

The application is configured to listen on port:

```text
5000
```

Application URL:

```text
https://fejaan-task-manager-2026.azurewebsites.net
```

---

## 🔄 CI/CD Pipeline

Every push to the `main` branch triggers GitHub Actions.

Pipeline:

```text
Git Push
   │
   ▼
GitHub Actions
   │
   ▼
Azure OIDC Authentication
   │
   ▼
Docker Build
   │
   ▼
Push Image to ACR
   │
   ▼
Update Azure App Service
   │
   ▼
Restart App Service
   │
   ▼
Application Deployed
```

Workflow file:

```text
.github/workflows/deploy.yml
```

### Pipeline stages

1. Checkout source code
2. Authenticate with Azure
3. Login to Azure Container Registry
4. Build Docker image
5. Push Docker image
6. Deploy image to Azure App Service
7. Restart App Service

---

## 🔐 Security

The project uses GitHub Actions **OpenID Connect (OIDC)** instead of storing an Azure client secret for GitHub authentication.

Sensitive configuration is stored outside the source code.

Example environment variables:

```text
DB_SERVER
DB_NAME
DB_USER
DB_PASSWORD
AZURE_STORAGE_CONNECTION_STRING
```

The `.env` file is excluded from Git:

```text
.env
```

Private keys, passwords, connection strings, and other credentials must never be committed to the repository.

---

## 📊 Monitoring

Application monitoring is implemented using:

* Azure Application Insights
* Azure Monitor
* App Service Health Check

Application Insights tracks application telemetry such as HTTP requests and failures.

The App Service health check uses:

```text
/
```

The project also includes an Azure Monitor alert for HTTP 5xx responses.

---

## ❤️ Health Check

The application exposes:

```text
GET /
```

The endpoint is used by Azure App Service Health Check to verify that the application is responding.

A successful response should return:

```text
HTTP 200 OK
```

---

## 🧪 Testing

Test the application locally:

```bash
source venv/bin/activate
python run.py
```

Open:

```text
http://localhost:5000
```

Test the production application:

```bash
curl -I https://fejaan-task-manager-2026.azurewebsites.net/
```

Expected response:

```text
HTTP/1.1 200 OK
```

---

## 🔧 Useful Azure Commands

Check App Service status:

```bash
az webapp show \
  --resource-group rg-azure-task-manager \
  --name fejaan-task-manager-2026 \
  --query state
```

Check deployed container:

```bash
az webapp config container show \
  --resource-group rg-azure-task-manager \
  --name fejaan-task-manager-2026
```

View

Screenshots

<img width="1917" height="1036" alt="Screenshot 2026-09-14 140633" src="https://github.com/user-attachments/assets/8d0e4c40-c472-412d-b88f-e1ed012a70dd" />
<img width="1917" height="676" alt="Screenshot 2026-09-14 140701" src="https://github.com/user-attachments/assets/409e1231-cd08-4889-849c-e57326fecedc" />
<img width="1917" height="1027" alt="Screenshot 2026-09-14 140714" src="https://github.com/user-attachments/assets/fcbd37fc-9a80-491b-8f90-39c4f0dd8b75" />
<img width="1917" height="985" alt="Screenshot 2026-09-14 140727" src="https://github.com/user-attachments/assets/c928d28b-3608-44ac-b1ae-c26253f86b9d" />
<img width="1917" height="1012" alt="Screenshot 2026-09-14 140744" src="https://github.com/user-attachments/assets/784e70d9-2ced-4eba-979e-397667a7c263" />
<img width="1917" height="1022" alt="Screenshot 2026-09-14 140815" src="https://github.com/user-attachments/assets/b35af0d7-2ae8-4101-b408-1c147976eff9" />
<img width="1917" height="1021" alt="Screenshot 2026-09-14 140840" src="https://github.com/user-attachments/assets/9466fa19-8c71-4bd3-bdf4-f9eed2c8cb78" />
<img width="1916" height="983" alt="Screenshot 2026-09-14 140803" src="https://github.com/user-attachments/assets/3a07cadb-1a89-489b-8e28-a188d9c10dc1" />



