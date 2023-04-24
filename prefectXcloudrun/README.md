# SERVERLESS DEPLOYMENT OF A PREFECT PIPELINE ON GOOGLE CLOUD RUN
>In this project, Prefect is used to orchestrate a Data Pipeline and Deploy it on Google Cloud Run.
>
>The project focuses on orchestrating the pipeline for the scraper application that extracts data from Yahoo Finance and Loads it into Google Cloud Storage.
>
>The Project is my final submission for the `Data Engineering Zoomcamp`
>
>[Link to the Yahoo Finance Website](https://finance.yahoo.com/crypto/?.tsrc=fin-srch&offset=0&count=100)
>
>[Link to the Medium Article](https://medium.com/@nwosupaul141/serverless-deployment-of-a-prefect-data-pipeline-on-google-cloud-run-8c48765f2480)
>
>[Link to the Previous Medium Article](https://medium.com/@nwosupaul141/orchestrating-data-pipelines-with-prefect-on-gcp-infrastructure-cdc7aaf42250) 
>
>[Setting your Environment on a Virtual Machine](https://medium.com/@nwosupaul141/optimizing-googles-cloud-infrastructure-for-data-engineering-and-analytics-49d1d91fe7b6)
>
>[Understanding how to Deploy on Google Cloud Run](https://medium.com/@nwosupaul141/deployment-of-containerized-data-applications-on-google-cloud-run-pt1-80750dce02f8)

## Project Structure

- Setting up the Environment
- Building and Pushing the Docker Image to Artifact Registry
- Deploying the Flow
- Running the Deployment

## Final Dashboard
![Dashboard_Image](https://nwosupaulonye2.s3.amazonaws.com/dashboard.png)

>[Link to Dashboard](https://lookerstudio.google.com/reporting/9ce9b40b-7ae9-436c-929d-e2eb44efcc29/page/enCCD/edit)

<br>

![Cover_Image](https://nwosupaulonye.s3.amazonaws.com/cover6.png)
 
## Set up your environment
Clone the Github Repo 
```bash
   git clone https://github.com/paulonye/Cloudrunjobs.git
```
Set up your Virtual Environment
```bash
   python -m venv env

   source env/bin/activate
```
Install the Required Libraries in the Virtual Environment
```bash
   pip install -r requirements.txt
```
Authenticate into your Prefect Cloud Workspace on the terminal
```bash
   prefect cloud login

   #Add your API key
```
Confirm that you have the right Google Cloud Credentials set
```bash
   gcloud config list

   gcloud auth application-default login
   #this will allow third party application access
```

## Building and Pushing the Docker Image to Artifact Registry
In the directory of the cloned repo, open the `Dockerfile` and make the changes you need to make. It is well documented, so just follow through.

Authenticate to the Region where your Artifact Registry is located
```bash
   gcloud auth configure-docker us-east1-docker.pkg.dev
```
Build the Docker Image for Artifact Registry
```bash
   docker build -t us-east1-docker.pkg.dev/my-project/my-repo/my-image:tag1 .
```
Where `my-project` is your GCP Project ID and `my-repo` is the name of the repo you created on artifact registry.
Push the Docker Image to Artifact Registry
```bash
   docker push us-east1-docker.pkg.dev/my-project/my-repo/my-image:tag1
```

## Deploying the Flow
 To deploy the flow, ensure you create the docker block on your prefect cloud workspace.
 Run the command to deploy
```bash
   prefect deployment build pipeline.py:main -n test-dev -ib cloud-run-job/dev -q dev -o dev.yaml
   
   #make changes to the dev.yaml file by adding the url parameter, then push the deployment to prefect cloud

   prefect deployment apply dev.yaml
```
Once the deployment has been made, navigate to the workspace to view it.

## Running the Deployment
To run the deployment, we need to set the prefect agent in our environment
For this, we need to set it up a detached environment, and we can do this using `tmux`
```bash
    tmux
    #this opens a new terminal window

    source emv/bin/activate
    #activate the virtual environment where you installed prefect

    prefect agent start -q dev
    #deploy the prefect agent to pickup workqueues from dev which is the name of the work queue we defined for our deployment to send its flows

    ctrl+D, B
    #detach from the tmux window

    tmux ls
    #list the tmux sessions currently running

    tmux attach -t 0
    #reattach to the tmux session

    tmux kill-session -t 0
    #kill the session
```
Navigate to your prefect workspace to start the flow.

The Prefect agent will pick up the flow run and orchestrate the entire process. This includes creating the necessary infrastructure on Google Cloud Run, submitting the flow to the cloud-run job, monitoring the run, and cleaning up resources once the job is completed.

You can also choose to schedule the deployment, just make sure you keep the prefect agent running.
