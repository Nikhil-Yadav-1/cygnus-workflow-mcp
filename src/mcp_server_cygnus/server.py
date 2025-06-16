import os
import sys
import logging
from pydantic import AnyUrl
from typing import Any

from mcp.server import InitializationOptions, NotificationOptions
from mcp.server.fastmcp.server import FastMCP
from mcp.server.stdio import stdio_server
import mcp.types as types


logger = logging.getLogger('mcp_cygnus_server')
logger.info("Starting MCP Server (Cygnus tools only)")

PROMPT_TEMPLATE = """
the assistant's goal is to fetch the invoke-service endpoint on the local API server and return the response as it is, to the user.
the assistant is supposed to wait for about 10 seconds after calling the invoke-service endpoint, to allow the server to process the request and return a response.
Prompts:
This server provides a pre-written prompt called "mcp-demo" that helps users create and analyze scenarios. The prompt accepts a "topic" argument and guides users through creating tables, analyzing data, and generating insights. For example, if a user provides "retail sales" as the topic, the prompt will help create relevant tables and guide the analysis process. Prompts basically serve as interactive templates that help structure the conversation with the LLM in a useful way.
Resources:
This server exposes one key resource: "memo://insights", which is a business insights memo that gets automatically updated throughout the analysis process. As users analyze and discover insights, the memo resource gets updated in real-time to reflect new findings. Resources act as living documents that provide context to the conversation.
Tools:
This server provides several tools:
"cygnus_alpha": A tool to read a sample text file (for demonstration purposes)
"invoke-service": A tool to call the dashboard-component-insight-agent service via HTTP POST to the local API.
"""

class CygnusServer(FastMCP):
    def __init__(self):
        super().__init__(name="mcp-server-cygnus")

    async def list_resources(self) -> list[types.Resource]:
        return [
            types.Resource(
                uri=AnyUrl("memo://insights"),
                name="Business Insights Memo",
                description="A living document of discovered business insights",
                mimeType="text/plain",
            )
        ]

    async def read_resource(self, uri: AnyUrl) -> str:
        if str(uri) == "memo://insights":
            return "No business insights have been discovered yet. (removed)"
        raise ValueError(f"Unknown resource: {uri}")

    async def list_tools(self) -> list[types.Tool]:
        return [
            types.Tool(
                name="cygnus_alpha",
                description="A tool to answer user's queries related to cygnus alpha",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "whatever the user asks about cygnus alpha"},
                    },
                    "required": ["query"],
                }
            ),
            types.Tool(
                name="invoke-service",
                description="Invoke the dashboard-component-insight-agent service via HTTP POST to the local API.",
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            ),
        ]

    async def call_tool(self, name: str, arguments: dict[str, Any]) -> list[types.TextContent]:
        if name == "cygnus_alpha":
            with open("/home/nikhil/Desktop/mcp/cygnus/workflow/sample.txt", "r") as file:
                content = file.read()
            return [types.TextContent(type="text", text=content)]
        elif name == "invoke-service":
            from mcp_server_cygnus.invoke_service_tool import invoke_service_tool
            result = invoke_service_tool()
            return [types.TextContent(type="text", text=result)]
        else:
            raise ValueError(f"Unknown tool: {name}")

    async def list_prompts(self) -> list[types.Prompt]:
        return [
            types.Prompt(
                name="mcp-demo",
                description="A prompt to seed the server with initial data and demonstrate what you can do with Cygnus tools",
                arguments=[
                    types.PromptArgument(
                        name="topic",
                        description="Topic to seed the server with initial data",
                        required=True,
                    )
                ],
            )
        ]

    async def get_prompt(self, name: str, arguments: dict[str, str] | None) -> types.GetPromptResult:
        if name != "mcp-demo":
            raise ValueError(f"Unknown prompt: {name}")
        if not arguments or "topic" not in arguments:
            raise ValueError("Missing required argument: topic")
        topic = arguments["topic"]
        prompt = PROMPT_TEMPLATE.format(topic=topic)
        return types.GetPromptResult(
            description=f"Demo template for {topic}",
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(type="text", text=prompt.strip()),
                )
            ],
        )

server = CygnusServer()

async def main():
    logger.info(f"Starting MCP Server (Cygnus tools only)")
    _server = CygnusServer()
    async with stdio_server() as (read_stream, write_stream):
        logger.info("Server running with stdio transport")
        await _server._mcp_server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="mcp-server-cygnus", # yahan change karna hai
                server_version="0.1.0",
                capabilities=_server._mcp_server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

class ServerWrapper():
    """A wrapper for compatibility with mcp[cli]"""
    def __init__(self):
        pass
    def run(self):
        import asyncio
        asyncio.run(main())

if __name__ == "__main__":
    wrapper = ServerWrapper()
    wrapper.run()
else:
    wrapper = ServerWrapper()
