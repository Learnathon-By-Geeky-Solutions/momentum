# Running the FastAPI Project

Follow these instructions to run the FastAPI project:

## Prerequisites

- Python 3.7+
- `pip` package manager
- PostgreSQL

## Setup

1. **Clone the repository:**
    ```bash
    git clone git@github.com:Learnathon-By-Geeky-Solutions/momentum.git
    cd momentum
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source .venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database:**
    - Create a PostgreSQL database.
    - Update the database URL in your environment variables or configuration file.

5. **Run database migrations:**
    ```bash
    alembic upgrade head
    ```

## Running the Server

1. **Start the FastAPI server:**
    ```bash
    uvicorn main:app --reload
    ```

2. **Access the API documentation:**
    Open your browser and navigate to `http://127.0.0.1:8000/docs` for the interactive API documentation.

## Testing

1. **Run the tests:**
    ```bash
    pytest
    ```

## Additional Commands

- **To deactivate the virtual environment:**
  ```bash
  deactivate
  ```

- **To install new dependencies:**
  ```bash
  pip install <package-name>
  pip freeze > requirements.txt
  ```
