import click


@click.command()
@click.argument("training_data")
def preprocess(training_data):
    print(training_data)


if __name__ == '__main__':
    preprocess()
