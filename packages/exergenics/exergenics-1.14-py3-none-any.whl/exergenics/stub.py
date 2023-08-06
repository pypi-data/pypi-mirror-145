from exergenics import ExergenicsApi

api = ExergenicsApi("apiteam@exergenics.com", "M3nt4llyF1t", False)

api.authenticate()

api.getJob(2)
print(api.numResults())

if api.numResults() == 1:
    job = api.nextResult()
    print(job)

# load jobs that are created_ready and waiting for something to do.
api.getJobs("created_ready", "waiting")

jobs = []

if api.numResults() == 0:
    print("No jobs found")
else:
    while api.moreResults():
        jobs.append(api.nextResult())

for i in range(len(jobs)):
    api.setJobStageComplete(jobs[i]['jobId'])
