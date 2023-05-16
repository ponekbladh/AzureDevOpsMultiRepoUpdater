# To keep secrets separate, create a empty file in subfolder env called __init__.py
# Copy config.py into the env folder, add secrets and modify the code to use
# from env.config import * 
# instead of 
# from config import *

#FinOps
NEW_BUILD_VERSION_FINOPS = '10.0.34 PEAP'

NEW_BUILD_PACKAGE_VERION_FINPS = {
    'Microsoft.Dynamics.AX.Application.DevALM.BuildXpp': '10.0.1515.44',
    'Microsoft.Dynamics.AX.ApplicationSuite.DevALM.BuildXpp': '10.0.1515.44',
    'Microsoft.Dynamics.AX.Platform.CompilerPackage': '7.0.6801.37',
    'Microsoft.Dynamics.AX.Platform.DevALM.BuildXpp': '7.0.6801.37'
}

#Global
WORK_FOLDER = 'C:\\temp\\updateRepos'

#AzureDevOps
ADO_AAD_ALIAS = 'johnsmith'
ADO_PERSONAL_ACCESS_TOKEN = 'Personal access token with full access'
ADO_DOMAIN = 'Azure devops org'
ADO_ORGANIZATION_URL = "https://dev.azure.com/%s"%(ADO_DOMAIN)
ADO_PROJECT = ''
ADO_TICKET = ""
TICKET_BRANCH = "user/%s/%s-update"%(ADO_AAD_ALIAS, ADO_TICKET)
TICKET_COMMIT_TITLE = "fix: Updated XYZ"
ADO_NUGET_CONFIG = """<?xml version="1.0" encoding="utf-8"?>
<configuration>
<packageSources>
    <clear />
</packageSources>
</configuration>"""

# Repositories to update
REPOSITORIES_TO_BASE = {
    'first repo name': 'master',
    'second repo name': 'main',
    'third repo name': 'main'
}

#Builds to start
BUILD_PARAMETER_NAME = 'BuildVersion'
BUILD_PARAMETER_VALUE_VERISON = '10.0.34'

#Find the build definition id by opening azure devops and navigating to the build, see id in url
REPOSITORIES_TO_BUILD_DEFINITION_ID = {
    'first repo name': '101',
    'second repo name': '131',
    'third repo name' : '227'
}