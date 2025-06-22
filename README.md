# A scalable job scheduler.

## To start application
- Run the following command
```bash
docker-compose up --build
```

### Use REST API
- [Swagger UI] http://localhost:8000/docs 

### View Database
- [PostgreSQL Admin] http://localhost:8080/

### View Redis
- [Redis UI] http://localhost:8081/

## Task breakup

### Functional requirements
1. Schedule jobs
2. Maintain job-related information
3. endpoint-1. List all jobs
4. endpoint-2. Get details of a job
5. endpoint-3. Create new job
6. Feature - Flexibility in configuration
7. Reoccuring Logic like Schedule every monday

### Non-functional requirements
1. 10000 users - Globally
2. 1000 services
3. 6000 API per minute 


## Architecture
1. Save to persistant storage with horizontal scaling.

Solution: Using postgreSQL server

2. Select jobs that are ready to be scheduled and put in a qriority queue. 

Solution: Redis cluster to implement priority queue using redis sorted set (ZSET).

3. Multiple workers need to pull job according to priority from the queue without conflict.

Solution: Redis supports atomic pop operation which ensures no 2 worker gets the same job.

4. Users should be able to use globally.

Solution: Host multiple instances of the application.
- PostgreSQL servers and redis clusters can scale horizontally.

