## Overview #
This python script is designed to generate the Airflow DAG file using the configuration file.

## How to change the Dag config file #
* Dag config file have the below items. Change the values as required, keep all the lines as it is, otherwise the program may not run properly.
  
  * schedule : '0 3 * * *'		    #Mandatory,Job Schedule 
  * job_name : My_test_job	        #Mandatory,Job Name
  * repo_name : "cloud-composer-dags-finance" # Name to the bitbucket repo were the code has to be pushed
  * email : "email@ntucenterprise.sg" # email id for the person generating the dag
  * branch : master                 # The branch under the destination repository where the files has to be loaded
  * start_delta_days : '2'	        #Optional, This to calcuate the date on which job has to start default value is 2 days
  * email_on_failure : 'False'	    #Optional, Decides on whether you should receive a email alert on failure default value is True
  * email_on_retry : 'True'       	#Optional, Decides on whether you should receive a email alert on retry is enabled default value is False
  * retries : '3'			        #Optional, how many times the dag should retry if there is a failure, default value is 1
  * retry_delay : '5'	            #Optional, interval beteween retry.Only accepts minutes, default value is 5 Minutes
  * concurrency : '5'		        #Optional, How many tasks under the dag should run parallel, default value is 5 Tasks
  * is_paused_upon_creation : 'False'     #Optional, Decide on whether the dag should run once deployed or should hold, default value is False
  * request_cpu : '1'		        #Optional, Number of CPU that should be allocated in the Kube pod, default value is 1
  * request_memory : '300M'       	#Optional, Quantity of internal memory that should be allocated in the Kube pod, default value is 300MB
  * limit_memory : '1G'		        #Optional, Quantity of hdd memory that should be allocated in the Kube pod, default value is 1 GB
  * limit_cpu : '1'		            #Optional, Quantity of hdd memory that should be allocated in the Kube pod, default value is 1 GB
  * etl_config_name : 'etl_conf'	#Mandatory, ETL job config header name inside etl.yml file
  * gcp_project_config: 'gcp'       #Mandatory, Header name inside the configuration for gcp (development.yml/production.yml)
  * gcp_data_ingestion_key: 'sa-coe-data-ingestion' # GCP credentials key
  * source_data_ingestion_key: 'database-credentials� #Soruce DB eg: mysql key

## How to run from CLI #
* The script accepts 3 arguments and all are mandatory:

 * 1) --config_file : This is the Dag config file which contains the information which will be replaced in the dag template file. This will be in ymal format. The values which is accepted are as follows
 * 2) --template_file : This is the common template of the airflow Dag. This has to be downloaded and the file path has to be provided to the script.
 * 3) --generated_Dag_path � This is the path were the generated Dag should be placed. This can be a folder path or a folder path with file name. If it is just a folder path then the file name will be picked from the job name provided in the Dag config file.  

Eg: in Window 
>> python dag_auto_gen.py 
* --config_file="C:\Users\xx\Desktop\config_data\config.yml" 
* --template_file="C:\Users\xxx\Desktop\template\dag_template.py" 
* --generated_dag_path="C:\Users\ronyabraham\Desktop\dags"
* Note: The program will give error if all the mandatory configs are not maintained.