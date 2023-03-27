"""
Create a spreadsheet in Google Sheets

python -m scripts.create_sheets --title="" --mail=""
"""

import argparse

# pylint: disable=import-error
from lib.docs import create_sheets


def _args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--title',
        type=str,
        required=False,
        default='Title',
        help='Spreadsheet title',
    )

    parser.add_argument(
        '--mail',
        type=str,
        required=True,
        help='Admin e-mail',
    )

    return parser.parse_args()


def main(args: argparse.Namespace):
    """ Create a spreadsheet by title and email """
    print(create_sheets(args.title, args.mail))
    print("Don't forget to add a second sheet to the table!")


if __name__ == '__main__':
    main(_args())
