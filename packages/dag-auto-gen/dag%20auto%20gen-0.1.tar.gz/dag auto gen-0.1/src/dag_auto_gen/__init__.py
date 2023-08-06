import yaml
from jinja2 import Environment, Template, FileSystemLoader
import json  
import sys
import argparse
import os
import logging


def get_config():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_file",help='Dag Config file(Full path with file name)', default="",required=True)
    parser.add_argument("--template_file", help='Dag Template to generate Airflow Dag', default="",required=True)
    parser.add_argument("--generated_dag_path", help='Folder for generated Airflow Dag file', default="")
    args = parser.parse_args()
    return args

def generate_dag(config_file,template_file,generated_dag_path):
    logging.basicConfig(level = logging.INFO)
    stream = yaml.safe_load(open(config_file))
    result={}
    result.update(stream['config'])
    # get template
    template_path = os.path.split(template_file)
    env = Environment(loader=FileSystemLoader(template_path[0]))
    template = env.get_template(template_path[1])

    #Check all Mandatory values are filled in ymal
    if (stream['config']['source_data_ingestion_key'] is None or stream['config']['gcp_data_ingestion_key'] is None
       or stream['config']['data_ingestion_image'] is None or stream['config']['gcp_project_config'] is None
       or stream['config']['etl_config_name'] is None or stream['config']['job_name'] is None
       or stream['config']['schedule'] is None) :
        logging.error( "Required parameters are not maintained in dag config yml file")
        sys.exit("Error encounterd during execution")

    #Then render the results dic as well
    output_from_parsed_template = template.render(result)

    # to save the results
    # check file name already passed as argumnet
    if not os.path.isfile(generated_dag_path):
        output_file = stream['config']['job_name']
        generated_dag_path = os.path.join(generated_dag_path.strip('"'),output_file + '.py')

    with open(generated_dag_path, "w") as fh:
        fh.write(output_from_parsed_template)

    if os.path.isfile(generated_dag_path):
        logging.info("Dag file generated successfully")


#if __name__ == "__main__":
#    args = get_config()
#    generate_dag(args.config_file,args.template_file,args.generated_dag_path)

