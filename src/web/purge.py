# -*- coding: utf-8; -*-
# vi: set encoding=utf-8

import sys
import fastly
from argparse import ArgumentParser


def purge(api_key):
    api = fastly.connect(api_key)
    print(api.purge_service_by_key('1bUC7xOWcgbVWpBPqPqHp', 'web'))


if __name__ == '__main__':
    """
    Usage: python purge.py --api-key <KEY>
    """
    parser = ArgumentParser(description='purge fastly')
    parser.add_argument('--api-key', type=str, help='Fastly API key')
    args = parser.parse_args()
    purge(args.api_key)

