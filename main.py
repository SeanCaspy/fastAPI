from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def read_root():
    return {'message': 'welcome to my first api'}

@app.get('/hello')
def say_hello(name: str = 'Sean'):
    return {'message' : f"hello {name}"}
