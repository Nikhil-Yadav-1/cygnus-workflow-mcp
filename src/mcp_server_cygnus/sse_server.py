import os
import sys
import logging
from pydantic import AnyUrl
from typing import Any

from mcp.server import InitializationOptions, NotificationOptions
from mcp.server.fastmcp.server import FastMCP
#import mcp.server.stdio import stdio_server  # removed for HTTP transport  # comment("here")
import mcp.types as types

import uvicorn  # comment("here")

logger = logging.getLogger('mcp_cygnus_server')
logger.info("Starting MCP Server (Cygnus tools only) over SSE HTTP")

PROMPT_TEMPLATE = """
Assistant Goals:
- Fetch the invoke-service endpoint on the local API server and return the response directly to the user.
- Wait approximately 10 seconds after calling the invoke-service endpoint to allow the server to process the request and respond.
- Suggest movies using the recobee movie suggestion tool for any movie-related queries.

Prompts:
- This server provides a pre-written prompt called "mcp-demo" to help users create and analyze scenarios. The prompt accepts a "topic" argument and guides users through creating tables, analyzing data, generating insights, and suggesting movies. For example, if a user provides "retail sales" as the topic, the prompt will help create relevant tables, guide the analysis process, and suggest movies related to retail or sales. Prompts serve as interactive templates to structure conversations with the LLM in a useful way.

Resources:
- This server exposes one key resource: "memo://mcp-server-cygnus", which provides Cygnus-specific information and context. Resources act as living documents providing context to the conversation.

Tools:
- "cygnus_alpha": Answers user queries related to cygnus alpha by reading a sample text file (for demonstration purposes).
- "invoke-service": Calls the dashboard-component-insight-agent service via HTTP POST to the local API and returns the response as-is.
- "weather-workflow-tool": Fetches the current weather for a specified city. Takes a single argument `city` (e.g., "Delhi") and returns a detailed weather report for that city using the dashboard-component-insight-agent service.
- "recobee-movie-suggestion-tool": Suggests movies based on user queries using the recobee-api-chat service. Takes a single argument `movie_query` (e.g., "Suggest a good sci-fi movie") and returns movie recommendations.
- "kindlife-bizz-chat": provides insights over kindlife's data and helps users with queries related to kindlife's business operations, products, and services.
"""

class CygnusServer(FastMCP):
    def __init__(self):
        super().__init__(name="mcp-server-cygnus")

    async def list_resources(self) -> list[types.Resource]:
        return [
            types.Resource(
                uri=AnyUrl("memo://mcp-server-cygnus"),
                name="Cygnus",
                description="A resource providing Cygnus-specific information and context.",
                mimeType="text/plain",
            )
        ]

    async def read_resource(self, uri: AnyUrl) -> str:
        if str(uri) == "memo://mcp-server-cygnus":
            return "simple mcp server for cygnus alpha, with tools and prompts to call workflows and invoke services."
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
            types.Tool(
                name="weather-workflow-tool",
                description="A weather tool which takes in the city name and returns the weather for that city using the dashboard-component-insight-agent service.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "city": {"type": "string", "description": "The name of the city to get the weather for (e.g., 'Jaipur')"},
                    },
                    "required": ["city"],
                },
            ),
            types.Tool(
                name="recobee-movie-suggestion-tool",
                description="A tool to suggest movies based on user queries using the recobee-api-chat service.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "movie_query": {"type": "string", "description": "The movie-related query for suggestions (e.g., 'Suggest a good sci-fi movie')"},
                    },
                    "required": ["movie_query"],
                }
            ),
            types.Tool(
                name="kindlife-bizz-chat",
                description="A tool to provide insights over kindlife's data and help users with queries related to kindlife's business operations, products, or services.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "The query related to kindlife's business operations, products, or services."},
                    },
                    "required": ["query"],
                }
            ),
        ]

    async def call_tool(self, name: str, arguments: dict[str, Any]) -> list[types.TextContent]:
        try:
            if name == "cygnus_alpha":
                answer = "invoke-service tool is used to call the dashboard-component-insight-agent service via HTTP POST to the local API. It is designed to fetch insights from the local API server."
                return [types.TextContent(type="text", text=answer)]
            elif name == "invoke-service":
                import asyncio
                from . import invoke_service_tool
                result = await asyncio.to_thread(invoke_service_tool.invoke_service_tool)
                return [types.TextContent(type="text", text=result)]
            elif name == "weather-workflow-tool":
                import asyncio
                from .tools import weather_workflow_tool
                city = arguments.get("city", "Jaipur")
                result = await asyncio.to_thread(weather_workflow_tool, city)
                return [types.TextContent(type="text", text=result)]
            elif name == "recobee-movie-suggestion-tool":
                import asyncio
                from .tools import recobee_movie_suggestion_tool
                movie_query = arguments.get("movie_query", "Suggest a good sci-fi movie")
                result = await asyncio.to_thread(recobee_movie_suggestion_tool, movie_query)
                return [types.TextContent(type="text", text=result)]
            elif name == "kindlife-bizz-chat":
                import asyncio
                from .tools import kindlife_bizz_chat_tool
                query = arguments.get("query", "Tell me about kindlife's latest products")
                result = await asyncio.to_thread(kindlife_bizz_chat_tool, query)
                return [types.TextContent(type="text", text=result)]
            else:
                raise ValueError(f"Unknown tool: {name}")
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error while calling tool '{name}': {str(e)}")]

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

app = server.sse_app()

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=os.getenv("MCP_HOST", "0.0.0.0"),
        port=int(os.getenv("MCP_PORT", "8070")),
    )
