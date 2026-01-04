[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![python](https://img.shields.io/badge/Python-3.12-3776AB.svg?style=flat&logo=python&logoColor=yellow)](https://www.python.org)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
![CSS](https://img.shields.io/badge/CSS-563d7c?&style=flat&logo=css3&logoColor=white)
![HTML](https://img.shields.io/badge/HTML-e34c26?style=flat&logo=html5&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)


# Formula 1 Race Report Web App
A Flask-based web application for displaying and exploring Formula 1 qualifying session results.  
Supports both Flask and FastAPI backends.

This project builds on the `formula1_race_analysis` package to provide interactive views, caching, sorting functionality, and a JSON API.

****This project is at the early stages of development. 

## Requirements
- Python 3.12+
- Flask & Flask-caching
- FastAPI & Uvicorn
- Pydantic-settings
- formula1_race_analysis (installed as a dependency)

## Running the Flask Web App

### Step 1: Install the project

```bash
uv pip install -e .
```

### Step 2: Run the server
Start the server with the following command:

```bash
formula1-app
```

### Flask Routes
This web application exposes several routes to display and interact with Formula 1 qualifying session data. Below is a complete overview of the available routes and their behavior:

| Route | Description                                                                                               |
| --- |-----------------------------------------------------------------------------------------------------------|
| / | 	Redirects to /report/. Acts as the default entry point.                                                  |
| /report/ | Displays the full qualifying session report. Supports sorting via the order query parameter.              |
| /report/drivers | Lists all drivers who participated in the session.                                                        |
| /report/drivers/<driver_id> | Displays results for a specific driver using a 3-letter ID (e.g., `KRF`). Returns **400 Bad Request** if the ID format is invalid or **404 Not Found** if no data is found for the given ID. |

### /report/
Displays the full race report sorted by lap times.

Query Parameters:

| Parameter | Description | Default |
| --- | --- |---------|
| order | Sort order: ASC or DESC | ASC     |

Example:
```console
/report/?order=ASC
```

### /report/drivers/<driver_id>
Displays data for the specified driver.

| Path parameter | Description                                                                                                          | Default |
|----------------|----------------------------------------------------------------------------------------------------------------------|---------|
| driver_id      | A 3-letter string combining initials from: first name, last name and car model (e.g. "KRF" → Kimi Räikkönen Ferrari) | -       |

```console
/report/drivers/KRF
```
### Caching
Each route is cached using flask-caching:
- Simple in-memory cache (SimpleCache)
- Timeout: 10 seconds.

## Running the FastAPI API
The FastAPI backend exposes the same data via a REST API.

### Step 1: Run the FastAPI server
```console
formula1-api
```

### FastAPI Routes
Route	Method	Description

| Route | Method | Description                                                                                                  |
| --- |---|--------------------------------------------------------------------------------------------------------------|
| / | GET | Redirects to /report/ (default JSON response)                                                                |
| /report/ | GET | Returns full race report in JSON format. Supports query params: order (ASC or DESC), fmt (json or xml formats) |
| /report/drivers | GET | Returns a list of all drivers participating in the race                                                      |
| /report/drivers/{driver_id} | GET | Returns results for a specific driver ID (3-letter code). Returns 400 for invalid ID, 404 if not found       |

Example requests:
```console
GET /report/?order=ASC
GET /report/drivers/
GET /report/drivers/KRF
```
### FastAPI Exception Handling

- 400 Bad Request: Invalid driver ID
- 404 Not Found: Driver not found in session data

Response includes timestamp and request info for better debugging.

## Setup Pre-commit Hooks:
Run this command after cloning the project to enable pre-commit:
```console
pre-commit install
```

## For Contributors
This project is managed with uv. All python dependencies have to be specified inside pyproject.toml file. 
1. Install uv globally:
```console
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
2. Clone the Repository
```console
https://github.com/KrisKulbych/formula1-race-results-web-app.git
cd formula1-race-results-web-app
```
4. Create a Virtual Environment
```console
uv venv
.venv/Scripts/activate
```
3. Install Dependencies
```console
uv sync --all-groups
uv pip install -e .
```
4. Run the Application
```console
formula1-app
formula1-api
```
5. Lint and format code:
```console
ruff check
ruff format
mypy .
```
6. Automatically format code, check linting, and ensure clean commits.
```console
pre-commit run 
```
7. Run tests
```console
pytest tests
```

tags: `python` `python3` `problem-solving` `programming` `learn-python` `formula1-race-report-web-app` `uv` `flask` `flask-cashing` `testpypi` `fastapi` `fastapa-cache2`
