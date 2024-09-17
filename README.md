# INFYNITE POLLING API

This is a FastAPI-based polling application that allows users to create, update, and retrieve poll questions and answers. It also provides the ability to track poll statistics and supports CORS for cross-origin requests.

## Features

- **Ping Server**: Check if the server is running.
- **Retrieve All Questions**: Get a list of all questions in the poll database.
- **Retrieve Question by ID**: Fetch a particular question by its ID.
- **Submit an Answer**: Increment the vote count for a selected answer.
- **Retrieve Poll Statistics**: Get statistics for a particular poll.
- **Add a New Question**: Insert a new question and its options into the poll.

## Prerequisites

- **FastAPI**: Framework used to build the API.
- **SQLAlchemy**: ORM for interacting with the MySQL database.
- **MySQL**: Backend database for storing poll questions and answers.
- **Mangum**: For AWS Lambda support.
- **CORS Middleware**: Handle Cross-Origin Resource Sharing.

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/juhiikataria/inFYInite-Polling-App.git
   cd inFYInite-Polling-App
   ```

2. Install required dependencies:

   ```bash
   pip install fastapi sqlalchemy pymysql mangum uvicorn
   ```

3. Set up your MySQL database and replace the placeholders in the connection string:

   ```python
   engine = create_engine(
       "mysql+pymysql://{username}:{password}@{rds_url_endpoint}/{database_name}"
   )
   ```

4. Run the FastAPI app locally using Uvicorn:

   ```bash
   uvicorn main:app --reload
   ```

5. The API will be available at `http://127.0.0.1:8000`.

### API Endpoints

| Method | Endpoint                                | Description                                          |
| ------ | --------------------------------------- | ---------------------------------------------------- |
| GET    | `/ping`                                 | Check the uptime of the server.                      |
| GET    | `/all_question`                         | Get all poll questions in the database.              |
| GET    | `/question/{question_id}`               | Fetch a specific question by its ID.                 |
| GET    | `/answer/{question_id}/{answer_id}`     | Increment the vote count for option 1 or 2.          |
| GET    | `/{question_id}/stats`                  | Retrieve statistics (votes) for a specific question. |
| GET    | `/addQuestion/{question}/{opt1}/{opt2}` | Add a new poll question with two options.            |

### Example Usage

1. **Ping the Server**

   ```bash
   curl -X 'GET' 'http://127.0.0.1:8000/ping'
   ```

2. **Retrieve All Questions**

   ```bash
   curl -X 'GET' 'http://127.0.0.1:8000/all_question'
   ```

3. **Add a New Poll Question**

   ```bash
   curl -X 'GET' 'http://127.0.0.1:8000/addQuestion/{question}/{opt1}/{opt2}'
   ```

4. **Submit an Answer**

   ```bash
   curl -X 'GET' 'http://127.0.0.1:8000/answer/{question_id}/{answer_id}'
   ```

5. **Retrieve Poll Statistics**
   ```bash
   curl -X 'GET' 'http://127.0.0.1:8000/{question_id}/stats'
   ```

### Database Schema

Ensure that your MySQL database contains the `poll_questions` table with the following columns:

```sql
CREATE TABLE poll_questions (
    question_id INT PRIMARY KEY AUTO_INCREMENT,
    question VARCHAR(255) NOT NULL,
    option1 VARCHAR(100),
    option2 VARCHAR(100),
    poll_1 INT DEFAULT 0,
    poll_2 INT DEFAULT 0,
    asked VARCHAR(10) DEFAULT 'no'
);
```

### CORS Configuration

This API allows cross-origin requests from any domain using the following CORS middleware configuration:

```python
app.add_middleware(CORSMiddleware, allow_origins=["*"])
```

### Deployment

If deploying to AWS Lambda, use `Mangum` to create a handler for the Lambda function:

```python
handler = Mangum(app)
```

### License

This project is licensed under the MIT License.

---
