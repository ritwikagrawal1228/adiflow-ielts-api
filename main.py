# Ritwik - Date= 22 may 2023, this code runs perfectly but is without CA Cert and SSL
# api built for 
# 1. getting questions from qb_reading table @app.get("/questions")
# 2. getting passages from passage_reading table @app.get("/passages")
# 3. getting listening questions from qb_listening table @app.get("/listening-questions")
# 4. getting listening audio url from audio_listening table @app.get("/audio-questions")
# 5. getting writing questions from qb_writing table @app.get("/writing-questions")
# 6. getting speaking questions from qb_speaking table @app.get("/speaking-questions")
# 7. getting test from test-table @app.get("/test")
# 8. getting question sets from question-sets table @app.get("/question-sets")
# 9. posting user response to ua-writing table @app.post("/ua-writing")
# 10. getting user response from ua-writing table @app.get("/ua-writing")
# 11. posting user response to ua-speaking table @app.post("/ua-speaking")
# 12. getting user response from ua-speaking table @app.get("/ua-speaking")




from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
import uvicorn
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from mangum import Mangum

now = datetime.now()
iso_string = now.isoformat()




# Set up a connection to CockroachDB using psycopg2
db_config = {
    "dbname": "defaultdb",
    "user": "ritwik_ag",
    "password": "XtcPQ6tFqArWPGynlpnXVA",
    "host": "unsung-ewe-4766.6xw.cockroachlabs.cloud",
    "port": "26257"

    # "sslmode": "verify-full",
    # "sslrootcert": "path/to/ca.crt"  # Replace with the path to your CA certificate file

}

# Create a FastAPI application instance
app = FastAPI()

#For aws lambda handler

handler = Mangum(app)

# Define a route to retrieve questions from the qb_reading table
    # """
    # Retrieves all the questions from the database.

    # Returns:
    #     A JSONResponse containing all the questions.

    # Raises:
    #     HTTPException (status_code=500): If there is an error connecting to the database.
    # """
@app.get("/questions")
def get_questions():
    try:
        # Establish a connection to the PostgreSQL database using the provided configuration
        conn = psycopg2.connect(**db_config)
        # Create a cursor object from the connection using RealDictCursor to return rows as dictionaries instead of tuples
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # Define a SQL query to select all rows from the "qb_reading" table
        query = "SELECT * FROM qb_reading"
        # Execute the query using the cursor
        cursor.execute(query)

        # Fetch all rows returned by the query
        questions = cursor.fetchall()

        # Return the fetched rows as a JSON response
        return JSONResponse(content=questions)

    # Catch any errors that occur during execution of the try block and raise an HTTPException with a 500 status code and the error message
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Close the cursor and connection objects regardless of whether the try block succeeded or raised an exception
    finally:
        cursor.close()
        conn.close()

# Define a function to fetch all passages from the database
@app.get("/passages")
def get_passages():
    try:
        # Connect to the database
        conn = psycopg2.connect(**db_config)
        # Create a cursor object to execute SQL queries
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # Define the SQL query to fetch all passages from the database
        query = "SELECT * FROM passage_reading"
        # Execute the SQL query
        cursor.execute(query)

        # Fetch all the passages from the database
        passages = cursor.fetchall()

        # Return the fetched passages as a JSON response
        return JSONResponse(content=passages)

    # Handle any exceptions raised during the execution of the code
    except psycopg2.Error as e:
        # Raise an HTTPException with a 500 status code and the error message
        raise HTTPException(status_code=500, detail=str(e))

    # Close the cursor and the database connection, regardless of whether an exception is raised or not
    finally:
        cursor.close()
        conn.close()

@app.get("/passages/{passage_id}")
def get_passage_by_id(passage_id: int):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        query = "SELECT * FROM passage_reading WHERE id = %s"
        cursor.execute(query, (passage_id,))

        passage = cursor.fetchone()

        if passage:
            return JSONResponse(content=passage)
        else:
            raise HTTPException(status_code=404, detail="Passage not found")

    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()

@app.get("/listening-questions")
def get_listening_questions():
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        query = "SELECT * FROM qb_listening"
        cursor.execute(query)

        questions = cursor.fetchall()

        return JSONResponse(content=questions)

    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()

@app.get("/listening-questions/{question_id}")
def get_listening_question_by_id(question_id: int):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        query = "SELECT * FROM qb_listening WHERE id = %s"
        cursor.execute(query, (question_id,))

        question = cursor.fetchone()

        if question:
            return JSONResponse(content=question)
        else:
            raise HTTPException(status_code=404, detail="Question not found")

    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()
@app.get("/audio-questions")
def get_audio_questions():
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        query = "SELECT * FROM audio_listening"
        cursor.execute(query)

        questions = cursor.fetchall()

        return JSONResponse(content=questions)

    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()
@app.get("/audio-questions/{question_id}")
def get_audio_question_by_id(question_id: int):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        query = "SELECT * FROM audio_listening WHERE id = %s"
        cursor.execute(query, (question_id,))

        question = cursor.fetchone()

        if question:
            return JSONResponse(content=question)
        else:
            raise HTTPException(status_code=404, detail="Question not found")

    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()


@app.get("/writing-questions")
def get_writing_questions():
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        query = "SELECT * FROM qb_writing"
        cursor.execute(query)

        questions = cursor.fetchall()

        return JSONResponse(content=questions)

    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()


@app.get("/writing-questions/{question_id}")
def get_writing_question_by_id(question_id: int):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        query = "SELECT * FROM qb_writing WHERE id = %s"
        cursor.execute(query, (question_id,))

        question = cursor.fetchone()

        if question:
            return JSONResponse(content=question)
        else:
            raise HTTPException(status_code=404, detail="Question not found")

    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()

@app.get("/speaking-questions")
def get_speaking_questions():
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        query = "SELECT * FROM qb_speaking"
        cursor.execute(query)

        questions = cursor.fetchall()

        return JSONResponse(content=questions)

    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()

@app.get("/speaking-questions/{question_id}")
def get_speaking_question_by_id(question_id: int):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        query = "SELECT * FROM qb_speaking WHERE id = %s"
        cursor.execute(query, (question_id,))

        question = cursor.fetchone()

        if question:
            return JSONResponse(content=question)
        else:
            raise HTTPException(status_code=404, detail="Question not found")

    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()

@app.get("/tests")
def get_tests():
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        query = "SELECT * FROM test_table"
        cursor.execute(query)

        tests = cursor.fetchall()

        return JSONResponse(content=tests)

    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()


@app.get("/tests/{test_id}")
def get_test_by_id(test_id: int):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        query = "SELECT * FROM test_table WHERE id = %s"
        cursor.execute(query, (test_id,))

        test = cursor.fetchone()

        if test:
            return JSONResponse(content=test)
        else:
            raise HTTPException(status_code=404, detail="Test not found")

    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()

@app.get("/question-sets")
def get_question_sets():
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        query = "SELECT * FROM question_sets"
        cursor.execute(query)

        question_sets = cursor.fetchall()

        return JSONResponse(content=question_sets)

    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()


@app.get("/question-sets/{question_set_id}")
def get_question_set_by_id(question_set_id: int):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        query = "SELECT * FROM question_sets WHERE id = %s"
        cursor.execute(query, (question_set_id,))

        question_set = cursor.fetchone()

        if question_set:
            return JSONResponse(content=question_set)
        else:
            raise HTTPException(status_code=404, detail="Question set not found")

    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()

class WritingResponse(BaseModel):
    user_code: str
    question_code: str
    user_essay: str
    timestamp: datetime
    assessed_status: bool
    question_code_id: str

@app.post("/writing-responses")
def create_writing_response(response: WritingResponse):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        query = "INSERT INTO ua_writing (user_code, question_code, user_essay, timestamp, assessed_status, question_code_id) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (response.user_code, response.question_code, response.user_essay, response.timestamp, response.assessed_status, response.question_code_id))
        conn.commit()

        return {"message": "Writing response created successfully"}

    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()


from datetime import datetime

@app.get("/writing-responses")
def get_writing_responses():
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        query = "SELECT * FROM ua_writing"
        cursor.execute(query)

        writing_responses = cursor.fetchall()

        # Convert datetime objects to string representation
        for response in writing_responses:
            response['timestamp'] = response['timestamp'].strftime('%Y-%m-%d %H:%M:%S')

        return JSONResponse(content=writing_responses)

    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()

class SpeakingResponse(BaseModel):
    user_code: str
    question_code: str
    user_audio_url: str
    timestamp: str
    assessed_status: bool
    transcribed_status: bool
    question_code_id: int


@app.post("/speaking-responses")
def create_speaking_response(response: SpeakingResponse):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        query = "INSERT INTO ua_speaking (user_code, question_code, user_audio_url, timestamp, assessed_status, transcribed_status, question_code_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (response.user_code, response.question_code, response.user_audio_url, response.timestamp, response.assessed_status, response.transcribed_status, response.question_code_id))
        conn.commit()

        return {"message": "Speaking response created successfully"}

    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()


@app.get("/speaking-responses")
@app.get("/speaking-responses")
def get_speaking_responses():
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        query = "SELECT * FROM ua_speaking"
        cursor.execute(query)

        speaking_responses = cursor.fetchall()

        # Convert datetime objects to strings
        for response in speaking_responses:
            response["timestamp"] = response["timestamp"].strftime("%Y-%m-%d %H:%M:%S")

        return JSONResponse(content=speaking_responses)

    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()





#END STATEMENT 
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
