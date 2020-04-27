import gh_actions_client
import argparse

parser = argparse.ArgumentParser(
    description='transfer learning for binary image task')
parser.add_argument('-s', '--base_path',
                    help='directory to base data', default='../../data')
parser.add_argument(
    '-d', '--data', help='directory to training and test data', default='train')  # noqa: E501
parser.add_argument(
    '-e', '--epochs', help='number of epochs', default=10, type=int)
parser.add_argument('-b', '--batch', help='batch size',
                    default=32, type=int)
parser.add_argument('-i', '--image_size',
                    help='image size', default=160, type=int)
parser.add_argument('-l', '--lr', help='learning rate',
                    default=0.0001, type=float)
parser.add_argument('-o', '--outputs',
                    help='output directory', default='model')
parser.add_argument('-f', '--dataset', help='cleaned data listing')
args = parser.parse_args()
