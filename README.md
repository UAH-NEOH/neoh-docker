# NEOH-docker

Pre-requisite sofwares

1. Docker (https://www.docker.com/)
2. Postman (https://www.postman.com/)
3. Python 3.9 

System requirements
	Minimum resources allocated to Docker Desktop
	8 GB RAM
	100 GB HDD (Volume-storage)

Steps to use this application

1. Start the Docker Desktop Application

2. Open the terminal, navigate to the neoh-docker directory, execute the following command in the root directory 

		`$ bash build_and_upload.sh` 

## About the files

The `app` directory contains the NEOH source code. The files can be modified to user/developer needs.

The `config.py` file contains the credentials information required for this app to work. To request data from NASA servers. It first needs to be authenticated by the Earthdata 

URS login (https://urs.earthdata.nasa.gov/) If you already have an account enter the username and password in the config.py file. Otherwise, Click Register on the Earthdata URS login page to get started.

**Main.py** Python file contains the Fast API declaration. The user can find all the end-point declarations. Based on the API endpoint, handlers are called to process the user payload. The process will be passed down to `start_cloud_workflow.py`

**Start_cloud_workflow.py** is where the user payload is gathered and processed (boundary files). The request-id is been generated and passed down to the download/aggregate step. The Request id is sent as a response to the user.

**Download_aggregate_opendap_imerg.py** handles the IMERG data download and aggregate process for Precipitation data. 

**Download_aggregate_opendap_modis.py** handles the MODIS data download and aggregate process for Temperature and Vegetation data. 

**Get_result.py** and** Get_status.py** is used to read the result and status of the requests inside the Docker

**Sn_bound_10deg.txt** boundary reference files used in the MODIS process

**Neoh_utils.py** The python helper library for creating directories and writing status information inside Docker.

**Requirements.txt**
	The file contains the python dependency libraries for the NEOH process. This will be installed inside the Docker. 


The Dockerfile has the step by step instructions for the installation and setup of the python tools in a virtual machine inside the Docker

## The Bash scripts: 

**Build_and_upload.sh**
	Builds the Docker image and uploads it to the Docker Desktop app
Also, stops and removes the previous setup with the same name (if any). This step is required for continuous development and deployment.
Runs the Docker in the specified port. The default is 80:80.

**Build_and_run_local.sh**
	Builds the Docker image and runs the service locally

**Run_local.sh**
Run the Python server without installing the dependencies. The dependencies should be already installed
