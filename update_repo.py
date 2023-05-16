import os
import xml.etree.ElementTree as ET
from printColor import *
from config import *
#from env.config import *

target_nuget_folder = 'Peap'
target_nuget_file = 'packages.config'
ATTRIBUTE_ID_VERSION = 'version'
ATTRIBUTE_ID_ID = 'id'
ENCODING_UTF_8 = 'utf-8'

def find_packages_file(target_folder, target_file):
    file_path = ''

    for root, dirs, files in os.walk('.'):
        if target_folder in dirs:
            folder_path = os.path.join(root, target_folder)
            for root, dirs, files in os.walk(folder_path):
                if target_file in files:
                    file_path = os.path.join(root, target_file)
            break
    else:
        # If the file is not found, print an error message and exit the program
        print_red(f"File '{target_file}' not found in folder '{target_folder}'")
    return file_path

def find_by_attribute_replace_attribute(root, target_attribute, taret_attribute_val, update_attribute, update_attribute_val):
    # Find the child element with the specific id attribute value
    target_element = None
    for child in root:
        attri_val = child.attrib.get(target_attribute)
        #if child.attrib.get(target_attribute) == taret_attribute_val:
        if child.attrib.get(target_attribute) == taret_attribute_val:
            target_element = child
            break

    # Update a specific attribute value in the child element
    if target_element is not None:
        target_element.set(update_attribute, update_attribute_val)

def update_nuget_packages(repository_name):
    print_yellow("Updating packages.config for repo %s"%(repository_name))
    
    file_path = find_packages_file(target_nuget_folder, target_nuget_file)
    
    if file_path == '':
        print_red("packages.config not found, skip update versions")
        return False
    
    print_yellow("packages.config found, updating versions")

    # Load the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    for package_id in NEW_BUILD_PACKAGE_VERION_FINPS.keys():
        find_by_attribute_replace_attribute(root, ATTRIBUTE_ID_ID, package_id, ATTRIBUTE_ID_VERSION, NEW_BUILD_PACKAGE_VERION_FINPS.get(package_id))

    # Write the updated XML to a file
    tree.write(file_path, encoding=ENCODING_UTF_8, xml_declaration=True)
    return True

def replace_file_content(file_path, new_content):
    try:
        with open(file_path, 'w') as file:
            file.write(new_content)
        print(f"Successfully replaced the content of {file_path}.")
        return True
    except IOError:
        print(f"Error occurred while replacing the content of {file_path}.")
        return False

def update_nuget_config(repository_name):
    file_path = find_packages_file(target_nuget_folder, 'nuget.config')
    
    if file_path == '':
        print_red("nuget.config not found, skip update versions")
        return False
    
    print_yellow("nuget.config found, updating versions")

    nuget_config = ADO_NUGET_CONFIG

    return replace_file_content(file_path, nuget_config);

def execute_changes_on_repo(repository_name):
    #apply_changes_success = update_nuget_packages(repository_name)
    apply_changes_success = update_nuget_config(repository_name)
    return apply_changes_success