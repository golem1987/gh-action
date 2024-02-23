import yaml
import sys

deleted_services = []
services_with_decreased_version=[]
deleted = []
decreased = []
del_service = 0
dec_version = 0

def parse_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)
    
def new_dict(dictionary):
    new_dictionary = {}
    for key, value in dictionary.items():
        if isinstance(value, dict):
            if 'imageTag' in value:
                new_dictionary[key] = value['imageTag']
    return new_dictionary

def compare_versions(main_version, pr_version):
    for key, value in pr_version.items():
        if key in main_version:
            if value < main_version[key]:
                print(f"::set-output name=images::Version for service {key} is decreased from {main_version[key]} to {value}")
                services_with_decreased_version.append(key)

def check_for_deleted_services(main_version, pr_version):
    for key, value in main_version.items():
        if key not in pr_version:
            deleted_services.append(key)

def print_services_info_and_exit():
    messages = []
    exit_code = 0 
    if deleted_services:
        deleted_services_str = ', '.join(deleted_services)
        deleted.append(f"Deleted Services: {deleted_services_str}")
    if services_with_decreased_version:
        services_with_decreased_version_str = ', '.join(services_with_decreased_version)
        decreased.append(f"Services with decreased version: {services_with_decreased_version_str}")

if __name__ == '__main__':

    main_values = parse_yaml("/tmp/basevalues.yaml")
    pr_values = parse_yaml("/tmp/prvalues.yaml")

    pr_dict=new_dict(pr_values)
    master_dict=new_dict(main_values)

    compare_versions(master_dict, pr_dict)
    check_for_deleted_services(master_dict, pr_dict)

    print_services_info_and_exit()
    
    if deleted_services:
        del_service = 1
    if services_with_decreased_version:
        dec_version = 1

    print(f"::set-output name=del_service::{del_service}")
    print(f"::set-output name=dec_version::{dec_version}")
    print(f"::set-output name=dec_ver_msg::{', '.join(deleted)}")
    print(f"::set-output name=del_ver_msg::{', '.join(decreased)}")