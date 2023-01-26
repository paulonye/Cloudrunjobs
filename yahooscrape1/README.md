# YahooScrape->GoogleSheets
>In this project, an Extract, Transform, and Load Pipeline application alongside all its dependencies is packaged and contanarized into a dokcer container.
>
>The project focuses on deploying the scraper application built in [Project one](https://github.com/paulonye/Smart_Sheet) on Google Cloud Run, a mangaged compute platform that allows you run stateless containers. 
>
>The Project is the 2nd series in my "Building your first Google Cloud Analytics Project"
>
>The Project is also a direct sequel to the [First Project](https://github.com/paulonye/Smart_Sheet)
>
>[Link to the Yahoo Finance Website](https://finance.yahoo.com/crypto/?.tsrc=fin-srch&offset=0&count=15)
>
>[Link to the Medium Article](https://medium.com/@nwosupaul141/building-an-etl-pipeline-using-google-service-accounts-85e2a6cfd94d) 

## Project Structure

- Background of Data Scraper
- Basics of Docker
- Building the Docker Image
- Running the Docker image locally
- Introduction to Artifact Registry
- Introduction to Google Cloud Run Jobs
- Configuration settings of Cloud Run
- Setting up a scheduler for the Cloud Run Job

![Cover_Image](https://storage.googleapis.com/images-xlr1001/cover2.png)
 
## Set up your environment
Clone the Github Repo 
```bash
   git clone https://github.com/paulonye/Cloudrunjobs.git
```

## Build the Docker Image
`cd` into the directory of the cloned repo, open the `Dockerfile` and make the changes you need to make. It is well documented, so just follow through.

Some changes to watch out for:
- Directory and Name of the service account.
- Name of the environment variable for the service account.
- The Name of the Google Sheets and the name of the worksheet that you will be using
- Remember to attach the service account email address to the Google Sheet, and also give edit access as explained in project one.

Once this is done; you can then build the docker image using
```bash
    docker build -t image_name .
```
The above command builds the docker image; to test that it works, use:
```bash
   docker run image_name
```
Once you are sure that it works, go ahead and set up the artifact registry as described in the medium article above.

## Pushing the Docker Container Image to Artifact registry
Authenticate to the Region where your Artifact Registry is located
```bash
   gcloud auth configure-docker us-central1-docker.pkg.dev
```
Build the Docker Image for Artifact Registry
```bash
   docker build -t us-central1-docker.pkg.dev/my-project/my-repo/my-image:tag1 .
```
Where `my-project` is your GCP Project ID and `my-repo` is the name of the repo you created on artifact registry.
Push the Docker Image to Artifact Registry
```bash
   docker push us-central1-docker.pkg.dev/my-project/my-repo/my-image:tag1
```
Deploy the Container on Cloud Run
```bash
   gcloud beta run jobs create job-quickstart --image image_name:tag --region us-central1
```
 ## Schedule a Cron job using Google Cloud Scheduler