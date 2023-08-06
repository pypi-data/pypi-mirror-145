import yaml
from yaml.loader import SafeLoader
from os.path import exists
import os

file_exists = exists(os.getcwd()+'/audit-dog.yml')

if not file_exists:
    with open('spec.yml', 'r') as f:
        yaml_data = list(yaml.load_all(f, Loader=SafeLoader))
        # print(yaml_data)

    yml_data = [{'client':yaml_data[0]['client'],'repo_name':yaml_data[0]['name'],'repo_description':yaml_data[0]['description']}]
    with open('audit-dog.yml', 'w') as f:
        data = yaml.dump(yml_data, f, sort_keys=False, default_flow_style=False)


