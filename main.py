import requests
from fastapi import FastAPI, HTTPException, Query
from enum import Enum

app = FastAPI()

class Gender(str, Enum):
    male = 'male'
    female = 'female'


def fetch_random_users(total_results: int, results_per_request: int, gender: Gender = None, nat : str = None, inc : str = None):
    users = []
    num_requests = total_results // results_per_request
    remaining = total_results % results_per_request

    for _ in range(num_requests):
        url = f'https://randomuser.me/api/1.4/?results={results_per_request}'
        if gender:
            url += f'&gender={gender.value}'
        if nat:
            url += f'&nat={nat}'
        if inc:
            url += f'&inc={inc}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            users.extend(data['results'])
        else:
            raise HTTPException(status_code=response.status_code, detail="Error fetching data from Random User API")
    
    if remaining > 0:
        url = f'https://randomuser.me/api/1.4/?results={remaining}'
        if gender:
            url += f'&gender={gender.value}'
        if nat:
            url += f'&nat={nat}'
        if inc:
            url += f'&inc={inc}'

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            users.extend(data['results'])
        else:
            raise HTTPException(status_code=response.status_code, detail="Error fetching data from Random User API")
    
    return users


@app.get('/')
def status_page():
    return {'status': 'ok'}


@app.get('/v1/randomusers/all-data')
def get_random_users(count: int = Query(5000, description="Number of users to fetch, max 1000"),
                    gender: Gender = Query(None, description="Filter by gender (male or female)"),
                    nat: str = Query(None, description='Avaible Country : au, br, ca, ch, de, dk, es, fi, fr, gb, ie, in, ir, mx, nl, no, nz, rs, tr, ua, us'),
                    inc: str = Query(None, description='show data by params : gender, name ,location ,email ,login ,registered ,dob, phone, cell, id, picture, nat')):
    if count > 5000:
        raise HTTPException(status_code=400, detail="Count cannot be greater than 5000")
    
    results_per_request = 1000
    data = fetch_random_users(count, results_per_request, gender, nat, inc)
    
    return {"results": data}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


