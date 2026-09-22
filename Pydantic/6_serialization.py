from pydantic import BaseModel

class Address(BaseModel):

    city: str
    state: str
    pin: str

class Patient(BaseModel):

    name: str
    gender: str = 'Male'
    age: int
    address: Address

address_dict = {'city': 'gurgaon', 'state': 'haryana', 'pin': '122001'}

address1 = Address(**address_dict)

patient_dict = {'name': 'nitish', 'age': 35, 'address': address1}

patient1 = Patient(**patient_dict)

# temp = patient1.model_dump(exclude=['name', 'gender']) # name and gender will be removed
# temp = patient1.model_dump(include=['name', 'gender']) # only name and gender will be shown
# temp = patient1.model_dump(exclude={'address':['state']})
temp = patient1.model_dump(exclude_unset=True) # Things which was not set during the object creation, will not be shown now


print(temp)
print(type(temp))