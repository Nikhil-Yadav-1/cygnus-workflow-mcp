import requests
import time
import traceback

def invoke_service_tool(query = "what is the weather in Jaipur?"):
    """
    Tool to call the invoke-service (sync, using requests).

    Args:
        query (str): The user's query or question to be sent to the dashboard-component-insight-agent service. Example: "what is the weather in Jaipur?"

    Returns:
        str: The response text from the service, or an error message if the request fails.
        The response is typically a formatted string containing the requested information. For example, for a weather query, it may return:

            The current weather in Jaipur, India is as follows:
            - **Temperature:** 30°C
            - **Weather Description:** Mist
            - **Humidity:** 75%
            - **Wind Speed:** 19 km/h (from the SE)
            - **Pressure:** 1001 hPa
            - **Visibility:** 3 km
            - **Feels Like:** 32°C
            - **Cloud Cover:** 75%
            - **UV Index:** 8
            **Sunrise:** 05:33 AM  
            **Sunset:** 07:23 PM  
            ![Weather Icon](https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0006_mist.png)

    Description:
        This function sends a POST request to the local dashboard-component-insight-agent API endpoint with the provided user query. It includes required headers and body parameters such as mobile, session_id, and client_identifier. The function waits for 10 seconds after making the request, prints the status code and response, and returns the response text. In case of an exception, it prints and returns the error message.
    """
    url = "http://localhost:8000/api/v1/api-controller/invoke-service/dashboard-component-insight-agent/"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Bearer CA-9544ea96-b134f-4446-9cef-cddeAF027444GH",
        "Cookie": "sessionid=lrqk2nf3v9k3dqgn82x17nb9ed8eftbe"
    }
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
    print("Invoking service tool...\n")
    invoke_service_tool()