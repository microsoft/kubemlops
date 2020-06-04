import kfp
import os
import argparse
from utils.azure_auth import get_access_token


def main():
    parser = argparse.ArgumentParser("publish pipeline")

    parser.add_argument(
        "--run_id",
        type=str,
        required=True,
        help="unique CI run id"
    )

    parser.add_argument(
        "--kfp_host",
        type=str,
        required=False,
        default="http://localhost:8080/pipeline",
        help="KFP endpoint"
    )

    parser.add_argument(
        "--pipeline_file_path",
        type=str,
        required=False,
        default="pipeline.py.tar.gz",
        help="KFP pipeline file path"
    )

    parser.add_argument(
        "--pipeline_name",
        type=str,
        required=True,
        help="KFP pipeline name "
    )

    parser.add_argument(
        "--tenant",
        type=str,
        required=True,
        help="Tenant"
    )

    parser.add_argument(
        "--service_principal",
        type=str,
        required=True,
        help="Service Principal"
    )

    parser.add_argument(
        "--sp_secret",
        type=str,
        required=True,
        help="Service Principal Secret"
    )

    args = parser.parse_args()

    pipeline_file_path = args.pipeline_file_path
    pipeline_name = "{0}-{1}".format(args.pipeline_name, args.run_id)

    token = get_access_token(args.tenant, args.service_principal, args.sp_secret)  # noqa: E501
    client = kfp.Client(host=args.kfp_host, existing_token=token)

    pipeline_file = os.path.join(pipeline_file_path)
    # We upload a new pipline every time with a run_id in the pipeline name
    # until the issue with uploading a pipeline version is resolved
    # see  https://github.com/kubeflow/pipelines/issues/3442
    pipeline = client.pipeline_uploads.upload_pipeline(pipeline_file, name=pipeline_name)  # noqa: E501
    return pipeline.id


if __name__ == '__main__':
    exit(main())
