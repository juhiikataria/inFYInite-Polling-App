from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from mangum import Mangum
from sqlalchemy import create_engine, text
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from urllib.parse import unquote


origins = ["*"]
app = FastAPI(title="INFYNITE POLLING DOCS")
handler = Mangum(app)

app.add_middleware(CORSMiddleware, allow_origins=origins)

# headers = {"Access-Control-Allow-Origin": "*"}


# (REQUEST BODY) MODEL CONFIGURATION
class poll_body(BaseModel):
    question: str
    option_1: str
    option_2: str


engine = create_engine(
    "mysql+pymysql://{username}:{password}@{rds_url_endpoint}/{database_name}")
connection = engine.connect()


@app.get('/ping', description="Check the uptime of the server")
async def ping():
    return JSONResponse(content={"message": "pong"}, status_code=200)


@app.get("/all_question", description="get the list of all the questions in the database")
async def question():
    q = []
    command = "SELECT * FROM poll_questions"
    questions = connection.execute(text(command))
    for row in questions:
        q.append(list(row))
    return JSONResponse(content={"message": q}, status_code=200)


@app.get('/question/{question_id}', description="get the question with a partiular question id")
def get_question(question_id: int):
    command = f"SELECT question, option1, option2 FROM poll_questions WHERE question_id = {question_id}"
    questions = connection.execute(text(command))
    temp = []
    for row in questions:
        temp.append(list(row))
    if len(temp) != 0:
        return JSONResponse(content={"message": temp}, status_code=200)
    else:
        return JSONResponse(content={"message": "No questions in the database"}, status_code=404)


@app.get("/answer/{question_id}/{answer_id}",
         description="update a particular question with it answer value and increment it by 1")
async def answer(answer_id: str, question_id: int):
    try:
        if answer_id == '1':
            command = f"UPDATE poll_questions SET poll_1 = poll_1 + 1, asked='yes' WHERE question_id = {question_id};"
            update_stats = connection.execute(text(command))
            connection.commit()
            return JSONResponse(content={"message": "poll_1 incremented"}, status_code=200)

        elif answer_id == '2':
            command = f"UPDATE poll_questions SET poll_2 = poll_2 + 1 , asked='yes' WHERE question_id = {question_id};"
            update_stats = connection.execute(text(command))
            connection.commit()
            return JSONResponse(content={"message": "poll_2 incremented"}, status_code=200)

        else:
            return JSONResponse(content={"message": "the answer_id is either 1 or 2."}, status_code=404)

    except Exception as e:
        return JSONResponse(content={"message": "some internal server error occured"}, status_code=500)


@app.get("/{question_id}/stats")
async def statistics(question_id: int):
    command = f"SELECT option1,option2,poll_1, poll_2 FROM poll_questions WHERE question_id={question_id}"
    stats = connection.execute(text(command))
    try:
        response = list(list(list(stats))[0])
        message = {response[0]: response[2],
                   response[1]: response[3]}
        return message
    except Exception as e:
        return JSONResponse(content={"message": "question index does not exist"}, status_code=404)


@app.get('/addQuestion/{question}/{opt1}/{opt2}')
async def addQuestion(question: str, opt1: str, opt2: str):
    command = f'INSERT INTO poll_questions (question, option1, option2) VALUES ("{unquote(question)}", "{unquote(opt1)}", "{unquote(opt2)}")'
    add_command = connection.execute(text(command))
    connection.commit()
    return JSONResponse(content={"message": "question added"}, status_code=201)