# aws/ssm/create-dev-appconfig.sh (create new)
# Recreateable script to provision the /codecraft-ai/dev/AppConfig parameter in AWS SSM Parameter Store.
# This ensures your local, CI, and cloud environments are always aligned and reproducible.

# --- Prerequisites ---
# - AWS CLI installed and configured with credentials/region (aws configure)
# - IAM permissions to write to SSM Parameter Store

# --- Usage ---
#   bash aws/ssm/create-dev-appconfig.sh

set -euo pipefail

SSM_PARAM_NAME="/codecraft-ai/dev/AppConfig"
AWS_REGION="${AWS_REGION:-af-south-1}"  # Default to your project's region
CONFIG_FILE="config/dev.json"

if [ ! -f "$CONFIG_FILE" ]; then
  echo "ERROR: $CONFIG_FILE does not exist. Please create it with your dev config JSON."
  exit 1
fi

echo "Uploading $CONFIG_FILE to SSM Parameter Store as $SSM_PARAM_NAME in $AWS_REGION..."

aws ssm put-parameter \
  --name "$SSM_PARAM_NAME" \
  --type "String" \
  --value "$(cat $CONFIG_FILE)" \
  --overwrite \
  --region "$AWS_REGION"

echo "✅ SSM parameter $SSM_PARAM_NAME updated successfully."
