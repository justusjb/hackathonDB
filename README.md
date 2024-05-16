# hackathonDB

This is the place to find all hackthons around the world

## The current state of HackathonDB

For the first step, I set up MongoDB Atlas and created a cluster. I also created a database called `hackathonDB` 
and a collection called `hackathons`. I have added a few hackathons to the collection.

The mondoDB_test.ipynb file has some code of me getting my hands dirty with the MongoDB Python driver.

There is a simple API endpoint in the `backend` folder that returns all hackathons in the collection. This is deployed 
on the DigitalOcean App Platform.
There is now a form to add hackathons to the database. This is not deployed on purpose.

Along with that, I have created a simple frontend in SvelteKit that connects to the endpoint and displays all hackathons. 
This is deployed on Vercel.

## How to run the project
### Backend
In the `backend` folder set up a virtual environment and install the requirements. 
Set the environment variable `MONGO_URI` to the MongoDB connection string. 
Also set the environment variable `LOCAL_DEV` to `True` if you want to activate data entry form.
Then start the backend server:

#### Locally:
```
uvicorn main:app --reload
```

#### On DigitalOcean:
```
uvicorn main:app --host 0.0.0.0 --port 8080
```

### Frontend
In the `frontend` folder install the dependencies and start the frontend server:

```
npm install
npm run dev
```
