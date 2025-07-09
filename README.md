[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![python](https://img.shields.io/badge/Python-3.12-3776AB.svg?style=flat&logo=python&logoColor=yellow)](https://www.python.org)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
![CSS](https://img.shields.io/badge/CSS-563d7c?&style=flat&logo=css3&logoColor=white)
![HTML](https://img.shields.io/badge/HTML-e34c26?style=flat&logo=html5&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)


# Formula 1 Race Report Web App
A Flask-based web application for displaying and exploring Formula 1 qualifying session results.  
This project builds on the `formula1_race_analysis` package to provide interactive views with caching and sorting functionality.

****This project is at the early stages of development. 

## Requirements
- Python 3.10+
- flask
- flask-caching
- pydantic-settings
- formula1_race_analysis (installed as a dependency)

## Running the Formula 1 Race Report Web App
To start the Flask-based Formula 1 Race Report Web App, use the provided CLI script after installing the project.

### Step 1: Install the project
If you haven't installed the project yet, run:

```bash
uv pip install -e .
```

### Step 2: Run the server
Start the server with the following command:

```bash
formula1-app
```

## URL Routes
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
| --- | --- | --- |
| order | Sort order: ASC or DESC | DESC |

Example:
```console
/report/?order=ASC
```

### /report/drivers/<driver_id>
Displays data only for the specified driver.

| Path parameter | Description                                                                                                          | Default |
|----------------|----------------------------------------------------------------------------------------------------------------------|---------|
| driver_id      | A 3-letter string combining initials from: first name, last name and car model (e.g. "KRF" → Kimi Räikkönen Ferrari) | -       |

```console
/report/drivers/KRF
```
## Caching
Each route is cached using flask-caching:
- Simple in-memory cache (SimpleCache)
- Timeout: 10 seconds.

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
2. Activate virtual environment
```console
python -m venv .venv
.venv/Scripts/activate
```
3. Lint and formate code:
```console
uvx ruff check
uvx ruff format
```
4. Automatically format code, check linting, and ensure clean commits.
```console
uvx pre-commit run 
```
5. Run tests
```console
uvx pytest tests\
```

tags: `python` `python3` `problem-solving` `programming` `learn-python` `formula1-race-report-web-app` `uv` `flask` `flask-cashing` `testpypi`
