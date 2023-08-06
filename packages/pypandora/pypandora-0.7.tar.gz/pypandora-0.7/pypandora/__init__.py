import argparse
import json
import sys

from pathlib import Path

from .api import PyPandora


def main():
    parser = argparse.ArgumentParser(description='Submit a file.')
    parser.add_argument('--url', type=str, help='URL of the instance (defaults to https://pandora.circl.lu/).')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--redis_up', action='store_true', help='Check if redis is up.')
    group.add_argument('-f', '--file', type=Path, help='Path to the file to submit.')
    args = parser.parse_args()

    if args.url:
        client = PyPandora(args.url)
    else:
        client = PyPandora()

    if not client.is_up:
        print(f'Unable to reach {client.root_url}. Is the server up?')
        sys.exit(1)
    if args.redis_up:
        response = client.redis_up()
    elif args.file:
        response = client.submit_from_disk(args.file, seed_expire=3600)
    print(json.dumps(response, indent=2))
