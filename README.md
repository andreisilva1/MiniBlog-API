# MiniBlog API

A back-end API built with FastAPI, PostgreSQL and Redis for managing a MiniBlog with Users, Posts and Tags features.


## 🚀 Technologies

Este projeto é construído com as seguintes tecnologias e ferramentas:

* **Python 3.12+**

* **FastAPI**

* **PostgreSQL**

  * `asyncpg`: Asynchronous PostgreSQL's driver.

  * `SQLAlchemy`: ORM (Object-Relational Mapper) for database interaction.

* **Redis**: Caching / task queue

* **Pydantic Settings**:  Environment configuration

* **Uvicorn**: ASGI Server

* **Render.com**: Deployment


 [Click here to test the deployed version of the API](https://miniblog-ckhn.onrender.com)
---


## 📘 API Endpoints

### 🧑‍💼 **Users**

| **Method** | **Endpoint**        | **Description** |
|------------|---------------------|------------------|
| `GET`      | `/users/`           | Retrieve the current logged-in user's information |
| `POST`     | `/users/signup`     | Create a new user account |
| `PATCH`    | `/users/`           | Update the current logged-in user's information |
| `DELETE`   | `/users/`           | Delete the current logged-in user |
| `POST`     | `/users/login`      | Log in a user if the provided credentials are valid |
| `GET`      | `/users/logout`     | Log out the current user session |

---

### 📝 **Publications**

| **Method** | **Endpoint**                  | **Description** |
|------------|-------------------------------|------------------|
| `GET`      | `/publications/latest`        | Retrieve the latest public posts |
| `GET`      | `/publications/me`            | Retrieve all posts created by the current user |
| `GET`      | `/publications/id`            | Retrieve a post by ID (if it exists) |
| `GET`      | `/publications/tag`           | Retrieve all posts with a specific tag |
| `GET`      | `/publications/days`          | Retrieve posts from a specific time period (e.g., last N days) |
| `GET`      | `/publications/like-post`     | Like a post by ID |
| `GET`      | `/publications/liked-posts`   | View all posts liked by the current user |
| `GET`      | `/publications/dislike-post`  | Dislike a post by ID |
| `GET`      | `/publications/disliked-posts`| View all posts disliked by the current user |
| `POST`     | `/publications/`              | Create a new post (requires authentication) |
| `PATCH`    | `/publications/`              | Update a post (if it belongs to the current user) |
| `DELETE`   | `/publications/`              | Delete a post (if it belongs to the current user) |

---

### 🚫 **Block System**

| **Method** | **Endpoint**        | **Description** |
|------------|---------------------|------------------|
| `POST`     | `/block/tags`       | Block a specific tag (hide posts with this tag) |
| `POST`     | `/block/users`      | Block a specific user (hide all posts from them) |

## Installation & Local Setup

Siga os passos abaixo para configurar e executar o MiniBlog API em seu ambiente local:

1. **Clone the repository:**
	```
	bash
	git clone https://github.com/andreisilva1/MiniBlog.git
	cd MiniBlog
	```
	
2. **Create and activate a virtual environment:** 
* **Linux/macOS:** 
	```
	python -m venv venv
	source venv/bin/activate
	```

* **Windows:**
	```
	python -m venv venv
	.venv\scripts\activate
	```
  
 3. **Install dependencies:**
	```
	pip install -r requirements.txt
	```

3. **Configure environment variables:** 
* Copy `.env.example` to .env
 * Fill in your local credentials (ex: PostgreSQL connection and Redis)


4. **Run the application:**
 * With Uvicorn:  ``` uvicorn app.main:app --reload ``` 
 * FastAPI development mode: ``` fastapi dev run ``` 


5. [Click here to access the interactive API Scalar docs]([http://localhost:8000/)
