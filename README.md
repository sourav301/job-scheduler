# A scalable job scheduler.

## To start application
- Run the following command
```bash
docker-compose up --build
```

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

If 100% of the queries are write queries then 8.64 million rows per day.

Solution: Using postgreSQL server with
- Index for job_status and run_at
- Partition by date

2. Select jobs that are ready to be scheduled and put in a qriority queue. 

Solution: Redis cluster to implement priority queue using redis sorted set (ZSET).

3. Multiple workers need to pull job according to priority from the queue without conflict.

Solution: Redis supports atomic pop operation which ensures no 2 worker gets the same job.

4. Users should be able to use globally.

Solution: Host multiple instances of the application.
- PostgreSQL servers and redis clusters can scale horizontally.

