import argparse
import papermill as pm
from pathlib2 import Path
import json


def info(msg, char="#", width=75):
    print("")
    print(char * width)
    print(char + "   %0*s" % ((-1 * width) + 5, msg) + char)
    print(char * width)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parameters for notebook')
    parser.add_argument('-tp', '--train_data_path',
                        help='Path to traning data', default='../../data')
    parser.add_argument('-no', '--notebook_output', help='Notebook Output')
    args = parser.parse_args()
    pm.execute_notebook('/scripts/experiment.ipynb', '/scripts/output.ipynb',
                        parameters=dict(traning_data_path=args.train_data_path), kernel_name="python3")  # noqa: E501

    notebook_output_file = Path(args.notebook_output).resolve(strict=False)
    Path(notebook_output_file).parent.mkdir(parents=True, exist_ok=True)

    with open('/scripts/output.ipynb') as f:
        data = json.load(f)

    with open(str(notebook_output_file), 'w+') as f:
        f.write(str(data))

    info("NoteBook execution completed")
