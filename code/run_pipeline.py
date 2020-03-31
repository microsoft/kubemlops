import kfp
import argparse


def main():
    parser = argparse.ArgumentParser("run pipeline")

    parser.add_argument(
        "--kfp_host",
        type=str,
        required=False,
        default="http://localhost:8080/pipeline",
        help="KFP endpoint"
    )

    parser.add_argument(
        "--resource_group",
        type=str,
        required=True,
        help="Resource Group"
    )

    parser.add_argument(
        "--workspace",
        type=str,
        required=True,
        help="AML Workspace"
    )

    parser.add_argument(
        "--pipeline_id",
        type=str,
        required=True,
        help="Pipeline Id"
    )

    parser.add_argument(
        "--run_name",
        type=str,
        required=True,
        help="KFP run name "
    )

    parser.add_argument(
        "--experiment_name",
        type=str,
        required=False,
        default="Default",
        help="Kubeflow experiment name "
    )

    args = parser.parse_args()
    client = kfp.Client(host=args.kfp_host)

    pipeline_params = {}
    pipeline_params["resource_group"] = args.resource_group
    pipeline_params["workspace"] = args.workspace
    exp = client.get_experiment(experiment_name=args.experiment_name)  # noqa: E501
    client.run_pipeline(exp.id,
                        job_name=args.run_name,
                        params=pipeline_params,
                        pipeline_id=args.pipeline_id)


if __name__ == '__main__':
    exit(main())
