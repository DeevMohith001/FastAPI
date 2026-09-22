from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
import json

app = FastAPI()

class patient(BaseModel):
    id: Annotated[str, Field(..., description='ID of the patient', examples=['p001'])]
    name: Annotated[str, Field(..., description='Name of the patient')]
    city: Annotated[str, Field(..., description='City where the patient is living')]
    age: Annotated[int, Field(..., gt=0, lt=120, description='Name of the patient')]
    gender: Annotated[Literal['male','female','others'], Field(..., description='Gender of the patient')]
    height: Annotated[float, Field(..., gt=0, description='Height of the patient in mtrs')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the patientin kgs')]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi <25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Normal'
        else:
            return 'Obese'

def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)


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
    raise HTTPException(status_code=404, detail='Patient not found')


@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description='Sort on the basis of height, weight or bmi'), order: str = Query('asc', description='Sort in asc or desc order')):
    valid_fields = ['height',  'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field select from {valid_fields}')

    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order select between asc and desc')

    data = load_data()

    sort_order = True if order=='desc' else False

    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data


@app.post('/create')
def create_patient(patient: patient):
    # load existing data
    data = load_data()

    # Check if the patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already eaxists')
    
    # New patient add to the database
    data[patient.id] = patient.model_dump(exclude=['id'])

    # Save into the json file
    save_data(data)

    return JSONResponse(status_code=201, content={'message': 'patient created successfully'})

"""
Notes:
--> Path parameters are the dynamic segmentsof a URL path used to identify a specific resource
--> The Path() function in FastAPI is used to provide metadata validation rules, and documentation hints for the path parameters in your API endpoints
--> Query parameters are the optional key-value pairs appended to the end of a URL, used to pass additional data to the server in an HTTP request.
    They are typically employed for operations like filtering, sorting, searching and  pagination without altering the endpoint path itself.

"""