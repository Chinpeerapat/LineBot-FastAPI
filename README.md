<p align="center"> <a href="https://github.com/yuting1214/LineBot-FastAPI"> <img src="frontend/assets/line.png" height="50"> </a> <h1 align="center"> <a href="https://github.com/yuting1214/LineBot-FastAPI">LineBot-FastAPI</a> </h1> </p> <p align="center"> <a href="https://railway.app/template/yNppuu?referralCode=jk_FgY"> <img src="https://railway.app/button.svg" alt="Deploy on Railway" height="30"> </a> </p>

LineBot-FastAPI is a comprehensive and modular template for developing LINE bots using FastAPI. It integrates seamlessly with various APIs and provides a robust structure for handling complex interactions and processing.


## Key Features and Integrations 🎉
Key features:

* 🤖 LINE Bot Integration: Easily create and manage LINE bots with built-in event handling and messaging capabilities.
* ⚡ FastAPI API Documentation and Authentication: Leverage FastAPI's powerful documentation tools and secure authentication mechanisms.
* 🧠 LLM Integration (OpenAI): Implement advanced chatbot logic using Large Language Models, with support for text and image modalities.

## Why This Template ? 🚀
* 📝 API-Driven Logging: This template uses API calls to log data, ensuring better modularity and flexibility.
* ⚙️ Async Non-Blocking Operations: Designed to handle multiple user inputs simultaneously, making the bot responsive and efficient even under heavy load.
* 🌐 LLM Omniversal Integration: Supports various input modalities (text and image) for a more versatile and interactive chatbot experience.

## Project Structure 📁

<details>
<summary>More Project Details</summary>

```
LineBot-FastAPI-Template/
├── backend/                      # Backend directory for the FastAPI application
│   ├── fastapi/                  # Main application directory
│   │   ├── __init__.py           # Initialization file for the fastapi package
│   │   ├── api/                  # Directory for API related code
│   │   │   ├── __init__.py       # Initialization file for the API package
│   │   │   ├── v1/               # Version 1 of the API
│   │   │   │   ├── __init__.py   # Initialization file for the v1 API package
│   │   │   │   ├── endpoints/    # Directory for API endpoint definitions
│   │   │   │   │   ├── __init__.py          # Initialization file for endpoints package
│   │   │   │   │   ├── base.py              # Endpoints for base url
│   │   │   │   │   ├── doc.py               # Endpoints for the API document
│   │   │   │   │   ├── message.py           # Endpoints for message management
│   │   │   │   │   ├── user.py              # Endpoints for user management
│   │   │   │   │   ├── line.py              # Endpoints for Line Webhook
│   │   ├── dependencies/         # Directory for dependency management
│   │   │   ├── __init__.py       # Initialization file for dependencies package
│   │   │   ├── database.py       # Database connection and session management
│   │   │   ├── rate_limiter.py   # Rate limiting logic
│   │   ├── request_handler/      # Directory for HTTP request handling utilities
│   │   │   ├── __init__.py
│   │   │   ├── api_requests.py   # Functions for API endpoint calling.
│   │   ├── core/                 # Core application logic
│   │   │   ├── __init__.py       # Initialization file for core package
│   │   │   ├── config.py         # Configuration settings
│   │   │   ├── init_setting.py   # Init settings with user's input
│   │   ├── models/               # Directory for SQLAlchemy models
│   │   │   ├── __init__.py       # Initialization file for models package
│   │   │   ├── user.py           # User model
│   │   │   ├── message.py        # Message model
│   │   ├── schemas/              # Directory for Pydantic schemas
│   │   │   ├── __init__.py       # Initialization file for schemas package
│   │   │   ├── user.py           # Schemas for user data
│   │   │   ├── message.py        # Schemas for message data
│   │   ├── crud/                 # Directory for CRUD operations
│   │   │   ├── __init__.py       # Initialization file for crud package
│   │   │   ├── user.py           # CRUD for user management
│   │   │   ├── session.py        # CRUD for session management
│   │   │   ├── message.py        # CRUD for message management
│   │   ├── main.py               # Main FastAPI application file
│   ├── line/                     # Line integration
│   │   ├── __init__.py           # Initialization file for Line package
│   │   ├── handlers/             # Directory for event handlers in Line Bot
│   │   │   ├── __init__.py       # Initialization file for the API package
│   │   │   ├── message_event.py  # Function for message event.
│   │   │   ├── image_event.py    # Function for image event.
│   │   ├── operations/           # Directory for Low-level operation in Line Bot
│   │   │   ├── __init__.py       # Initialization file for 
│   │   │   ├── user.py           # User model relevant operations in Line Bot
│   │   │   ├── message.py        # Message model relevant operations in Line Bot
│   │   │   ├── llm.py            # LLM relevant operations in Line Bot
│   ├── data/                     # Directory for data when initiating DB
│   │   ├── __init__.py           # Initialization file for data package
│   ├── security/                 # Directory for authentication and authorization
│   │   ├── __init__.py           # Initialization file for security package
│   │   ├── authentication.py     # Authentication logic
│   │   ├── authorization.py      # Authorization logic
│   ├── tests/                    # Directory for test files
│   │   ├── __init__.py           # Initialization file for tests package
│   │   ├── test_user.py          # Test cases for user management
│   │   ├── test_message.py       # Test cases for message management
│   ├── constant.py               # Constant settings for backend
├── frontend/
│   ├── __init__.py               # Initialization file for frontend package
│   ├── assets/                   # Static assets (e.g., CSS, JS) for the web app
│   │   └── favicon.ico           # Favicon for the web app
│   ├── login/                    # Main login UI directory
│   │   ├── __init__.py           # Initialization file for the login folder
│   │   ├── static/               # Directory for static files
│   │   │   ├── style.css         # CSS for login UI 
│   │   │   └── favicon.ico       # Favicon for the login UI         
│   │   └── templates/            # Directory for HTML templates
│   │       ├── base.html         # HTML base template
│   │       └── login.html        # HTML login template 
├── llm/
│   ├── __init__.py               # Initialization file for LLM package
│   ├── chain/                    # Folder for prompt handling
│   │   ├── __init__.py           # Initialization file for chain package
│   │   ├── llm_text_chain.py     # Function for LLM text generation.
│   │   ├── llm_image_chain.py    # Function for LLM image understanding.
│   ├── prompt/                   # Folder for prompt handling
│   │   ├── __init__.py           # Initialization file for prompt package
│   │   ├── base_text_templates.py# Stores base prompt templates for text generation
│   │   ├── examples/             # Directory for few-shot examples used by the chain
│   │   ├── deprecated/           # Directory for deprecated prompts
│   ├── memory/                   # Folder for Memory Management
│   │   ├── __init__.py           # Initialization file for memory package
│   │   ├── memory_management.py  # Module for LLM memory management
├── .env                          # Environment variables file
├── Dockerfile                    # Dockerfile for containerizing the application
├── README.md                     # Readme file with project description and setup instructions
├── requirements.txt              # Python dependencies file
├── LICENSE                       # License file
```
</details>

## Contributing 🤝
We welcome contributions from the community! Whether it's bug fixes, feature enhancements, or documentation improvements, feel free to open a pull request.

---

Designed with :heart: by [Mark Chen](https://github.com/yuting1214)
