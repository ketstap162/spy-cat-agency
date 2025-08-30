# Spy Cat Agency (SCA)

Spy Cat Agency (SCA) is a management application, so that it simplifies their spying work processes. SCA needs a system to manage their cats, missions they undertake, and targets they are assigned to.

From cats perspective, a mission consists of spying on targets and collecting data. One cat can only have one mission at a time, and a mission assumes a range of targets (minimum: 1, maximum: 3). While spying, cats should be able to share the collected data into the system by writing notes on a specific target. Cats will be updating their notes from time to time and eventually mark the target as complete. If the target is complete, notes should be frozen, i.e. cats should not be able to update them in any way. After completing all of the targets, the mission is marked as completed.

From the agency perspective, they regularly hire new spy cats and so should be able to add them to and visualize in the system. SCA should be able to create new missions and later assign them to cats that are available. Targets are created in place along with a mission, meaning that there will be no page to see/create all/individual targets.

# How to start:
1) Clone this repository.
2) Copy `.env.sample` to `.env`
3) Run Docker engine.
4) Run `docker-compose build` in Terminal.
5) Run `docker-compose up` in Terminal after building.

# Docs
Docs provided on this endpoints:
`http://127.0.0.1:8000/docs` - for Swagger
`http://127.0.0.1:8000/redoc` - for Redoc
