import kfp
import os
import argparse


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

    args = parser.parse_args()

    host = args.kfp_host
    pipeline_file_path = args.pipeline_file_path
    pipeline_name = "{0}-{1}".format(args.pipeline_name, args.run_id)

    client = kfp.Client(host=host)
    pipeline_file = os.path.join(pipeline_file_path)
    try:
        # We upload a new pipline every time with a run_id in the pipeline name
        # until the issue with uploading a pipeline version is resolved
        # see  https://github.com/kubeflow/pipelines/issues/3442
        pipeline = client.pipeline_uploads.upload_pipeline(pipeline_file, name=pipeline_name)  # noqa: E501
        return pipeline.id

    except TypeError as err:
        print("An error related to this issue https://github.com/kubeflow/pipelines/issues/3441 {0}".format(err))  # noqa: E501
    # pipeline_version = client.pipeline_uploads.upload_pipeline_version(pipeline_file,  # noqa: E501  # noqa: E501
    #                                                                    name="Version1",  # noqa: E501  # noqa: E501
    #                                                                    pipelineid=pipeline.id)  # noqa: E501  # noqa: E501


if __name__ == '__main__':
    exit(main())
