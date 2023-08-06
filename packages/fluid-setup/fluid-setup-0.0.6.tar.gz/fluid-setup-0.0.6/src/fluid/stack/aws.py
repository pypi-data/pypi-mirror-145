from typing import (
    Dict,
)


def generate_login_function(config: Dict) -> str:
    return f"""function okta-login {{
  local role="${{1:-{config["credentials"]["role"]}}}" # Set as default role the role that you uses most
  local role_uppercase="$(echo "${{role^^}}" | tr - _)" # Used to export "PROD_*" vars
  local env="${{role_uppercase##*_}}" # Services compatibility
  local args=(
    authenticate
    --user "{config["credentials"]["email"]}"
    --pass "{config["credentials"]["password"]}"
    --organization {config["organization"]}
    --role "arn:aws:iam::{config["iam"]}:role/${{role}}"
    --application {config["application"]}
    --silent
    --duration 32400
    --environment
    --no-aws-cache
  ) # Flags required for aws-okta-processor

  eval $(aws-okta-processor "${{args[@]}}") \
    && export "${{role_uppercase}}_AWS_ACCESS_KEY_ID"="${{AWS_ACCESS_KEY_ID}}" \
    && export "${{role_uppercase}}_AWS_SECRET_ACCESS_KEY"="${{AWS_SECRET_ACCESS_KEY}}" \
    && export "${{env}}_AWS_ACCESS_KEY_ID"="${{AWS_ACCESS_KEY_ID}}" \
    && export "${{env}}_AWS_SECRET_ACCESS_KEY"="${{AWS_SECRET_ACCESS_KEY}}"
}}"""


def setup_aws(config: Dict) -> None:
    if not config["setup"]:
        return
    function = generate_login_function(config)
    print(function)
