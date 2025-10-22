# FastAPI Docker Google Cloud Project

This project demonstrates how to deploy a FastAPI application using Docker and Google Cloud. The application interfaces with Meshtastic devices over a serial connection.

## Project Structure

```
fastapi-docker-gcloud
├── src
│   ├── main.py          # FastAPI application code
│   └── requirements.txt  # Python dependencies
├── Dockerfile            # Docker image build instructions
├── .dockerignore         # Files to ignore during Docker build
├── cloudbuild.yaml       # Google Cloud Build configuration
└── README.md             # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd fastapi-docker-gcloud
   ```

2. **Install dependencies:**
   Navigate to the `src` directory and install the required Python packages:
   ```bash
   cd src
   pip install -r requirements.txt
   ```

## Running the Application Locally

To run the FastAPI application locally, use the following command:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```
You can then access the API at `http://localhost:8000`.

## Building the Docker Image

To build the Docker image, run the following command from the root of the project:
```bash
docker build -t fastapi-docker-gcloud .
```

## Deploying to Google Cloud

1. **Set up Google Cloud SDK:**
   Make sure you have the Google Cloud SDK installed and configured.

2. **Deploy using Cloud Build:**
   Run the following command to trigger the build and deployment:
   ```bash
   gcloud builds submit --config cloudbuild.yaml .
   ```

## Usage

Once deployed, you can interact with the FastAPI application using the endpoints defined in `main.py`. 

## License

This project is licensed under the MIT License.