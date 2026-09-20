from fastapi import FastAPI, Path
import json

app = FastAPI()

def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data

@app.get("/")
def hello():
    return {'message':'Patient Management System API'}

@app.get('/about')
def about():
    return {'message': 'A fully functional API to manage your patient records'}


# Creating an endpoint which will give all the patients data to the client
@app.get('/view')
def view():
    data = load_data()
    return data


@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description='ID of the patient in the DB', example='p001')):
    # load all the patients
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    return {'error':'patient not found'}



"""
Notes:
--> Path parameters are the dynamic segmentsof a URL path used to identify a specific resource
--> The Path() function in FastAPI is used to provide metadata validation rules, and documentation hints for the path parameters in your API endpoints

"""