import logging
import asyncio
import json
from typing import Any
from pydantic import AnyUrl
import mcp.types as types
from mcp.server import Server
import uvicorn
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import StreamingResponse, Response, JSONResponse
from starlette.routing import Route
from starlette.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('mcp_cygnus_http_server')

class CygnusServer:
    def __init__(self):
        self.server = Server("mcp-server-cygnus")
        self.initialized = False
        
        self.server.list_resources = self.list_resources
        self.server.read_resource = self.read_resource
        self.server.list_tools = self.list_tools
        self.server.call_tool = self.call_tool
        self.server.list_prompts = self.list_prompts
        self.server.get_prompt = self.get_prompt

    async def list_resources(self) -> list[types.Resource]:
        """List available resources"""
        return [
            types.Resource(
                uri=AnyUrl("memo://mcp-server-cygnus"),
                name="Cygnus Server Info",
                description="Information about the Cygnus MCP server and its capabilities",
                mimeType="text/plain",
            )
        ]

    async def read_resource(self, uri: AnyUrl) -> str:
        """Read a specific resource"""
        if str(uri) == "memo://mcp-server-cygnus":
            return """
            Cygnus MCP Server

            This is an MCP (Model Context Protocol) server providing access to Cygnus tools and workflows.

            Available Tools:
            - cygnus_alpha: Query Cygnus Alpha information
            - weather-workflow-tool: Get weather information for cities
            - recobee-movie-suggestion-tool: Get movie recommendations
            - kindlife-bizz-chat: Query KindLife business data

            Available Prompts:
            - mcp-demo: Interactive demo prompt with topic-based guidance

            Resources:
            - This memo resource providing server information
            """.strip()
        raise ValueError(f"Unknown resource: {uri}")

    async def list_tools(self) -> list[types.Tool]:
        """List available tools"""
        return [
            types.Tool(
                name="cygnus_alpha",
                description="Query information related to Cygnus Alpha system",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string", 
                            "description": "Query about Cygnus Alpha system"
                        }
                    },
                    "required": ["query"],
                }
            ),
            types.Tool(
                name="weather-workflow-tool",
                description="Get current weather information for a specified city",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string", 
                            "description": "Name of the city to get weather for (e.g., 'Jaipur', 'Delhi')"
                        }
                    },
                    "required": ["city"],
                },
            ),
            types.Tool(
                name="recobee-movie-suggestion-tool",
                description="Get movie suggestions based on user preferences or queries",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "movie_query": {
                            "type": "string", 
                            "description": "Movie-related query or preferences (e.g., 'Suggest a good sci-fi movie', 'Comedy movies from 2020')"
                        }
                    },
                    "required": ["movie_query"],
                }
            ),
            types.Tool(
                name="kindlife-bizz-chat",
                description="Query KindLife business data and get insights about operations, products, or services",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string", 
                            "description": "Business-related query about KindLife operations, products, or services"
                        }
                    },
                    "required": ["query"],
                }
            ),
            types.Tool(
                name="my-account-chat",
                description="Interact with the Kindlife.in customer support chatbot for product information, order support, promotions, membership programs, and community resources",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string", 
                            "description": "Your question or request about Kindlife.in services (e.g., 'Tell me about your clean beauty products', 'How do I track my order?')"
                        }
                    },
                    "required": ["query"],
                }
            ),
        ]

    async def call_tool(self, name: str, arguments: dict[str, Any]) -> list[types.TextContent]:
        """Execute a tool call"""
        try:
            if name == "cygnus_alpha":
                query = arguments.get("query", "")
                try:
                    from mcp_server_cygnus.tools import cygnus_alpha_tool
                    result = await asyncio.to_thread(cygnus_alpha_tool, query)
                except ImportError:
                    result = f"Cygnus Alpha Response: The invoke-service tool is used to call the dashboard-component-insight-agent service via HTTP POST to the local API. Query received: {query}"
                return [types.TextContent(type="text", text=result)]
                    
            elif name == "weather-workflow-tool":
                city = arguments.get("city", "Unknown City")
                try:
                    from mcp_server_cygnus.tools import weather_workflow_tool
                    result = await asyncio.to_thread(weather_workflow_tool, city)
                except ImportError:
                    result = f"Weather for {city}: Sunny, 25°C (77°F), Humidity: 60%, Wind: 10 km/h. This is a mock response - integrate with actual weather service."
                return [types.TextContent(type="text", text=result)]
                
            elif name == "recobee-movie-suggestion-tool":
                movie_query = arguments.get("movie_query", "")
                try:
                    from mcp_server_cygnus.tools import recobee_movie_suggestion_tool
                    result = await asyncio.to_thread(recobee_movie_suggestion_tool, movie_query)
                except ImportError:
                    result = f"Movie Suggestions for '{movie_query}': Based on your query, here are some recommendations: 1. Blade Runner 2049 (Sci-Fi), 2. Interstellar (Sci-Fi Drama), 3. The Matrix (Action Sci-Fi). This is a mock response - integrate with actual Recobee API."
                return [types.TextContent(type="text", text=result)]
                
            elif name == "kindlife-bizz-chat":
                query = arguments.get("query", "")
                try:
                    from mcp_server_cygnus.tools import kindlife_bizz_chat_tool
                    result = await asyncio.to_thread(kindlife_bizz_chat_tool, query)
                except ImportError:
                    result = f"KindLife Business Insights for '{query}': Our latest products show strong market performance with 15% growth in Q4. Customer satisfaction remains high at 4.2/5 stars. This is a mock response - integrate with actual KindLife business data API."
                return [types.TextContent(type="text", text=result)]
                
            elif name == "my-account-chat":
                query = arguments.get("query", "")
                try:
                    from mcp_server_cygnus.tools import my_account_chat_tool
                    result = await asyncio.to_thread(my_account_chat_tool, query)
                except ImportError:
                    result = f"Kindlife.in Customer Support: I can help you with information about our products, order tracking, promotions, membership programs, and community resources. Please try again with a specific question. Your query was: '{query}'"
                return [types.TextContent(type="text", text=result)]

            else:
                raise ValueError(f"Unknown tool: {name}")
                
        except Exception as e:
            logger.error(f"Error in tool {name}: {e}")
            return [types.TextContent(type="text", text=f"Error executing tool {name}: {str(e)}")]

    async def list_prompts(self) -> list[types.Prompt]:
        """List available prompts"""
        return [
            types.Prompt(
                name="mcp-demo",
                description="Interactive demo prompt that guides users through creating scenarios, analyzing data, and getting suggestions",
                arguments=[
                    types.PromptArgument(
                        name="topic", 
                        description="The topic or domain to focus the demo on (e.g., 'retail sales', 'weather analysis', 'movie recommendations')", 
                        required=True
                    )
                ],
            )
        ]

    async def get_prompt(self, name: str, arguments: dict[str, str] | None) -> types.GetPromptResult:
        """Get a specific prompt"""
        if name != "mcp-demo":
            raise ValueError(f"Unknown prompt: {name}")
            
        if not arguments or "topic" not in arguments:
            raise ValueError("Missing required argument: topic")
            
        topic = arguments["topic"]
        
        prompt_content = f"""
        # MCP Cygnus Demo: {topic}

        Welcome to the Cygnus MCP Server demonstration focused on: **{topic}**

        ## Available Tools for {topic}:

        1. **cygnus_alpha** - Query Cygnus Alpha system information
        2. **weather-workflow-tool** - Get weather data (useful for location-based {topic} analysis)
        3. **recobee-movie-suggestion-tool** - Get movie recommendations (great for entertainment-related {topic})
        4. **kindlife-bizz-chat** - Query business insights (perfect for business-related {topic})

        ## Suggested Workflow:

        1. Start by using the **cygnus_alpha** tool to understand the system capabilities for {topic}
        2. If your {topic} involves locations, try the **weather-workflow-tool**
        3. For entertainment aspects of {topic}, use **recobee-movie-suggestion-tool**
        4. For business insights related to {topic}, use **kindlife-bizz-chat**

        ## Example Queries:

        - "What can Cygnus Alpha tell me about {topic}?"
        - "Get weather data for cities relevant to {topic}"
        - "Suggest movies related to {topic}"
        - "What business insights does KindLife have about {topic}?"

        Try any of these tools to explore {topic} with the Cygnus system!
        """.strip()
        
        return types.GetPromptResult(
            description=f"Interactive demo template for exploring {topic} with Cygnus tools",
            messages=[
                types.PromptMessage(
                    role="user", 
                    content=types.TextContent(type="text", text=prompt_content)
                )
            ]
        )

cygnus_server = CygnusServer()

async def handle_mcp_request_logic(rpc_request: dict) -> dict:
    """Handle MCP protocol request logic with proper error handling and logging"""
    method = rpc_request.get("method")
    params = rpc_request.get("params", {})
    request_id = rpc_request.get("id")
    
    logger.info(f"Handling MCP request: {method} with params: {params}")
    
    try:
        if method == "initialize":
            cygnus_server.initialized = True
            result = {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "resources": {
                        "subscribe": False, 
                        "listChanged": False
                    },
                    "tools": {
                        "listChanged": False
                    },
                    "prompts": {
                        "listChanged": False
                    }
                },
                "serverInfo": {
                    "name": "mcp-server-cygnus",
                    "version": "1.0.0"
                }
            }
            logger.info("Server initialized successfully")
            
        elif method == "initialized":
            logger.info("Client confirmed initialization")
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {}
            }
            
        elif method == "resources/list":
            if not cygnus_server.initialized:
                raise ValueError("Server not initialized")
            resources = await cygnus_server.list_resources()
            result = {"resources": [r.model_dump() for r in resources]}
            logger.info(f"Listed {len(resources)} resources")
            
        elif method == "resources/read":
            if not cygnus_server.initialized:
                raise ValueError("Server not initialized")
            uri = params.get("uri")
            if not uri:
                raise ValueError("Missing required parameter: uri")
            content = await cygnus_server.read_resource(AnyUrl(uri))
            result = {"contents": [{"uri": uri, "mimeType": "text/plain", "text": content}]}
            logger.info(f"Read resource: {uri}")
            
        elif method == "tools/list":
            if not cygnus_server.initialized:
                raise ValueError("Server not initialized")
            tools = await cygnus_server.list_tools()
            result = {"tools": [t.model_dump() for t in tools]}
            logger.info(f"Listed {len(tools)} tools: {[t.name for t in tools]}")
            
        elif method == "tools/call":
            if not cygnus_server.initialized:
                raise ValueError("Server not initialized")
            name = params.get("name")
            arguments = params.get("arguments", {})
            if not name:
                raise ValueError("Missing required parameter: name")
            contents = await cygnus_server.call_tool(name, arguments)
            result = {"content": [c.model_dump() for c in contents]}
            logger.info(f"Called tool: {name}")
            
        elif method == "prompts/list":
            if not cygnus_server.initialized:
                raise ValueError("Server not initialized")
            prompts = await cygnus_server.list_prompts()
            result = {"prompts": [p.model_dump() for p in prompts]}
            logger.info(f"Listed {len(prompts)} prompts")
            
        elif method == "prompts/get":
            if not cygnus_server.initialized:
                raise ValueError("Server not initialized")
            name = params.get("name")
            arguments = params.get("arguments")
            if not name:
                raise ValueError("Missing required parameter: name")
            prompt_result = await cygnus_server.get_prompt(name, arguments)
            result = prompt_result.model_dump()
            logger.info(f"Got prompt: {name}")
            
        else:
            logger.error(f"Unknown method: {method}")
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32601, "message": f"Method not found: {method}"}
            }
        
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": result
        }
        logger.info(f"Successfully handled {method}")
        return response
        
    except Exception as e:
        logger.error(f"Error handling method {method}: {e}")
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
        }

async def handle_mcp_request(request: Request) -> Response:
    """Handle MCP protocol requests (both POST and GET for SSE)"""
    try:
        if request.method == "GET":
            return await handle_mcp_sse(request)
        elif request.method != "POST":
            return Response("Only POST and GET requests are supported for MCP protocol", status_code=405)
        
        body = await request.body()
        if not body:
            return Response("Request body is required", status_code=400)
            
        try:
            rpc_request = json.loads(body.decode())
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON: {e}")
            return Response("Invalid JSON", status_code=400)
        
        if not isinstance(rpc_request, dict) or "jsonrpc" not in rpc_request:
            return Response("Invalid JSON-RPC request", status_code=400)
        
        response_data = await handle_mcp_request_logic(rpc_request)
        
        return Response(
            json.dumps(response_data),
            media_type="application/json",
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization",
            }
        )
        
    except Exception as e:
        logger.error(f"Unexpected error handling MCP request: {e}")
        error_response = {
            "jsonrpc": "2.0",
            "id": rpc_request.get("id") if 'rpc_request' in locals() else None,
            "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
        }
        return Response(
            json.dumps(error_response),
            media_type="application/json",
            status_code=500
        )

async def handle_mcp_sse(request: Request) -> StreamingResponse:
    """Handle MCP protocol with Server-Sent Events"""
    logger.info("Setting up SSE connection for MCP protocol")
    
    async def event_stream():
        try:
            yield f"data: {json.dumps({'type': 'connection', 'status': 'established', 'server': 'mcp-server-cygnus'})}\n\n"
            
            while True:
                await asyncio.sleep(30)
                yield f"data: {json.dumps({'type': 'keepalive', 'timestamp': asyncio.get_event_loop().time()})}\n\n"
                
        except asyncio.CancelledError:
            logger.info("SSE connection cancelled")
            yield f"data: {json.dumps({'type': 'connection', 'status': 'cancelled'})}\n\n"
        except Exception as e:
            logger.error(f"SSE stream error: {e}")
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
    
    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Cache-Control, Content-Type",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS"
        }
    )

async def discover_capabilities(request: Request) -> JSONResponse:
    """Discovery endpoint for agents to understand server capabilities"""
    try:
        tools = await cygnus_server.list_tools()
        
        capabilities = {
            "name": "mcp-server-cygnus",
            "version": "1.0.0",
            "capabilities": {
                "tools": {
                    "list": True,
                    "call": True,
                    "register": False,
                    "listChanged": False,
                    "available_tools": [{
                        "name": tool.name,
                        "description": tool.description,
                        "input_schema": tool.inputSchema
                    } for tool in tools]
                },
                "resources": {
                    "list": True,
                    "read": True,
                    "subscribe": False,
                    "listChanged": False
                },
                "prompts": {
                    "list": True,
                    "get": True,
                    "listChanged": False
                }
            },
            "endpoints": {
                "mcp": "/mcp",
                "health": "/health"
            },
            "description": "Cygnus MCP Server with tools for weather, movies, and business insights"
        }
        
        logger.info("Serving capabilities:")
        logger.info(f"- Tools: {[tool.name for tool in tools]}")
        logger.info(f"- Endpoints: {capabilities['endpoints']}")
        
        return JSONResponse(capabilities)
        
    except Exception as e:
        logger.error(f"Error in discover_capabilities: {e}")
        return JSONResponse(
            {"error": f"Failed to get server capabilities: {str(e)}"},
            status_code=500
        )

async def health_check(request: Request) -> Response:
    """Health check endpoint"""
    return Response("OK", status_code=200)

app = Starlette(
    routes=[
        Route("/", discover_capabilities, methods=["GET"]),
        Route("/discover", discover_capabilities, methods=["GET"]),
        Route("/mcp", handle_mcp_request, methods=["GET", "POST"]),
        Route("/mcp/sse", handle_mcp_sse, methods=["GET"]),  
        Route("/health", health_check, methods=["GET"]),
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def main():
    """Main entry point"""
    logger.info("Starting Fixed Cygnus MCP HTTP Server on port 8070")
    logger.info("Available endpoints:")
    logger.info("  GET / or /discover - Server capabilities")
    logger.info("  POST /mcp - MCP protocol endpoint")
    logger.info("  GET /health - Health check")
    logger.info("")
    logger.info("Windsurf Configuration:")
    logger.info('  "mcp-server-cygnus-http": {')
    logger.info('    "serverUrl": "http://localhost:8070/mcp"')
    logger.info('  }')
    
    uvicorn.run(
        "http_server:app",
        host="0.0.0.0",
        port=8070,
        log_level="info",
        access_log=True,
        reload=False,
        timeout_keep_alive=15
    )

if __name__ == "__main__":
    main()