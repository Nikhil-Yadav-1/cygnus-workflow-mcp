import requests

def invoke_service_tool():
    """
    Tool to call the /invoke-service endpoint
    """
    url = "http://localhost:8000/api/v1/api-controller/invoke-service/dashboard-component-insight-agent/"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Bearer CA-9544ea96-b134f-4446-9cef-cddeAF027444GH",
        "Cookie": "sessionid=lrqk2nf3v9k3dqgn82x17nb9ed8eftbe"
    }
    data = {
        "mobile": "1234567899",
        "text": "what is the weather in Jaipur?",
        "session_id": "f101",
        "client_identifier": "insights-5"
    }
    response = requests.post(url, headers=headers, data=data)
    return response.text

# mcp dev src/mcp_server_cygnus/server.py:wrapper