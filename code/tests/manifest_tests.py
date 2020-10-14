import kfp


def test_func():
    print('This is the test function to make sure the ' +
          'installation of kubeflow is correct ' +
          'and pipelines could be executed correctly.')
    print(1 + 1)


if __name__ == "__main__":
    # convert Python function into a pipeline component
    op = kfp.components.func_to_container_op(test_func)

    # write a pipeline function using DSL
    @kfp.dsl.pipeline(
            name='Testing pipeline',
            description='Testing pipeline'
            )
    def test_pipeline():
        my_step = op()
        print(my_step.name)

    kfp.compiler.Compiler().compile(test_pipeline, 'test-pipeline.zip')

    client = kfp.Client()
    experiment = client.create_experiment(name='test')
    run = client.run_pipeline(experiment.id,
                              'test-pipeline',
                              'test-pipeline.zip')
    print(run)
