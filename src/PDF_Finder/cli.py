# cli.py
import argparse
import asyncio
from .orchestrator import run


def main():
    parser = argparse.ArgumentParser(description="Batched DOI harvester: staged downloads → processing → reports")
    parser.add_argument("--config", required=True, help="Path to YAML config file")
    args = parser.parse_args()
    asyncio.run(run(args.config))


if __name__ == "__main__":
    main()
