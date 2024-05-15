# hackathonDB

This is the place to find all hackthons around the world

## The current state of HackathonDB

For the first step, I set up MongoDB Atlas and created a cluster. I also created a database called `hackathonDB` 
and a collection called `hackathons`. I have added a few hackathons to the collection.

The mondoDB_test.ipynb file has some code of me getting my hands dirty with the MongoDB Python driver.

There is a simple API endpoint in the `backend` folder that returns all hackathons in the collection. This will be 
deployed on some PaaS, probably DigitalOcean App Platform.

Along with that, I have created a simple frontend in SvelteKit that connects to the endpoint and displays all hackathons. 
This will be deployed on Vercel.
