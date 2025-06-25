import os
import aws_cdk as cdk
from stateful_stack import StatefulStack
from stateless_stack import StatelessStack
from pathlib import Path
import sys

# 🟦 NOTE: Defensive check to ensure this file is executed from the correct working directory.
# 🟨 CAUTION: If CDK is run from a different directory, relative imports or file checks may fail.
# This block ensures the script always runs from the infrastructure/ directory.
expected_dir = Path(__file__).parent.resolve()
if Path.cwd().resolve() != expected_dir:
    print(
        f"🟨 CAUTION: Changing working directory to {expected_dir} for CDK app execution."
    )
    os.chdir(expected_dir)
    sys.path.insert(0, str(expected_dir))

app = cdk.App()

# Determine the environment from the CDK context variable 'env' (e.g., -c env=staging)
# Default to 'prod' if not specified.
env_name = app.node.try_get_context("env") or "prod"
stack_suffix = env_name.capitalize()

# The stateful stack is deployed once per environment.
stateful = StatefulStack(app, f"CodeCraftAiStatefulStack{stack_suffix}")

# The stateless stack contains the application and can be safely redeployed.
# It depends on the resources created in the stateful stack.
stateless = StatelessStack(
    app,
    f"CodeCraftAiStatelessStack{stack_suffix}",
    env_name=env_name,
    data_bucket=stateful.data_bucket,
    vector_store_bucket=stateful.vector_store_bucket,
    api_repo=stateful.api_repo,
    ingestion_repo=stateful.ingestion_repo,
)

app.synth()
