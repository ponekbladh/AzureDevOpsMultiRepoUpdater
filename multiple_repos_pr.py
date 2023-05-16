# Automate similar pull request creation for multiple repositories with a small python 3.7 script.
# All you have to do:
# 1. Provide your Azure DevOps credentials in config section and any other configurations
# 2. Declare repositories and their base branches for which you want to create PR in "repositories_to_base" dictionary in config
# 3. Implement "execute_changes" function

import os
from os import path
from azure.devops.connection import Connection
from azure.devops.v7_1.git.git_client import GitClient
from azure.devops.v7_0.git.models import GitPullRequest,ResourceRef
from msrest.authentication import BasicAuthentication
from config import *
from update_repo import execute_changes_on_repo
from printColor import *

def execute_changes(repository_name):
    print_yellow("Executing changes to repo")
    return execute_changes_on_repo(repository_name)

def get_commit_title():
    return TICKET_COMMIT_TITLE

# Utility functions
def get_connection():
    credentials = BasicAuthentication('', ADO_PERSONAL_ACCESS_TOKEN)
    connection = Connection(base_url=ADO_ORGANIZATION_URL, creds=credentials)
    return connection

def get_gitclient():    
    connection = get_connection()
    git_client = connection.clients.get_git_client()
    return git_client

def get_repository(repository_name):
    git_client = get_gitclient()
    repository = git_client.get_repository(repository_name, ADO_PROJECT)
    return repository

def get_project_from_name(project_name):
    connection = get_connection()
    core_client = connection.clients.get_core_client()

    # Get project details by project name
    project = core_client.get_project(project_name)
    return project

def get_base_branch(repository_name):
    return REPOSITORIES_TO_BASE.get(repository_name)

def clone_repository(repository_name):
    print_yellow("Clone repository %s"%(repository_name))
    os.system("git clone https://%s@%s.visualstudio.com/%s/_git/%s"%(ADO_PERSONAL_ACCESS_TOKEN, ADO_DOMAIN, ADO_PROJECT,repository_name))

def prepare_branch(repository_name, base_branch, branch):
    print_yellow("Preparing ticket branch %s"%(branch))
    os.system("git add --all")
    os.system("git reset --hard head")
    os.system("git checkout %s"%(base_branch))
    os.system("git pull origin %s"%(base_branch))
    run_command_checkout_new_branch = "git checkout -b %s"%(branch)
    os.system(run_command_checkout_new_branch)

def is_anything_to_commit():
    if os.popen('git diff --exit-code').read():
        return True
    print_red("\nNo changes appeared after execution. Skipping...\n")
    return False

def branch_commit(branch):
    print_yellow("Branch commit")
    os.system('git add --all')
    commit_title = get_commit_title()
    os.system("git commit -m\"%s\";"%(commit_title))

def branch_push(branch):
    print_yellow("Branch push")
    os.system("git push origin %s"%(branch))

def create_pr(branch, base_branch, repository_name):
    print_yellow("Creating PR")
    pr_title = get_commit_title()
    pr_body = """
    Ticket: %s

    ### What has been done?
    1. %s

    """%(ADO_TICKET, pr_title)
    
    git_client = get_gitclient()
    repository = get_repository(repository_name)

    pull_request_create = GitPullRequest(
        source_ref_name=f'refs/heads/{branch}',
        target_ref_name=f'refs/heads/{base_branch}',
        title = pr_title,
        description = pr_body,
        is_draft = False,
        work_item_refs = [
            {
                'id': ADO_TICKET
            }
        ]
    )

    pull_request = git_client.create_pull_request(
        git_pull_request_to_create = pull_request_create,
        repository_id = repository.id
    )
    
    print_green("\nPR created, id and title : %s - %s "%(pull_request.pull_request_id, pr_title))

def cleanup(repository_name):
    print_yellow("Cleanup")
    os.chdir("..")
    #os.system("rm -rf %s"%(repository_name))
    run_command = "powershell.exe –noprofile Remove-Item -Path \"%s\\*\" -Force -Recurse"%(WORK_FOLDER)
    os.system(run_command)
    
def execute_changes_on_multiple_repos():
    print_yellow("\n\n\n************************* STARTING REPO UPDATES: *************************\n\n")
    for repository_name in REPOSITORIES_TO_BASE.keys():
        print_yellow("\n\n\n************************* Repository: %s *************************\n\n"%(repository_name))
        base_branch = REPOSITORIES_TO_BASE.get(repository_name)
        os.chdir(WORK_FOLDER)
        clone_repository(repository_name)
        os.chdir(repository_name)
        prepare_branch(repository_name, base_branch, TICKET_BRANCH)
        are_changes_executed = execute_changes(repository_name)
        
        if not are_changes_executed:
            cleanup(repository_name)
            continue

        if not is_anything_to_commit():
            cleanup(repository_name)
            continue

        branch_commit(TICKET_BRANCH)
        branch_push(TICKET_BRANCH)
        create_pr(TICKET_BRANCH, base_branch, repository_name)
        cleanup(repository_name)

    print_yellow("\n\n\n************************* ALL DONE: *************************\n\n")

def execute_changes_single_repo(repository_name):
    base_branch = REPOSITORIES_TO_BASE.get(repository_name)
    os.chdir(WORK_FOLDER)
    os.chdir(repository_name)
    #prepare_branch(repository_name, base_branch, TICKET_BRANCH)
    execute_changes(repository_name)

def run_multiple_builds():
    print_yellow("\n\n\n************************* STARTING BUILDS: *************************\n\n")
    
    connection = get_connection()
    build_client = connection.clients.get_build_client()

    project = get_project_from_name(ADO_PROJECT)
    if project is None:
        print_red("Project not found")
        return

    for repository_build in REPOSITORIES_TO_BUILD_DEFINITION_ID.keys():
        definition_id = REPOSITORIES_TO_BUILD_DEFINITION_ID.get(repository_build)

        # Create a build request
        build_request = {
            'definition': {'id': definition_id},
            'project': {'id': project.id},
            'parameters': f'{{ "{BUILD_PARAMETER_NAME}": "{BUILD_PARAMETER_VALUE_VERISON}" }}'
        }
        
        # Queue the build
        queued_build = build_client.queue_build(build_request, project.id)
        print_green("\nBuild started for: %s"%(repository_build))

# Main
print_yellow("\n\n\n************************* STARTING PROCESS: *************************\n\n")
#run_multiple_builds()
#execute_changes_on_multiple_repos()
#execute_changes_single_repo('reponame')