import httpx
import json

url = "http://localhost:8070/mcp/?session_id=test-session"
headers = {
    "Accept": "application/json, text/event-stream",
    "Content-Type": "application/json"
}

with httpx.Client(http2=True, timeout=None) as client:
    # Initialize session
    init_payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "1.0",
            "capabilities": {},
            "clientInfo": {"name": "httpx", "version": "1.0"}
        }
    }
    resp = client.post(url, headers=headers, content=json.dumps(init_payload))
    print(resp.text)

    # List tools (reuse the same client/session)
    tools_payload = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    }
    resp = client.post(url, headers=headers, content=json.dumps(tools_payload))
    print(resp.text)

    # Call kindlife-bizz-chat tool
    kindlife_payload = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "kindlife-bizz-chat",
            "arguments": {"query": "Tell me about kindlife's latest products"}
        }
    }
    resp = client.post(url, headers=headers, content=json.dumps(kindlife_payload))
    print(resp.text)

    # Call my-account-chat tool
    my_account_payload = {
        "jsonrpc": "2.0",
        "id": 4,
        "method": "tools/call",
        "params": {
            "name": "my-account-chat",
            "arguments": {"query": "i wanna know about superkind"}
        }
    }
    resp = client.post(url, headers=headers, content=json.dumps(my_account_payload))
    print(resp.text)