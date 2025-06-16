from . import server
import asyncio
import argparse


def main():
    """Main entry point for the package."""
    parser = argparse.ArgumentParser(description='Cygnus workflow MCP Server')
    parser.parse_args()  # Parse but do not use args
    asyncio.run(server.main())

__all__ = ["main", "server"]
