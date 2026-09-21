from fastapi import FastAPI, HTTPException, Path, Query
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




"""
Notes:
--> Path parameters are the dynamic segmentsof a URL path used to identify a specific resource
--> The Path() function in FastAPI is used to provide metadata validation rules, and documentation hints for the path parameters in your API endpoints
--> Query parameters are the optional key-value pairs appended to the end of a URL, used to pass additional data to the server in an HTTP request.
    They are typically employed for operations like filtering, sorting, searching and  pagination without altering the endpoint path itself.

"""