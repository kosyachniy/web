"""
Create a spreadsheet in Google Sheets
"""

import argparse

from api.lib.docs import create_sheets


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


if __name__ == '__main__':
    main(_args())
