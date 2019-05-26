import click


APP_YAML_TEMPLATE = """runtime: python37
env_variables:
  ELMO_BASE_URL: '{BASE_URL}'
  ELMO_VENDOR: '{VENDOR}'
handlers:
- url: /.*
  script: auto
  secure: always
  redirect_http_response_code: 301
"""


@click.command()
@click.argument("base_url")
@click.argument("vendor")
def generate_app_yaml(base_url, vendor):
    """Use APP_YAML_TEMPLATE to generate app.yaml for AppEngine deployments.

    Args:
        base_url: defines ELMO_BASE_URL env variable in AppEngine config.
        vendor: defines ELMO_VENDOR env variable in AppEngine config.
    Returns:
        Writes `app.yaml` file in the current folder.
    """
    print("Writing the following deployment config to disk:")
    app_yaml = APP_YAML_TEMPLATE.format(BASE_URL=base_url, VENDOR=vendor)
    print(app_yaml)

    with open("app.yaml", "w") as f:
        f.write(app_yaml)
    print("Done! You can deploy the service with `gcloud app deploy`")


if __name__ == "__main__":
    generate_app_yaml()
