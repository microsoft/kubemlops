
import click
import mlflow


@click.command()
@click.argument("training_data")
def workflow(training_data):
    with mlflow.start_run() as active_run:                                        # noqa: F841, E501

        preprocess_run = mlflow.run(".", "preprocess", parameters={               # noqa: F841, E501
                                    "training_data": training_data})
        train_model_run = mlflow.run(".", "train", parameters={                   # noqa: F841, E501
                                     "training_data": training_data})


if __name__ == '__main__':
    workflow()
