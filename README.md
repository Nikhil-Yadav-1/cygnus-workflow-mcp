# Cygnus MCP Server (Cygnus Tools Only)

## Overview
A Model Context Protocol (MCP) server implementation that provides two demonstration tools: `cygnus_alpha` (reads a sample text file) and `invoke-service` (calls a local API endpoint). This server is designed for demonstration and integration with Cygnus workflows, and does not use or require any database.

## Components

### Resources
The server exposes a single resource:
- `memo://insights`: A business insights memo (static, as no database is used)

### Prompts
The server provides a demonstration prompt:
- `mcp-demo`: Interactive prompt that guides users through scenario analysis
  - Required argument: `topic` - The domain to analyze
  - Generates a template for analysis and insight generation
  - Integrates with the business insights memo

### Tools
The server offers two core tools:

- `cygnus_alpha`
   - Reads and returns the contents of a sample text file
   - Input:
     - `query` (string): Any user query (for demonstration)
   - Returns: Contents of the sample file

- `invoke-service`
   - Calls the dashboard-component-insight-agent service via HTTP POST to the local API
   - No input required
   - Returns: The response from the local API service


## Usage with Claude Desktop

### uv

```bash
# Add the server to your claude_desktop_config.json
"mcpServers": {
  "cygnus": {
    "command": "uv",
    "args": [
      "--directory",
      "parent_of_servers_repo/servers/src/cygnus",
      "run",
      "mcp-server-cygnus"
    ]
  }
}
```

### Docker

```json
# Add the server to your claude_desktop_config.json
"mcpServers": {
  "cygnus": {
    "command": "docker",
    "args": [
      "run",
      "--rm",
      "-i",
      "mcp/cygnus"
    ]
  }
}
```

## Usage with VS Code

For quick installation, click the installation buttons below (update the name/command as needed):

[![Install with UV in VS Code](https://img.shields.io/badge/VS_Code-UV-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=cygnus&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22mcp-server-cygnus%22%5D%7D) [![Install with UV in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-UV-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=cygnus&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22mcp-server-cygnus%22%5D%7D&quality=insiders)

[![Install with Docker in VS Code](https://img.shields.io/badge/VS_Code-Docker-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=cygnus&config=%7B%22command%22%3A%22docker%22%2C%22args%22%3A%5B%22run%22%2C%22-i%22%2C%22--rm%22%2C%22mcp%2Fcygnus%22%5D%7D) [![Install with Docker in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Docker-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=cygnus&config=%7B%22command%22%3A%22docker%22%2C%22args%22%3A%5B%22run%22%2C%22-i%22%2C%22--rm%22%2C%22mcp%2Fcygnus%22%5D%7D&quality=insiders)

For manual installation, add the following JSON block to your User Settings (JSON) file in VS Code. You can do this by pressing `Ctrl + Shift + P` and typing `Preferences: Open Settings (JSON)`.

Optionally, you can add it to a file called `.vscode/mcp.json` in your workspace. This will allow you to share the configuration with others.

> Note that the `mcp` key is needed when using the `mcp.json` file.

### uv

```json
{
  "mcp": {
    "servers": {
      "cygnus": {
        "command": "uvx",
        "args": [
          "mcp-server-cygnus"
        ]
      }
    }
  }
}
```

### Docker

```json
{
  "mcp": {
    "servers": {
      "cygnus": {
        "command": "docker",
        "args": [
          "run",
          "-i",
          "--rm",
          "mcp/cygnus"
        ]
      }
    }
  }
}
```

## Building

Docker:

```bash
docker build -t mcp/cygnus .
```

## Test with MCP inspector

```bash
uv add "mcp[cli]"
mcp dev src/mcp_server_cygnus/server.py:server
```

## License

This MCP server is licensed under the MIT License. This means you are free to use, modify, and distribute the software, subject to the terms and conditions of the MIT License. For more details, please see the LICENSE file in the project repository.
