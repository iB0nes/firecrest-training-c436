import firecrest as fc
import os
import time
import argparse
import utilities as util


# You can use this set to decide if the job has finished
final_slurm_states = {
    'BOOT_FAIL',
    'CANCELLED',
    'COMPLETED',
    'DEADLINE',
    'FAILED',
    'NODE_FAIL',
    'OUT_OF_MEMORY',
    'PREEMPTED',
    'TIMEOUT',
}

# If you are working on the CI-pipeline use case remove the line bellow:
#exit(0)

# Setup variables of the client as secrets,
# no need to change anything here
CLIENT_ID = os.environ.get("FIRECREST_CLIENT_ID")
CLIENT_SECRET = os.environ.get("FIRECREST_CLIENT_SECRET")
FIRECREST_URL = os.environ.get("FIRECREST_URL")
AUTH_TOKEN_URL = os.environ.get("AUTH_TOKEN_URL")
print("CLIENT ID: "+CLIENT_ID)
print("FIRECREST URL: "+FIRECREST_URL)
print("AUTH URL: "+AUTH_TOKEN_URL)
# Setup an argument parser for the script,
# no need to change anything here
parser = argparse.ArgumentParser()
parser.add_argument("--system", default=os.environ.get('MACHINE'), help="choose system to run")
parser.add_argument("--branch", default="main", help="branch to be tested")
parser.add_argument("--account", default="csstaff", help="branch to be tested")
parser.add_argument("--repo", help="repository to be tested")
args = parser.parse_args()
system_name = args.system
ref = args.branch
print(f"Will try to run the ci in system {system_name} on branch {ref}")

# Setup up a firecrest client
keycloak = fc.ClientCredentialsAuth(CLIENT_ID, CLIENT_SECRET, AUTH_TOKEN_URL)
client = fc.Firecrest(FIRECREST_URL, authorization=keycloak)

script_content = util.create_batch_script(repo=args.repo, constraint='gpu', num_nodes=2, account=args.account, custom_modules=['cray-python'], branch=ref)
with open("submission_script.sh", "w") as fp:
    fp.write(script_content)

print(client.whoami())

# Check the status of the system and print it in the console
system = client.service(system_name)
print("STATUS: "+str(system))
status = ""
# If the status is available submit and poll every 30 secs until
# it reaches a final state
if status == "available":
    pass

    # Print the filename of stdout and stderr in the console,
    # as well as their content


    # Add some sanity checks:
    # - Poll for the final result of the system and make sure it "COMPLETED"

    # Check the output with the util function that is provided
    # util.check_output(stdout_content)

else:
    print("System {system_name} is not available")
    exit(1)
