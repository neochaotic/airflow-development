<p align="center">
  <img src="https://airflow.apache.org/images/feature-image.png" width="400" alt="Airflow Logo">
</p>
<p align="center">
  <img src="https://img.shields.io/badge/Airflow-2.11.0-blue.svg" alt="Airflow 2.11.0">
  <img src="https://img.shields.io/badge/Python-3.11-blue.svg" alt="Python 3.11">
  <img src="https://img.shields.io/badge/Google%20Provider-10.15.0-blue.svg" alt="Google Provider 10.15.0">
</p>

# 🚀 Local Airflow with GCP: A Docker-based Development Environment

> [!WARNING]
> **This is a local development environment and is NOT suitable for production use.**
> It is designed for ease of use, local testing, and rapid development. For production deployments, please consult the official Airflow documentation for best practices on security, scalability, and high availability.

This project provides a straightforward way to run a local Apache Airflow development environment using Docker Compose. It's pre-configured to seamlessly integrate with your local Google Cloud Platform (GCP) credentials, automatically setting up the default BigQuery connection on initialization.

This setup allows you to develop and test your Airflow DAGs that interact with GCP services (like BigQuery, GCS, etc.) entirely on your local machine, using your own GCP account for authentication.

## 🛠️ Key Dependencies

This project is built and tested with specific versions to ensure stability.

| Dependency                  | Version | Defined In        |
| :-------------------------- | :------ | :---------------- |
| **Apache Airflow**          | `2.11.0`  | `Dockerfile`      |
| **Python**                  | `3.11`    | `Dockerfile`      |
| **Airflow Google Provider** | `10.15.0` | `requirements.txt`|

## 📋 Prerequisites

- Docker and Docker Compose
- Google Cloud SDK (`gcloud` CLI)
- `make` (optional, but recommended for easy commands)

## 🏗️ Project Structure

```
.
├── dags/                     # Your Airflow DAGs go here
├── logs/                     # Airflow logs (auto-generated)
├── plugins/                  # Your custom Airflow plugins
├── tests/                    # Your pytest tests go here
├── .env                      # Local environment configuration (you must create this)
├── pytest.ini                # Pytest configuration (e.g., to filter warnings)
├── docker-compose.yaml       # Docker Compose definition for Airflow services
├── Dockerfile                # Custom Airflow image definition
├── Makefile                  # Helper commands (e.g., make up, make down)
└── requirements.txt          # Python dependencies for the custom image
```

## ⚙️ Setup Steps (Order is Important)

### 1. Authenticate with Google Cloud

Run the following command in your terminal to authenticate using your user credentials. This step creates/updates the Application Default Credentials (ADC) file on your local system, which will be used by Airflow inside Docker.

```bash
# This will open a browser window for you to log in to your Google account.
gcloud auth application-default login
```

### 2. Create and Configure `.env` File

In the project root directory (same location as `docker-compose.yaml`), create a file named `.env`. This file will store environment-specific configurations.

**Copy the content below into your `.env` file and adjust the values:**

```properties
# .env - Essential Settings

# Your default GCP project ID. This will be used for the auto-created 'bigquery_default' connection.
GCP_PROJECT_ID=your-gcp-project-id-here

# Path to the gcloud configuration directory on your host system.
# This directory contains the Application Default Credentials generated in Step 1.
# macOS Example: /Users/your_user/.config/gcloud
# Linux Example: /home/your_user/.config/gcloud
# Windows Example: C:/Users/YourUser/AppData/Roaming/gcloud
LOCAL_GCLOUD_CONFIG_DIR_PATH=/path/to/your/.config/gcloud

# Airflow user UID (important for Linux file permissions).
# On Linux, use the output of 'id -u'. For macOS/Windows, 50000 usually works.
AIRFLOW_UID=50000

AIRFLOW_GID=0
AIRFLOW_PROJ_DIR=.

# Optional: Airflow Admin User Credentials (defaults to airflow/airflow if not set)
_AIRFLOW_WWW_USER_USERNAME=airflow
_AIRFLOW_WWW_USER_PASSWORD=airflow
```

**Note:** The `LOCAL_GCLOUD_CONFIG_DIR_PATH` is crucial. It tells Docker Compose where to find your GCP ADC file on your host machine to mount it into the Airflow containers. The `GCP_PROJECT_ID` will be used by the `airflow-init` service to configure the `bigquery_default` connection.

### 3. Start the Airflow Environment

Now that your GCP authentication is set up and your `.env` file is configured, you can start the Airflow environment using `make`:

```bash
make up
```

On the first run (or after `make down`), the `airflow-init` service will:
- Initialize the Airflow database.
- Create the default Airflow admin user (credentials from `.env` or defaults).
- **Automatically create/update the `bigquery_default` Airflow connection**, configuring it to use your `GCP_PROJECT_ID` and the mounted Application Default Credentials.

If you are not using `make`, you can use `docker-compose` directly:
```bash
docker-compose up -d
```

---

## 🕹️ Usage & Common Commands

### Accessing the Airflow Web UI
- **URL:** `http://localhost:8081` (or whichever host port you configure in `docker-compose.yaml`)
- **Login:** Use the credentials from your `.env` file (`_AIRFLOW_WWW_USER_USERNAME` and `_AIRFLOW_WWW_USER_PASSWORD`). The default is `airflow` / `airflow`.

### Makefile Commands
This project includes a `Makefile` to simplify common tasks.

| Command | Description |
| :--- | :--- |
| `make up` | Build the image (if needed) and start all services. |
| `make down` | Stop and remove all containers, networks, and volumes. |
| `make restart` | A quick way to run `make down && make up`. |
| `make logs` | View and follow the logs from all running services. |
| `make cli` | Access a bash shell inside the `airflow-cli` container. |
| `make build` | Force a rebuild of the custom Airflow Docker image. |
| `make lint` | Run code linting and formatting checks. |
| `make test` | Runs unit tests on the live environment (faster, for quick checks). |
| `make test-local` | An alias for `make test`. |
| `make test-ci` | Runs the full, CI-like unit test suite (slower, most reliable). |
| `make test-integration` | Runs integration tests against GCP using your local credentials. |
| `make clean` | **Stop all project services and remove their containers, volumes, and dangling images.** |

---

## 📦 Adding Python Dependencies

This project uses a custom `Dockerfile` to build the Airflow image, which is the recommended way to manage Python dependencies.

1.  Add your required Python packages to the `requirements.txt` file (e.g., `pandas==1.5.3`).
2.  Rebuild the main Docker image with the new dependencies:
    ```bash
    make build
    ```
3.  Restart your environment for the changes to take effect:
    ```bash
    make restart
    ```
---

## 🧑‍💻 Contributing & Quality Assurance

To ensure code quality and consistency, this project uses `pre-commit` for automated checks and `pytest` for testing. Contributions are welcome!

### Development Setup

1.  **Set up Pre-commit Hooks (Recommended):**
    This will automatically run checks on your code before you commit, ensuring it adheres to the project's style guide. First, install the tool on your host machine:
    ```bash
    pip install pre-commit
    ```
    Then, set up the git hooks in your local repository clone:
    ```bash
    pre-commit install
    ```

### Running Checks Manually
Even without the pre-commit hooks, you can run all quality checks at any time using the `make` commands. These commands execute inside Docker for a consistent and isolated environment:
-   **Linting & Formatting:** `make lint`
-   **DAG Integrity Tests:** `make test`

### CI Pipeline

A GitHub Actions workflow is configured to run on every pull request. It will execute both the `lint` and `test` steps to ensure that all contributions meet the quality standards before being merged.

---

## GCP Interaction
With the `LOCAL_GCLOUD_CONFIG_DIR_PATH` correctly set in `.env`, your GCP credentials mounted, and the `bigquery_default` connection automatically configured by `airflow-init` (using `GCP_PROJECT_ID` from `.env`), your DAGs can interact with GCP services (like BigQuery) using your local ADC.

---

## Quick Tips / Troubleshooting

- **Permission Issues (Linux):** Ensure `AIRFLOW_UID` in `.env` matches your host user ID (`id -u`).
- **Port is already allocated:** If you get an error that port `8080` is already in use, change the port mapping in `docker-compose.yaml` for the `airflow-webserver` service (e.g., from `"8080:8080"` to `"8081:8080"`) and access the UI on the new port.
- **Errors during `make up` or `docker-compose up`?** Always check the logs of the services, especially `airflow-init`, `airflow-webserver`, and `airflow-scheduler`:
  ```bash
  docker-compose logs airflow-init
  docker-compose logs airflow-webserver
  # etc.
  ```
- **Re-authenticating GCP:** If your GCP credentials expire, re-run `gcloud auth application-default login` and then restart your Airflow services (e.g., `make down && make up`).

```