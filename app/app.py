from fastapi import FastAPI
# from imagekitio import 

app= FastAPI()

@app.get("/hello-world")
def hello_world():                       # Function name should be same or similar to the decorator
    return {"message": "Hello World"}    # Should be in Pydantic Format