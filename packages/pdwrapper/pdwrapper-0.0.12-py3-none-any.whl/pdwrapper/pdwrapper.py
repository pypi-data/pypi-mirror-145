import click
import logging
import sys,os
import yaml
import jsonschema
import subprocess
import boto3
from botocore.exceptions import ClientError
from datetime import datetime, timezone
from time import time

##############################################
# Global Variables
##############################################
aws_profile = os.getenv('AWS_PROFILE')
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
git_branch = os.getenv('GITHUB_REF_NAME', '')
git_commit = os.getenv('GITHUB_SHA', '')
git_author = os.getenv('GITHUB_ACTOR', '')

allowed_app_types = ['ui', 'service', 'infra']

default_ui_yaml_schema = {
    "type" : "object",
    "properties": {
        "name" : { "type" : "string" },
        "type" : { "type" : "string" },
        "deploy" : { "type" : "boolean" },
        "stages" : { "type" : "array" }
    },
    "required": ["name", "type", "deploy", "stages"]
}
rollback_ui_yaml_schema = {
    "type": "object",
    "properties": {
        "name": { "type": "string" },
        "type": { "type": "string" },
        "deploy": { "type": "boolean" },
        "stages": { "type": "array" },
        "pipeline_metadata": {
            "type": "object",
            "properties": {
                "deploy": {
                    "type": "object",
                    "properties": {
                        "version":{ "type": "string" },
                        "s3_bucket":{ "type": "string" },
                        "status": { "type": "boolean" },
                        "invalidate_cache": { "type": "boolean" },
                        "last_version": { "type": "string" },
                        "last_version_folder": { "type": "string" },
                    },
                    "required": ["version", "s3_bucket", "status", "invalidate_cache", "last_version", "last_version_folder"]
                }
            },
            "required": ["deploy"]
        }
    },
    "required": ["name", "type", "deploy", "stages", "pipeline_metadata"]
}

default_infra_yaml_schema = {
    "type" : "object",
    "properties": {
        "name" : { "type" : "string" },
        "type" : { "type" : "string" },
        "deploy" : { "type" : "boolean" },
        "stages" : { "type" : "array" },
        "regions" : { "type" : "array" }
    },
    "required": ["name", "type", "deploy", "stages", "regions"]
}
rollback_infra_yaml_schema = {
    "type": "object",
    "properties": {
        "name": { "type": "string" },
        "type": { "type": "string" },
        "deploy": { "type": "boolean" },
        "stages": { "type": "array" },
        "regions": { "type": "array" },
        "pipeline_metadata": {
            "type": "object",
            "properties": {
                "cloudformation_stack": { "type": "string" },
                "deploy": {
                    "type": "object",
                    "properties": {
                        "run":{ "type": "string" },
                        "status": { "type": "boolean" },
                        "timestamp_last": { "type": "string" }
                    },
                    "required": ["status", "timestamp_last"]
                }
            },
            "required": ["cloudformation_stack", "deploy"]
        }
    },
    "required": ["name", "type", "deploy", "stages", "regions", "pipeline_metadata"]
}

default_service_yaml_schema = {
    "type" : "object",
    "properties": {
        "name" : { "type" : "string" },
        "type" : { "type" : "string" },
        "deploy" : { "type" : "boolean" },
        "stages" : { "type" : "array" },
        "regions" : { "type" : "array" },
        "migrations" : { "type" : "boolean" },
        "sfsp" : { "type" : "boolean" }
    },
    "required": ["name", "type", "deploy", "stages", "regions", "migrations", "sfsp"]
}
rollback_service_yaml_schema = {
    "type": "object",
    "properties": {
        "name": { "type": "string" },
        "type": { "type": "string" },
        "deploy": { "type": "boolean" },
        "stages": { "type": "array" },
        "regions": { "type": "array" },
        "migrations": { "type": "boolean" },
        "sfsp": { "type": "boolean" },
        "pipeline_metadata": {
            "type": "object",
            "properties": {
                "cloudformation_stack": { "type": "string" },
                "deploy": {
                    "type": "object",
                    "properties": {
                        "run":{ "type": "string" },
                        "status": { "type": "boolean" },
                        "timestamp_last": { "type": "string" }
                    },
                    "required": ["status", "timestamp_last"]
                }
            },
            "required": ["cloudformation_stack", "deploy"]
        }
    },
    "required": ["name", "type", "deploy", "stages", "regions", "migrations", "sfsp", "pipeline_metadata"]
}
run_sfsp_yaml_schema = {
    "type" : "object",
    "properties": {
        "name" : { "type" : "string" },
        "type" : { "type" : "string" },
        "deploy" : { "type" : "boolean" },
        "stages" : { "type" : "array" },
        "regions" : { "type" : "array" },
        "migrations" : { "type" : "boolean" },
        "sfsp" : { "type" : "boolean" },
        "pipeline_metadata": {
            "type": "object",
            "properties": {
                "deploy": {
                    "type": "object",
                    "properties": {
                        "run":{ "type": "string" },
                        "status": { "type": "boolean" },
                        "timestamp_after": { "type": "string" }
                    },
                    "required": ["status", "timestamp_after"]
                }
            },
            "required": ["deploy"]
        }
    },
    "required": ["name", "type", "deploy", "stages", "regions", "migrations", "sfsp", "pipeline_metadata"]
}

migrations_up_service_yaml_schema = {
    "type" : "object",
    "properties": {
        "name" : { "type" : "string" },
        "type" : { "type" : "string" },
        "deploy" : { "type" : "boolean" },
        "stages" : { "type" : "array" },
        "regions" : { "type" : "array" },
        "migrations" : { "type" : "boolean" },
        "sfsp" : { "type" : "boolean" },
        "pipeline_metadata": {
            "type": "object",
            "properties": {
                "deploy": {
                    "type": "object",
                    "properties": {
                        "run":{ "type": "string" },
                        "status": { "type": "boolean" },
                        "timestamp_after": { "type": "string" }
                    },
                    "required": ["status", "timestamp_after"]
                }
            },
            "required": ["deploy"]
        }
    },
    "required": ["name", "type", "deploy", "stages", "regions", "migrations", "sfsp", "pipeline_metadata"]
}
migrations_down_service_yaml_schema = {
    "type" : "object",
    "properties": {
        "name" : { "type" : "string" },
        "type" : { "type" : "string" },
        "deploy" : { "type" : "boolean" },
        "stages" : { "type" : "array" },
        "regions" : { "type" : "array" },
        "migrations" : { "type" : "boolean" },
        "sfsp" : { "type" : "boolean" },
        "pipeline_metadata": {
            "type": "object",
            "properties": {
                "deploy": {
                    "type": "object",
                    "properties": {
                        "run":{ "type": "string" },
                        "status": { "type": "boolean" },
                        "timestamp_after": { "type": "string" }
                    },
                    "required": ["status", "timestamp_after"]
                },
                "migrations": {
                    "type": "object",
                    "properties": {
                        "up":{
                            "type": "object",
                            "properties": {
                                "run":{ "type": "string" },
                                "status": { "type": "boolean" },
                            },
                            "required": ["status"]
                        },
                    },
                    "required": ["up"]
                }
            },
            "required": ["deploy", "migrations"]
        }
    },
    "required": [
        "name", "type", "deploy", "stages", "regions", "migrations", "sfsp", "pipeline_metadata"]
}

##############################################
# Setup
##############################################

logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.INFO)

if aws_profile or (aws_access_key_id and aws_secret_access_key):
    cloudformation_client = boto3.client('cloudformation')
    s3_client = boto3.client('s3')
    cloudfront_client = boto3.client('cloudfront')
else:
    logging.error(f'AWS Credentials are not configured in the environment...')
    logging.error(f'AWS_PROFILE, or AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY env variables are not set')
    sys.exit(1)

##############################################
# Helper Functions
##############################################

def read_file(file):
    with open(file, 'r') as f:
        try:
            return yaml.full_load(f)
        except yaml.YAMLError as exception:
            raise exception

def write_traits_to_file(content, file):
    with open(file, 'w') as f:
        try:
            yaml.dump(content, f, default_flow_style=False)
        except yaml.YAMLError as exception:
            raise exception

def validate_yaml(content, validation_schema):
    validationErrors = []

    v = jsonschema.Draft4Validator(validation_schema)
    for error in v.iter_errors(content):
        validationErrors.append(error)

    if validationErrors:
        logging.error('Failed schema validation for the apps\'s yaml file provided...')
        for error in validationErrors:
            print(error.message)
        #print(f'Required schema: {yaml.dump(service_yaml_schema)}')
        print(f'Required schema: {validation_schema}')
        sys.exit(1)

def load_traits_from_file(file='traits.yml', validation_schema=default_service_yaml_schema):
    content = read_file(file)
    validate_yaml(content, validation_schema)
    return content

def run_bash(command: str):
    logging.info(f'Running command: {command}')
    subprocess.run(command, shell=True, check=True)

def dump_yaml_content(data):
    for key, value in data.items():
        print(key,':',value)

def cloudformation_get_deployment_bucket(stack):
    try:
        return cloudformation_client.describe_stack_resource(
            StackName=stack,
            LogicalResourceId='ServerlessDeploymentBucket'
        )["StackResourceDetail"]["PhysicalResourceId"]
    except ClientError as e:
        logging.warning("CloudFormation stack was not found or the stack has not been deployed yet")
        logging.warning("Describe stack resource response: %s" % e)
        return None

def get_sls_timestamps(stack, app_name, stage):
    s3_bucket = cloudformation_get_deployment_bucket(stack)
    if not s3_bucket:
        return []

    folders = s3_client.list_objects(Bucket=s3_bucket, Prefix=f'serverless/{app_name}/{stage}/', Delimiter='/')
    if not folders.get('CommonPrefixes'):
        logging.warning(f'Deployment bucket exists, but no timestamps were found for app ({app_name})')
        return []
    else:
        timestamps = []
        for folder in folders.get('CommonPrefixes'):
            timestamps.append(folder.get('Prefix').split('/')[-2].split('-')[0])
        timestamps.sort(reverse=True)
        return timestamps

def sls_deploy(stage, region, args, chdir_path):
    cwd = os.getcwd()
    os.chdir(chdir_path)
    command=f'sls deploy --stage {stage} --region {region} {args}'
    run_bash(command)
    os.chdir(cwd)

def sls_rollback(stage, region, chdir_path, timestamp):
    cwd = os.getcwd()
    os.chdir(chdir_path)
    command=f'sls rollback --timestamp {timestamp} --stage {stage} --region {region}'
    run_bash(command)
    os.chdir(cwd)

def sls_migrate(stage, region, chdir_path, function, data):
    cwd = os.getcwd()
    os.chdir(chdir_path)
    command=f'sls invoke --stage {stage} --region {region} --function {function} --data {data}'
    run_bash(command)
    os.chdir(cwd)

def sls_sfsp(stage, region, chdir_path):
    cwd = os.getcwd()
    os.chdir(chdir_path)
    command=f'sls sfsp --stage={stage} --region={region}'
    run_bash(command)
    os.chdir(cwd)

def populate_git_traits(app, branch, commit, version, author):
    app["branch"] = branch if branch else git_branch
    app["commit"] = commit if commit else git_commit
    app["author"] = author if author else git_author
    app["version"] = version if version else ''
    return app

def cloudfront_distribution_exists(distribution_id):
    try:
        distributions = cloudfront_client.list_distributions()
        if distributions['DistributionList']['Quantity']:
            for distribution in distributions['DistributionList']['Items']:
                if distribution_id == distribution['Id']:
                    return True
        logging.warning(f'Cloudfront Distribution ({distribution_id}) not found!')
        return False

    except ClientError as e:
        logging.warning("Cloudfront Client error: %s" % e)
        return False

def create_invalidation(distribution_id, paths):
    if cloudfront_distribution_exists(distribution_id):
        try:
            response = cloudfront_client.create_invalidation(
                DistributionId=distribution_id,
                InvalidationBatch={
                    'Paths': {
                        'Quantity': len(paths),
                        'Items': paths,
                    },
                    'CallerReference': str(time()).replace(".", "")
                }
            )
            invalidation_id = response['Invalidation']['Id']
            logging.info(f'Cache Invalidation created successfully with ID: {invalidation_id}')
            return True
        except ClientError as e:
            logging.warning("Cloudfront Client error: %s" % e)
            return False

def get_ui_versions(s3_bucket):
    if not s3_bucket_exists_and_not_empty(s3_bucket):
        logging.warning(f'"versions" folder in bucket ({s3_bucket}) was not found or it is empty.')
        return []

    paginator = s3_client.get_paginator('list_objects')
    pages = paginator.paginate(Bucket=s3_bucket, Prefix='versions/', Delimiter='/')
    if not pages:
        logging.warning(f'S3 Bucket ({s3_bucket}) was not found or it is empty.')
        return []

    try:
        versions = []
        for page in pages:
            for folder in page['CommonPrefixes']:
                version = folder["Prefix"].split('/')[1]
                if '-' in version:
                    versions.append(version)
        versions.sort(reverse=True)
        return versions
    except:
        logging.warning(f'versions folder in bucket ({s3_bucket}) is not empty but folders are badly formated.')
        return []

def s3_bucket_exists_and_not_empty(s3_bucket) -> bool:
    logging.info(f'Checking if s3 bucket ({s3_bucket}) exists...')
    try:
        resp = s3_client.list_objects(Bucket=s3_bucket, Prefix='versions/', MaxKeys=1)
        return 'Contents' in resp
    except ClientError as e:
        logging.error("S3 Client error: %s" % e)
        sys.exit(1)

def s3_cp(source, target, args=''):
    command=f'aws s3 cp {source} {target} {args}'
    run_bash(command)

def s3_sync(source, target, args=''):
    command=f'aws s3 sync {source} {target} {args}'
    run_bash(command)

def s3_rm_version(s3_bucket, target, args=''):
    command=f'aws s3 rm s3://{s3_bucket}/versions/{target} --recursive {args}'
    run_bash(command)


## Check functions
def check_app_type(app, type):
    if app["type"] != type or app["type"] not in allowed_app_types:
        logging.warning(f'Skipping {type} ({app["name"]}) deployment...')
        logging.warning(f'App type is not ({type}) or not supported! Type passed from traits: {app["type"]}')
        sys.exit(0)

def check_app_stage_region(app, stage, region=None):
    if stage not in app["stages"]:
        logging.warning(f'Skipping {app["type"]} ({app["name"]}) deployment...')
        logging.warning(f'Stage ({stage}) is not supported for {app["type"]} ({app["name"]}). Allowed stages: {app["stages"]}')
        sys.exit(0)

    if not region:
        pass
    elif region not in app["regions"]:
        logging.warning(f'Skipping {app["type"]} ({app["name"]}) deployment...')
        logging.warning(f'Region ({region}) is not supported for {app["type"]} ({app["name"]}). Allowed regions: {app["regions"]}')
        sys.exit(0)

    pass

# UI
def run_deploy_ui_checks(app, stage):
    check_app_type(app, 'ui')
    check_app_stage_region(app, stage)

    if not app["deploy"]:
        logging.info(f'Skipping {app["type"]} ({app["name"]}) deployment...')
        logging.info(f'"deploy" parameter is set to False in traits file.')
        sys.exit(0)

    pass

def run_rollback_ui_checks(app, stage):
    check_app_type(app, 'ui')
    check_app_stage_region(app, stage)

    if app["pipeline_metadata"]["deploy"]["status"] == False:
        logging.info(f'Skipping {app["type"]} ({app["name"]}) rollback...')
        logging.info(f'Deploy status is "False" in {app["type"]} ({app["name"]}) traits')
        sys.exit(0)

    if app["pipeline_metadata"]["rollback"]["version"] == '':
        logging.info(f'Skipping {app["type"]} ({app["name"]}) rollback...')
        logging.info(f'Rollback version for ({app["name"]}) is empty')
        logging.warning(f'UI ({app["name"]}) was deployed for the first time, not rolling back!')
        sys.exit(0)

    pass

# Infra
def run_deploy_infra_checks(app, stage, region):
    check_app_type(app, 'infra')
    check_app_stage_region(app, stage, region)

    if not app["deploy"]:
        logging.info(f'Skipping {app["type"]} ({app["name"]}) deployment...')
        logging.info(f'"deploy" parameter is set to False in traits file.')
        sys.exit(0)

    pass

def run_rollback_infra_checks(app, stage, region):
    check_app_type(app, 'infra')
    check_app_stage_region(app, stage, region)

    if app["pipeline_metadata"]["deploy"]["status"] == False:
        logging.info(f'Skipping {app["type"]} ({app["name"]}) rollback...')
        logging.info(f'Deploy status is "False" in {app["type"]} ({app["name"]}) traits')
        sys.exit(0)

    if app["pipeline_metadata"]["rollback"]["timestamp"] == '':
        logging.info(f'Skipping {app["type"]} ({app["name"]}) rollback...')
        logging.info(f'Rollback timestamp for ({app["name"]}) is empty')
        logging.warning(f'Infra ({app["name"]}) was deployed for the first time, not rolling back!')
        sys.exit(0)

    pass

# Service
def run_deploy_service_checks(app, stage, region):
    check_app_type(app, 'service')
    check_app_stage_region(app, stage, region)

    if not app["deploy"]:
        logging.info(f'Skipping {app["type"]} ({app["name"]}) deployment...')
        logging.info(f'Deploy is not enabled for this {app["type"]} in traits')
        sys.exit(0)

    pass

def run_sfsp_checks(app, stage, region):
    check_app_type(app, 'service')
    check_app_stage_region(app, stage, region)

    if app["sfsp"] == False:
        logging.info(f'Skipping {app["type"]} ({app["name"]}) sfsp run...')
        logging.info(f'Service ({app["name"]}) has no "sfsp"')
        sys.exit(0)

    if app["pipeline_metadata"]["deploy"]["status"] == False:
        logging.info(f'Skipping {app["type"]} ({app["name"]}) sfsp run...')
        logging.info(f'Deploy status is "False" in {app["type"]} ({app["name"]}) traits')
        sys.exit(0)

    if app["pipeline_metadata"]["deploy"]["timestamp_after"] == '':
        logging.info(f'Skipping {app["type"]} ({app["name"]}) sfsp run...')
        logging.info(f'After deploy timestamp is empty in {app["type"]} ({app["name"]}) traits')
        sys.exit(0)

    pass

def run_rollback_service_checks(app, stage, region):
    check_app_type(app, 'service')
    check_app_stage_region(app, stage, region)
    #timestamp = str(timestamp) if timestamp else app["pipeline_metadata"]["deploy"]["timestamp_last"]

    if app["pipeline_metadata"]["deploy"]["status"] == False:
        logging.info(f'Skipping {app["type"]} ({app["name"]}) rollback...')
        logging.info(f'Deploy status is "False" in {app["type"]} ({app["name"]}) traits')
        sys.exit(0)

    if app["pipeline_metadata"]["rollback"]["timestamp"] == '':
        logging.info(f'Skipping {app["type"]} ({app["name"]}) rollback...')
        logging.info(f'Rollback timestamp for ({app["name"]}) is empty')
        logging.warning(f'Service ({app["name"]}) was deployed for the first time, not rolling back!')
        sys.exit(0)

    pass

def run_migrations_up_service_checks(app, stage, region):
    check_app_type(app, 'service')
    check_app_stage_region(app, stage, region)

    # Check if app has migrations
    if app["migrations"] == False:
        logging.info(f'Skipping {app["type"]} ({app["name"]}) migrations up...')
        logging.info(f'{app["type"]} ({app["name"]}) has no migrations')
        sys.exit(0)

    # Check if deploy_status is True
    if app["pipeline_metadata"]["deploy"]["status"] == False:
        logging.info(f'Skipping {app["type"]} ({app["name"]}) migrations up...')
        logging.info(f'Deploy status is "False" in {app["type"]} ({app["name"]}) traits')
        sys.exit(0)

    if app["pipeline_metadata"]["deploy"]["timestamp_after"] == '':
        logging.info(f'Skipping {app["type"]} ({app["name"]}) sfsp run...')
        logging.info(f'After deploy timestamp is empty in {app["type"]} ({app["name"]}) traits')
        sys.exit(0)

    pass

def run_migrations_down_service_checks(app, stage, region):
    check_app_type(app, 'service')
    check_app_stage_region(app, stage, region)

    # Check if service has migrations and if they were run
    if app["migrations"] == False:
        logging.info(f'Skipping {app["type"]} ({app["name"]}) migrations down...')
        logging.info(f'{app["type"]} ({app["name"]}) has no migrations')
        sys.exit(0)

    # Check if deploy_status is True
    if app["pipeline_metadata"]["deploy"]["status"] == False:
        logging.info(f'Skipping {app["type"]} ({app["name"]}) migrations down...')
        logging.info(f'Deploy status is "False" in {app["type"]} ({app["name"]}) traits')
        sys.exit(0)

    if app["pipeline_metadata"]["deploy"]["timestamp_after"] == '':
        logging.info(f'Skipping {app["type"]} ({app["name"]}) sfsp run...')
        logging.info(f'After deploy timestamp is empty in {app["type"]} ({app["name"]}) traits')
        sys.exit(0)

    # ... and service migrations_up_status is True
    if app["pipeline_metadata"]["migrations"]["up"]["status"] == False:
        logging.info(f'Skipping service ({app["name"]}) migrations down...')
        logging.info(f'{app["type"]} ({app["name"]}) migrations up was run but failed')
        sys.exit(0)

    pass



##############################################
# Commands
##############################################

@click.group(chain=True)
@click.version_option()
def cli():
    pass

@cli.command("deploy-infra")
@click.option('-r', '--region', required=True, type=str, help='Deployment region')
@click.option('-s', '--stage', required=True, type=str, help='Deployment stage')
@click.option('--args', type=str, default='', help='Additional sls arguments passed to the sls deploy command')
@click.option('--app-dir', type=click.Path(exists=True, file_okay=False), default='.', help='App directory where to run sls deploy')
@click.option('--branch', type=str, default=None, help='Git branch')
@click.option('--commit', type=str, default=None, help='Git commit')
@click.option('--version', type=str, default=None, help='Version')
@click.option('--author', type=str, default=None, help='Git commit author')
@click.option('--traits-input-file', type=click.Path(exists=True, file_okay=True, dir_okay=False, writable=True), default='traits.yml', help='Load traits file. Default (traits.yml)')
@click.option('--traits-output-file', type=click.Path(exists=True, file_okay=True, dir_okay=False, writable=True), default='traits.yml', help='Updated traits file. Default (traits.yml)')
def deploy_infra_cmd(stage, region, args, app_dir, branch, commit, version, author, traits_input_file, traits_output_file):
    app = load_traits_from_file(traits_input_file, default_infra_yaml_schema)

    app = populate_git_traits(app, branch, commit, version, author)
    app["pipeline_metadata"] = {}
    app["pipeline_metadata"]["nx_app_name"] = app["type"] + "-" + app["name"]
    app["pipeline_metadata"]["cloudformation_stack"] = app["name"] + "-" + stage
    app["pipeline_metadata"]["deploy"] = {}
    app["pipeline_metadata"]["deploy"]["run"] = ''
    app["pipeline_metadata"]["deploy"]["status"] = False
    app["pipeline_metadata"]["deploy"]["timestamp_last"] = ''
    app["pipeline_metadata"]["deploy"]["timestamp_after"] = ''
    write_traits_to_file(app, traits_output_file)

    run_deploy_infra_checks(app, stage, region)

    timestamps = get_sls_timestamps(app["pipeline_metadata"]["cloudformation_stack"], app["name"], stage)
    if timestamps:
        logging.info(f'Last deployment timestamp: {timestamps[0]} - {datetime.fromtimestamp(int(timestamps[0])/1000, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")}')
        app["pipeline_metadata"]["deploy"]["timestamp_last"] = timestamps[0]
        write_traits_to_file(app, traits_output_file)

    app["pipeline_metadata"]["deploy"]["run"] = str(datetime.now(timezone.utc).replace(tzinfo=timezone.utc))
    write_traits_to_file(app, traits_output_file)
    logging.info(f'Deploying infra ({app["name"]}) on ({stage}) in ({region})...')

    sls_deploy(stage, region, args, app_dir)

    app["pipeline_metadata"]["deploy"]["status"] = True
    write_traits_to_file(app, traits_output_file)

    timestamps = get_sls_timestamps(app["pipeline_metadata"]["cloudformation_stack"], app["name"], stage)
    if timestamps:
        logging.info(f'New deployment timestamp: {timestamps[0]} - {datetime.fromtimestamp(int(timestamps[0])/1000, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")}')
        app["pipeline_metadata"]["deploy"]["timestamp_after"] = timestamps[0]
        write_traits_to_file(app, traits_output_file)

@cli.command("rollback-infra")
@click.option('-r', '--region', required=True, type=str, help='Deployment region')
@click.option('-s', '--stage', required=True, type=str, help='Deployment stage')
@click.option('-t', '--timestamp', type=str, default=None, help='Serverless timestamp')
@click.option('--app-dir', type=click.Path(exists=True, file_okay=False), default='.', help='App directory where to run sls rollback')
@click.option('--traits-input-file', type=click.Path(exists=True, file_okay=True, dir_okay=False, writable=True), default='traits.yml', help='Load traits file. Default (traits.yml)')
@click.option('--traits-output-file', type=click.Path(exists=True, file_okay=True, dir_okay=False, writable=True), default='traits.yml', help='Updated traits file. Default (traits.yml)')
def rollback_infra_cmd(stage, region, timestamp, app_dir, traits_input_file, traits_output_file):
    app = load_traits_from_file(traits_input_file, rollback_infra_yaml_schema)

    app["pipeline_metadata"]["rollback"] = {}
    app["pipeline_metadata"]["rollback"]["status"] = False
    app["pipeline_metadata"]["rollback"]["timestamp"] = str(timestamp) if timestamp else app["pipeline_metadata"]["deploy"]["timestamp_last"]
    app["pipeline_metadata"]["rollback"]["timestamp_after"] = ''
    write_traits_to_file(app, traits_output_file)

    run_rollback_infra_checks(app, stage, region)

    app["pipeline_metadata"]["rollback"]["run"] = str(datetime.now(timezone.utc).replace(tzinfo=timezone.utc))
    write_traits_to_file(app, traits_output_file)
    logging.info(f'Rolling back infra ({app["name"]}) to timestamp ({app["pipeline_metadata"]["rollback"]["timestamp"]})...')

    sls_rollback(stage, region, app_dir, app["pipeline_metadata"]["rollback"]["timestamp"])

    app["pipeline_metadata"]["rollback"]["status"] = True
    write_traits_to_file(app, traits_output_file)

    timestamps = get_sls_timestamps(app["pipeline_metadata"]["cloudformation_stack"], app["name"], stage)
    if timestamps:
        logging.info(f'Rollback deployment timestamp: {timestamps[0]} - {datetime.fromtimestamp(int(timestamps[0])/1000, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")}')
        app["pipeline_metadata"]["rollback"]["timestamp_after"] = timestamps[0]
        write_traits_to_file(app, traits_output_file)


@cli.command("deploy-service")
@click.option('-r', '--region', required=True, type=str, help='Deployment region')
@click.option('-s', '--stage', required=True, type=str, help='Deployment stage')
@click.option('--args', type=str, default='', help='Additional sls arguments passed to the sls deploy command')
@click.option('--app-dir', type=click.Path(exists=True, file_okay=False), default='.', help='App directory where to run sls deploy')
@click.option('--branch', type=str, default=None, help='Git branch')
@click.option('--commit', type=str, default=None, help='Git commit')
@click.option('--version', type=str, default=None, help='Version')
@click.option('--author', type=str, default=None, help='Git commit author')
@click.option('--traits-input-file', type=click.Path(exists=True, file_okay=True, dir_okay=False, writable=True), default='traits.yml', help='Load traits file. Default (traits.yml)')
@click.option('--traits-output-file', type=click.Path(exists=True, file_okay=True, dir_okay=False, writable=True), default='traits.yml', help='Updated traits file. Default (traits.yml)')
def deploy_service_cmd(stage, region, args, app_dir, branch, commit, version, author, traits_input_file, traits_output_file):
    app = load_traits_from_file(traits_input_file, default_service_yaml_schema)

    app = populate_git_traits(app, branch, commit, version, author)
    app["pipeline_metadata"] = {}
    app["pipeline_metadata"]["nx_app_name"] = app["type"] + "-" + app["name"]
    app["pipeline_metadata"]["cloudformation_stack"] = app["name"] + "-" + stage
    app["pipeline_metadata"]["deploy"] = {}
    app["pipeline_metadata"]["deploy"]["run"] = ''
    app["pipeline_metadata"]["deploy"]["status"] = False
    app["pipeline_metadata"]["deploy"]["timestamp_last"] = ''
    app["pipeline_metadata"]["deploy"]["timestamp_after"] = ''
    write_traits_to_file(app, traits_output_file)

    run_deploy_service_checks(app, stage, region)

    timestamps = get_sls_timestamps(app["pipeline_metadata"]["cloudformation_stack"], app["name"], stage)
    if timestamps:
        logging.info(f'Last deployment timestamp: {timestamps[0]} - {datetime.fromtimestamp(int(timestamps[0])/1000, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")}')
        app["pipeline_metadata"]["deploy"]["timestamp_last"] = timestamps[0]
        write_traits_to_file(app, traits_output_file)

    app["pipeline_metadata"]["deploy"]["run"] = str(datetime.now(timezone.utc).replace(tzinfo=timezone.utc))
    write_traits_to_file(app, traits_output_file)
    logging.info(f'Deploying service ({app["name"]}) on ({stage}) in ({region})...')

    sls_deploy(stage, region, args, app_dir)

    app["pipeline_metadata"]["deploy"]["status"] = True
    write_traits_to_file(app, traits_output_file)

    timestamps = get_sls_timestamps(app["pipeline_metadata"]["cloudformation_stack"], app["name"], stage)
    if timestamps:
        logging.info(f'New deployment timestamp: {timestamps[0]} - {datetime.fromtimestamp(int(timestamps[0])/1000, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")}')
        app["pipeline_metadata"]["deploy"]["timestamp_after"] = timestamps[0]
        write_traits_to_file(app, traits_output_file)


@cli.command("rollback-service")
@click.option('-r', '--region', required=True, type=str, help='Deployment region')
@click.option('-s', '--stage', required=True, type=str, help='Deployment stage')
@click.option('-t', '--timestamp', type=str, default=None, help='Serverless timestamp')
@click.option('--app-dir', type=click.Path(exists=True, file_okay=False), default='.', help='App directory where to run sls rollback')
@click.option('--traits-input-file', type=click.Path(exists=True, file_okay=True, dir_okay=False, writable=True), default='traits.yml', help='Load traits file. Default (traits.yml)')
@click.option('--traits-output-file', type=click.Path(exists=True, file_okay=True, dir_okay=False, writable=True), default='traits.yml', help='Updated traits file. Default (traits.yml)')
def rollback_service_cmd(stage, region, timestamp, app_dir, traits_input_file, traits_output_file):
    app = load_traits_from_file(traits_input_file, rollback_service_yaml_schema)

    app["pipeline_metadata"]["rollback"] = {}
    app["pipeline_metadata"]["rollback"]["status"] = False
    app["pipeline_metadata"]["rollback"]["timestamp"] = str(timestamp) if timestamp else app["pipeline_metadata"]["deploy"]["timestamp_last"]
    app["pipeline_metadata"]["rollback"]["timestamp_after"] = ''
    write_traits_to_file(app, traits_output_file)

    run_rollback_service_checks(app, stage, region)

    app["pipeline_metadata"]["rollback"]["run"] = str(datetime.now(timezone.utc).replace(tzinfo=timezone.utc))
    write_traits_to_file(app, traits_output_file)
    logging.info(f'Rolling back service ({app["name"]}) to timestamp ({app["pipeline_metadata"]["rollback"]["timestamp"]})...')

    sls_rollback(stage, region, app_dir, app["pipeline_metadata"]["rollback"]["timestamp"])

    app["pipeline_metadata"]["rollback"]["status"] = True
    write_traits_to_file(app, traits_output_file)

    timestamps = get_sls_timestamps(app["pipeline_metadata"]["cloudformation_stack"], app["name"], stage)
    if timestamps:
        logging.info(f'Rollback deployment timestamp: {timestamps[0]} - {datetime.fromtimestamp(int(timestamps[0])/1000, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")}')
        app["pipeline_metadata"]["rollback"]["timestamp_after"] = timestamps[0]
        write_traits_to_file(app, traits_output_file)


@cli.command("run-sfsp")
@click.option('-r', '--region', required=True, type=str, help='Deployment region')
@click.option('-s', '--stage', required=True, type=str, help='Deployment stage')
@click.option('--app-dir', type=click.Path(exists=True, file_okay=False), default='.', help='App directory where to run sls rollback')
@click.option('--traits-input-file', type=click.Path(exists=True, file_okay=True, dir_okay=False, writable=True), default='traits.yml', help='Load traits file. Default (traits.yml)')
@click.option('--traits-output-file', type=click.Path(exists=True, file_okay=True, dir_okay=False, writable=True), default='traits.yml', help='Updated traits file. Default (traits.yml)')
def run_sfsp_cmd(stage, region, app_dir, traits_input_file, traits_output_file):
    app = load_traits_from_file(traits_input_file, run_sfsp_yaml_schema)

    app["pipeline_metadata"]["sfsp"] = {}
    app["pipeline_metadata"]["sfsp"]["run"] = ''
    app["pipeline_metadata"]["sfsp"]["status"] = False
    write_traits_to_file(app, traits_output_file)

    run_sfsp_checks(app, stage, region)

    logging.info(f'Running sfsp for service ({app["name"]})...')
    app["pipeline_metadata"]["sfsp"]["run"] = str(datetime.now(timezone.utc).replace(tzinfo=timezone.utc))
    write_traits_to_file(app, traits_output_file)

    sls_sfsp(stage, region, app_dir)

    app["pipeline_metadata"]["sfsp"]["status"] = True
    write_traits_to_file(app, traits_output_file)


@cli.command("migrations-up-service")
@click.option('-r', '--region', required=True, type=str, help='Deployment region')
@click.option('-s', '--stage', required=True, type=str, help='Deployment stage')
@click.option('-d', '--data', type=str, default='{}', help='Migration data param passed to "up" function')
@click.option('--app-dir', type=click.Path(exists=True, file_okay=False), default='.', help='App directory where to run sls rollback')
@click.option('--traits-input-file', type=click.Path(exists=True, file_okay=True, dir_okay=False, writable=True), default='traits.yml', help='Load traits file. Default (traits.yml)')
@click.option('--traits-output-file', type=click.Path(exists=True, file_okay=True, dir_okay=False, writable=True), default='traits.yml', help='Updated traits file. Default (traits.yml)')
def migrations_up_service_cmd(stage, region, data, app_dir, traits_input_file, traits_output_file):
    app = load_traits_from_file(traits_input_file, migrations_up_service_yaml_schema)

    app["pipeline_metadata"]["migrations"] = {}
    app["pipeline_metadata"]["migrations"]["up"] = {}
    app["pipeline_metadata"]["migrations"]["up"]["run"] = ''
    app["pipeline_metadata"]["migrations"]["up"]["status"] = False
    write_traits_to_file(app, traits_output_file)

    run_migrations_up_service_checks(app, stage, region)

    logging.info(f'Running migrations UP for service ({app["name"]})...')
    app["pipeline_metadata"]["migrations"]["up"]["run"] = str(datetime.now(timezone.utc).replace(tzinfo=timezone.utc))
    write_traits_to_file(app, traits_output_file)

    sls_migrate(stage, region, app_dir, "up", data)

    app["pipeline_metadata"]["migrations"]["up"]["status"] = True
    write_traits_to_file(app, traits_output_file)


@cli.command("migrations-down-service")
@click.option('-r', '--region', required=True, type=str, help='Deployment region')
@click.option('-s', '--stage', required=True, type=str, help='Deployment stage')
@click.option('-d', '--data', type=str, default='{}', help='Migration data param passed to "up" function')
@click.option('--app-dir', type=click.Path(exists=True, file_okay=False), default='.', help='App directory where to run sls rollback')
@click.option('--traits-input-file', type=click.Path(exists=True, file_okay=True, dir_okay=False, writable=True), default='traits.yml', help='Load traits file. Default (traits.yml)')
@click.option('--traits-output-file', type=click.Path(exists=True, file_okay=True, dir_okay=False, writable=True), default='traits.yml', help='Updated traits file. Default (traits.yml)')
def migrations_down_service_cmd(stage, region, data, app_dir, traits_input_file, traits_output_file):
    app = load_traits_from_file(traits_input_file, migrations_down_service_yaml_schema)

    app["pipeline_metadata"]["migrations"]["down"] = {}
    app["pipeline_metadata"]["migrations"]["down"]["run"] = ''
    app["pipeline_metadata"]["migrations"]["down"]["status"] = False
    write_traits_to_file(app, traits_output_file)

    run_migrations_down_service_checks(app, stage, region)

    logging.info(f'Running migrations DOWN for service ({app["name"]})...')
    app["pipeline_metadata"]["migrations"]["down"]["run"] = str(datetime.now(timezone.utc).replace(tzinfo=timezone.utc))
    write_traits_to_file(app, traits_output_file)

    sls_migrate(stage, region, app_dir, "down", data)

    app["pipeline_metadata"]["migrations"]["down"]["status"] = True
    write_traits_to_file(app, traits_output_file)


@cli.command("deploy-ui")
@click.option('-s', '--stage', required=True, type=str, help='Deployment stage')
@click.option('--s3-bucket', type=str, required=True, help='S3 Bucket to deploy static files')
@click.option('--version', type=str, required=True, help='Version')
@click.option('--distribution-id', type=str, default=None, help='Distribution ID of the Cloudfront serving static files from s3 bucket.\nIf provided, will trigger cache invalidation.')
@click.option('--invalidate-paths', type=str, default='/*', help='The space-separated paths to be invalidated in Cloudfront Distribution.\nRequires --distribution-id.\nDefault: "/*"')
@click.option('--args', type=str, default='', help='Additional aws cli arguments passed to the aws s3 sync command')
@click.option('--build-dir', type=click.Path(exists=True, file_okay=False), default='.', help='Directory containing the built static files to deploy in s3.')
@click.option('--branch', type=str, default=None, help='Git branch')
@click.option('--commit', type=str, default=None, help='Git commit')
@click.option('--author', type=str, default=None, help='Git commit author')
@click.option('--traits-input-file', type=click.Path(exists=True, file_okay=True, dir_okay=False, writable=True), default='traits.yml', help='Load traits file. Default (traits.yml)')
@click.option('--traits-output-file', type=click.Path(exists=True, file_okay=True, dir_okay=False, writable=True), default='traits.yml', help='Updated traits file. Default (traits.yml)')
def deploy_ui_cmd(stage, s3_bucket, version, distribution_id, invalidate_paths, args, build_dir, branch, commit, author, traits_input_file, traits_output_file):
    app = load_traits_from_file(traits_input_file, default_ui_yaml_schema)
    invalidate_paths = invalidate_paths.split(' ')

    timestamp = str(int(datetime.now(timezone.utc).replace(tzinfo=timezone.utc).timestamp() * 1000))

    app = populate_git_traits(app, branch, commit, version, author)
    app["pipeline_metadata"] = {}
    app["pipeline_metadata"]["deploy"] = {}
    app["pipeline_metadata"]["nx_app_name"] = app["type"] + "-" + app["name"]
    app["pipeline_metadata"]["deploy"]["run"] = ''
    app["pipeline_metadata"]["deploy"]["status"] = False
    app["pipeline_metadata"]["deploy"]["s3_bucket"] = s3_bucket
    app["pipeline_metadata"]["deploy"]["version"] = version
    app["pipeline_metadata"]["deploy"]["version_folder"] = timestamp + '-' + version
    app["pipeline_metadata"]["deploy"]["last_version"] = ''
    app["pipeline_metadata"]["deploy"]["last_version_folder"] = ''
    app["pipeline_metadata"]["deploy"]["second_last_version"] = ''
    app["pipeline_metadata"]["deploy"]["second_last_version_folder"] = ''
    app["pipeline_metadata"]["deploy"]["invalidate_cache"] = True if distribution_id else False
    if distribution_id:
        app["pipeline_metadata"]["deploy"]["distribution_id"] = distribution_id
        app["pipeline_metadata"]["deploy"]["invalidate_paths"] = invalidate_paths
        app["pipeline_metadata"]["deploy"]["invalidate_status"] = False
    write_traits_to_file(app, traits_output_file)

    run_deploy_ui_checks(app, stage)

    app["pipeline_metadata"]["deploy"]["run"] = str(datetime.now(timezone.utc).replace(tzinfo=timezone.utc))
    write_traits_to_file(app, traits_output_file)

    logging.info(f'Deploying ui ({app["name"]}) in ({stage})...')

    # Get last version
    last_versions=get_ui_versions(s3_bucket)
    if last_versions and len(last_versions) > 1:
        app["pipeline_metadata"]["deploy"]["last_version_folder"] = last_versions[0]
        app["pipeline_metadata"]["deploy"]["last_version"] = last_versions[0].split('-')[1]
        app["pipeline_metadata"]["deploy"]["second_last_version_folder"] = last_versions[1]
        app["pipeline_metadata"]["deploy"]["second_last_version"] = last_versions[1].split('-')[1]
        write_traits_to_file(app, traits_output_file)
    elif last_versions and len(last_versions) == 1:
        app["pipeline_metadata"]["deploy"]["last_version_folder"] = last_versions[0]
        app["pipeline_metadata"]["deploy"]["last_version"] = last_versions[0].split('-')[1]
        write_traits_to_file(app, traits_output_file)

    #Sync . to s3 (version)
    s3_sync(build_dir, f's3://{s3_bucket}/versions/{timestamp}-{version}', '--delete')

    # Backup current live to previous
    s3_sync(f's3://{s3_bucket}/live', f's3://{s3_bucket}/previous', '--delete')

    #Sync . to s3 live
    s3_sync(build_dir, f's3://{s3_bucket}/live', f'--exclude "{traits_output_file}" --delete')

    app["pipeline_metadata"]["deploy"]["status"] = True
    write_traits_to_file(app, traits_output_file)

    if app["pipeline_metadata"]["deploy"]["invalidate_cache"]:
        logging.info(f'Invalidating cache in distribution {distribution_id} on paths ({" ".join(invalidate_paths)})')
        app["pipeline_metadata"]["deploy"]["invalidate_status"] = create_invalidation(distribution_id, invalidate_paths)
        write_traits_to_file(app, traits_output_file)

    # Update the latest traits.yml file in s3
    s3_cp(f'{traits_output_file}', f's3://{s3_bucket}/versions/{timestamp}-{version}/{traits_output_file}')


@cli.command("rollback-ui")
@click.option('-s', '--stage', required=True, type=str, help='Deployment stage')
@click.option('--traits-input-file', type=click.Path(exists=True, file_okay=True, dir_okay=False, writable=True), default='traits.yml', help='Load traits file. Default (traits.yml)')
@click.option('--traits-output-file', type=click.Path(exists=True, file_okay=True, dir_okay=False, writable=True), default='traits.yml', help='Updated traits file. Default (traits.yml)')
def rollback_ui_cmd(stage, traits_input_file, traits_output_file):
    app = load_traits_from_file(traits_input_file, rollback_ui_yaml_schema)

    app["pipeline_metadata"]["rollback"] = {}
    app["pipeline_metadata"]["rollback"]["run"] = ''
    app["pipeline_metadata"]["rollback"]["status"] = False
    app["pipeline_metadata"]["rollback"]["version"] = app["pipeline_metadata"]["deploy"]["last_version"]
    app["pipeline_metadata"]["rollback"]["version_folder"] = app["pipeline_metadata"]["deploy"]["last_version_folder"]
    if app["pipeline_metadata"]["deploy"]["invalidate_cache"]:
        app["pipeline_metadata"]["rollback"]["invalidate_status"] = False
    write_traits_to_file(app, traits_output_file)

    run_rollback_ui_checks(app, stage)

    app["pipeline_metadata"]["rollback"]["run"] = str(datetime.now(timezone.utc).replace(tzinfo=timezone.utc))
    write_traits_to_file(app, traits_output_file)

    logging.info(f'Rolling back ui ({app["name"]}) to version ({app["pipeline_metadata"]["rollback"]["version"]})...')

    # Move second_last_version  or last_version to previous
    if app["pipeline_metadata"]["deploy"]["second_last_version_folder"] and app["pipeline_metadata"]["deploy"]["second_last_version"]:
        logging.info(f'Syncing second last ui ({app["name"]}) version ({app["pipeline_metadata"]["deploy"]["second_last_version"]}) into (previous)...')
        s3_cp(
            f's3://{app["pipeline_metadata"]["deploy"]["s3_bucket"]}/versions/{app["pipeline_metadata"]["deploy"]["second_last_version_folder"]}',
            f's3://{app["pipeline_metadata"]["deploy"]["s3_bucket"]}/previous',
            '--recursive'
        )
        s3_sync(
            f's3://{app["pipeline_metadata"]["deploy"]["s3_bucket"]}/versions/{app["pipeline_metadata"]["deploy"]["second_last_version_folder"]}',
            f's3://{app["pipeline_metadata"]["deploy"]["s3_bucket"]}/previous',
            '--delete'
        )
    else:
        logging.info(f'No second last version found for ui ({app["name"]})!')
        logging.info(f'Syncing last ui ({app["name"]}) version ({app["pipeline_metadata"]["deploy"]["last_version"]}) into (previous)...')
        s3_cp(
            f's3://{app["pipeline_metadata"]["deploy"]["s3_bucket"]}/versions/{app["pipeline_metadata"]["deploy"]["last_version_folder"]}',
            f's3://{app["pipeline_metadata"]["deploy"]["s3_bucket"]}/previous',
            '--recursive'
        )
        s3_sync(
            f's3://{app["pipeline_metadata"]["deploy"]["s3_bucket"]}/versions/{app["pipeline_metadata"]["deploy"]["last_version_folder"]}',
            f's3://{app["pipeline_metadata"]["deploy"]["s3_bucket"]}/previous',
            '--delete'
        )

    logging.info(f'Syncing last ui ({app["name"]}) version ({app["pipeline_metadata"]["deploy"]["last_version"]}) into (live)...')
    s3_cp(
        f's3://{app["pipeline_metadata"]["deploy"]["s3_bucket"]}/versions/{app["pipeline_metadata"]["deploy"]["last_version_folder"]}',
        f's3://{app["pipeline_metadata"]["deploy"]["s3_bucket"]}/live',
        f'--exclude "{traits_output_file}" --recursive'
    )
    s3_sync(
        f's3://{app["pipeline_metadata"]["deploy"]["s3_bucket"]}/versions/{app["pipeline_metadata"]["deploy"]["last_version_folder"]}',
        f's3://{app["pipeline_metadata"]["deploy"]["s3_bucket"]}/live',
        f'--exclude "{traits_output_file}" --delete'
    )

    # Remove deployed version
    logging.info(f'Removing ui ({app["name"]}) version ({app["pipeline_metadata"]["deploy"]["version"]}) from bucket ({app["pipeline_metadata"]["deploy"]["s3_bucket"]})...')
    s3_rm_version(app["pipeline_metadata"]["deploy"]["s3_bucket"], app["pipeline_metadata"]["deploy"]["version_folder"])


    app["pipeline_metadata"]["rollback"]["status"] = True
    write_traits_to_file(app, traits_output_file)

    if app["pipeline_metadata"]["deploy"]["invalidate_cache"]:
        logging.info(f'Invalidating cache in distribution {app["pipeline_metadata"]["deploy"]["distribution_id"]} on paths ({" ".join(app["pipeline_metadata"]["deploy"]["invalidate_paths"])})')
        app["pipeline_metadata"]["rollback"]["invalidate_status"] = create_invalidation(app["pipeline_metadata"]["deploy"]["distribution_id"], app["pipeline_metadata"]["deploy"]["invalidate_paths"])
        write_traits_to_file(app, traits_output_file)





if __name__ == "__main__":
    cli()
