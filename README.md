# Scam Crawler

> This is a project to facilitate the extraction of internship job posting from various websites and upload them to the [ScamWeb](https://github.com/InGenius-Project/ScamWeb) server.

## Installation

To install the dependencies.

- poetry

  ```bash
  # create virtual environment (optional)
  poetry env use python

  poetry shell
  poetry install
  ```

- pip

  ```bash
  pip install -r requirements.txt
  ```

## Usage

- Windows

  ```powershell
  python main.py
  ```

- Linux

  ```bash
  python3 main.py
  ```

## Dot Env

- The following variables should be set in `.env` file

  | **Variable**   | **Explanation**                                                                         |
  | :------------- | :-------------------------------------------------------------------------------------- |
  | GOOGLE_API_KEY | API key for google account                                                              |
  | GOOGLE_CSE_KEY | API key for google custom search engine (CSE)                                           |
  | SERVER_IP      | This is the ip address of [ScamWeb](https://github.com/InGenius-Project/ScamWeb) server |
  | PORT           | This is the port of [ScamWeb](https://github.com/InGenius-Project/ScamWeb) server       |

- Create `.env` by `.env.example` and set the variables.

  ```bash
  cp .env.example .env
  ```
