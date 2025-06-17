import requests
import time
import traceback

def weather_workflow_tool(city: str = "Jaipur"):
    """
    Tool to fetch the weather for a given city using the dashboard-component-insight-agent service.

    Args:
        city (str): The name of the city for which to fetch the weather. Example: "Jaipur"

    Returns:
        str: The response text from the service, or an error message if the request fails.
        The response is typically a formatted string containing the weather information for the specified city.

    Description:
        This function sends a POST request to the local dashboard-component-insight-agent API endpoint with a weather query for the specified city. It includes required headers and body parameters such as mobile, session_id, and client_identifier. The function waits for 10 seconds after making the request, prints the status code and response, and returns the response text. In case of an exception, it prints and returns the error message.
    """
    url = "http://localhost:8000/api/v1/api-controller/invoke-service/dashboard-component-insight-agent/"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Bearer CA-9544ea96-b134f-4446-9cef-cddeAF027444GH",
        "Cookie": "sessionid=lrqk2nf3v9k3dqgn82x17nb9ed8eftbe"
    }
    query = f"what is the weather in {city}?"
    body = {
        "mobile": "1234567899",
        "text": query,
        "session_id": "h1",
        "client_identifier": "insights-5"
    }
    try:
        response = requests.post(url, headers=headers, data=body, timeout=40)
        time.sleep(10)
        print(f"Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        return response.text
    except Exception as e:
        print(f"Exception occurred: {e}")
        print(traceback.format_exc())
        return str(e)

if __name__ == "__main__":
    print("Invoking weather workflow tool...\n")
    weather_workflow_tool()
