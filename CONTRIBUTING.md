# How to Contribute

We're excited you're interested in contributing to this project! All contributions are welcome.

To ensure a smooth and collaborative process, please follow these guidelines.

## Getting Started

1.  **Fork the Repository:** Start by forking this repository to your own GitHub account.
2.  **Clone Your Fork:** Clone your fork to your local machine:
    ```bash
    git clone https://github.com/YOUR-USERNAME/YOUR-REPO.git
    cd YOUR-REPO
    ```

## Development Environment Setup

This project uses Docker and Docker Compose to manage the Airflow development environment. The `README.md` provides detailed setup instructions.

### 1. Set Up Pre-commit Hooks (Recommended)
This project uses `pre-commit` to ensure code quality and consistency. Setting up the hooks will automatically run checks (like `black` and `flake8`) before you commit.

First, install the tool on your host machine:
```bash
pip install pre-commit
```
Then, set up the git hooks in your local repository clone:
```bash
pre-commit install
```

### 2. Configure the Environment
1.  **Authenticate with GCP:** Run `gcloud auth application-default login`.
2.  **Configure `.env`:** Copy the `.env.example` file to `.env` and fill in the required values, such as `GCP_PROJECT_ID` and `LOCAL_GCLOUD_CONFIG_DIR_PATH`.

### 3. Start the Services
Use the `Makefile` to build the images and start all containers:
    ```bash
    make up
    ```

## Making Changes

1.  **Create a Branch:** Always create a new branch for your changes from the `main` branch. Use a descriptive name.
    ```bash
    # Examples:
    # git checkout -b feat/add-new-dag
    # git checkout -b fix/correct-bigquery-operator
    git checkout -b <type>/<short-description>
    ```
2.  **Write Your Code:** Make your changes to the codebase.
3.  **Run Checks and Tests:** Before committing, ensure your code passes all quality checks and tests. These commands run inside the Docker environment for consistency.
    ```bash
    # Run linting and formatting checks
    make lint

    # Run the unit test suite
    make test
    ```
4.  **Commit Your Changes:** Use clear and descriptive commit messages that follow the Conventional Commits standard.
    ```bash
    git commit -m "feat: Add new feature X"
    ```

## Submitting a Pull Request (PR)

1.  **Push Your Branch:** Push your branch to your fork on GitHub.
    ```bash
    git push origin feat/add-new-dag
    ```
2.  **Open the Pull Request:** On your fork's GitHub page, click "Contribute" and "Open pull request". Clearly describe what your change does and why it's needed.
3.  **Code Review:** A maintainer will review your code. Be prepared to respond to feedback or requests for changes. Once your PR is approved and all automated checks pass, it will be merged.

Thank you for your contribution!
