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
    
def recobee_movie_suggestion_tool(movie_query: str = "Suggest a good sci-fi movie"):
    """
    Tool to fetch movie suggestions using the recobee-api-chat service.

    Args:
        movie_query (str): The movie-related query for suggestions. Example: "Suggest a good sci-fi movie"

    Returns:
        str: The response text from the service, or an error message if the request fails.
        The response is typically a formatted string containing movie suggestions based on the query.

    Description:
        This function sends a POST request to the local recobee-api-chat API endpoint with a movie suggestion query. It includes required headers and body parameters such as mobile, session_id, and client_identifier. The function waits for 10 seconds after making the request, prints the status code and response, and returns the response text. In case of an exception, it prints and returns the error message.
    """
    url = "http://localhost:8000/api/v1/api-controller/invoke-service/recobee-api-chat/"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Bearer recobee-badb5552-1429-4d3e-9169-afd01c80add6",
        "Cookie": "sessionid=lrqk2nf3v9k3dqgn82x17nb9ed8eftbe"
    }
    body = {
        "mobile": "1234567899",
        "text": movie_query,
        "session_id": "h1dddd",
        "client_identifier": "insights-5"
    }
    try:
        response = requests.post(url, headers=headers, data=body, timeout=40)
        time.sleep(15)
        print(f"Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        return response.text
    except Exception as e:
        print(f"Exception occurred: {e}")
        print(traceback.format_exc())
        return str(e)

def kindlife__bizz_chat(query: str = "gmv for last 3 months"):
    """
    Tool to fetch movie suggestions using the kindlife__bizz_chat service.

    Args:
        query (str): The query related to kindlife's business operations, products, or services. Example: "gmv for last 3 months"

    Returns:
        str: The response text from the service, or an error message if the request fails.
        The response is typically a formatted string containing insights based on the query.

    Description:
        This function sends a POST request to the local kindlife__bizz_chat API endpoint with a query. It includes required headers and body parameters such as mobile, session_id, and client_identifier. The function waits for 10 seconds after making the request, prints the status code and response, and returns the response text. In case of an exception, it prints and returns the error message.
    """
    url = "http://localhost:8000/api/v1/api-controller/invoke-service/kindlife-bizz-chat/"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Bearer kindlife-a210a35a-c140-43fb-8030-31231edebbbb",
        "Cookie": "sessionid=lrqk2nf3v9k3dqgn82x17nb9ed8eftbe"
    }
    body = {
        "mobile": "1234567899",
        "text": query + """credentials: {
        "type": "service_account",
        "project_id": "ca-dev-01-426608",
        "private_key_id": "3c732eb1344124b35f34a1be0bf728cef6d181b0",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC5UeYc06G2Tw2U\n30ndwzPv6/QBqqtZIIdRd9EtbsSNd3nmZLiGP9GjnNtjiDmegk49goVlz8P1vE+M\nT3e4BwH2g9Tc08fhPYrRy6Jnca7BTyVR33vdidWzRcrjsSs1utK1KTeX6hXHYCJR\npXHc0XWUauG0TXGHpzZ41OxyERk9oUAdYBFoUZyZFeHmcJp7rWXKRx1OJFBhqm1T\nHr1ZCuwmQ2dfc9iyRagT6PwWRRRtY8UA19noIrda5IrcsbrURcTzGo7VjOPSqdvq\nzYjUDHDTlzXI98I8wb/vBNrjVlWYyL0DEXtD0eQfLZYtF8XQoyTwUQjrPVCaUffC\n1HnIeupnAgMBAAECggEALNOLKmjkonEf02VpfCtmCkBUXvzWArKUGNg3MFqtT5zZ\nTyoI2mxgfMeJ59sBOP7DByzlsJlfiLbatRFZ35lOV79Ow3W00R5uUE4GBCijAV5w\nJAw/bXiUSQ92QrpNverpYenM6UG1r+rokkBHOQcvfk2WN+NNtWb0jajPYs4RAW9w\nouar/7B5Uo/0DjOoK0Hg5fjdgOAw4+0DnvQYAp9ZZBf3TrYaTbh8z9cx+RxKMO5m\n5urL4299a5mxiyYmCOzTDLpDg2JXFo/ZT7TTW5YduLJRzfgc+fZIxzJWxZY2bNF8\niJHQy3D0GPyiB9NFZ4cjiXQt80+A1eWH439VG60ncQKBgQDq5PtIbq8PRlqVfpf1\ngrUkX6hYza2fialNSBGEhSbVXKhOmxY3JM+iGvMYoGQeTX598k/sgy4y9qn9rdCD\nYtUqPjo0yXI/YATMOazLthrxyzok2MAf56Ks30fephtvJnoWObn+Cgqo8P6Y4vF1\nIgBH4N2QQOUrbqKraDOV/iIJ0QKBgQDJ+JvWkyFkptKK+NHAPcVwyqc88bycciOL\ntU5FLZeXck6uj6YyHsF8ilD+0d3W/ntqlEGu0FCXn5UB0BUwUf4BFu1hR5MdCHV4\n/V9hEd9bJySDRplV7lRgxSks2TZYlALoWZohMnunYPniMUiahJ/LT64BJdPRqIq7\ni+98EvsGtwKBgQDHcKa/CGORJ54wAm3J4jIlcScCR5ictgjO+lsNVvTzAhpRq7KA\nHbxCGnm/tidr50Z4b65W1cb7NJ5/Kv65H8h4dp97RHPBxagtMuc5jCRymqiCsprm\nPAnOmEJwlD8E7/mHN3ppbWNBsGWrsD1tw/HTFeVp3v/2EZkCypXKTB3gkQKBgGHB\nGmw4uijlNXJeC+dn/nAhJeCxgACYneu4zTFeZ8i9YqfKjz4i9LM6nwk2upCci0+C\ngmgCG3/HlW9TL247wRz14975rZKXzYPJ3qg05k5QG7QOL5kPyXcs9kjmuQ8WVHHx\nLFB1BrR0k32PLPzcxBq7bhTQIj2PvdYYXMlIxobxAoGBALCP+lITnLtc+2BPOalU\no9MN2uobE3GMwEPLNIVsm/8dHSQZ36yNa3CfULH7hrTyTNyIQ/MQ8su0HJwMmfh6\n4WHuzDTNHU3ssnc0sDJdKjXrD2FZ5kDfemsIxA8vnAhYc7/+fd2q6BDRXHtASX1x\nVfNk6sZJm0KvB+DKn1Qxn+Pk\n-----END PRIVATE KEY-----\n",
        "client_email": "kl-bigquery@ca-dev-01-426608.iam.gserviceaccount.com",
        "client_id": "100210303134810182483",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/kl-bigquery%40ca-dev-01-426608.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
        }"""
        ,
        "session_id": "i11",
        "client_identifier": "insights-5"
    }
    print("body:\n", body)
    try:
        response = requests.post(url, headers=headers, data=body, timeout=40)
        time.sleep(10)
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        return response.text
    except Exception as e:
        print(f"Exception occurred: {e}")
        print(traceback.format_exc())
        return str(e)
    
def my_account_chat_tool(query: str = "how can you help me?") -> str:
    """
    Tool to interact with the Kindlife.in customer support chatbot.

    Args:
        query (str): The user's question or request about Kindlife.in services.
            Examples:
            - "Tell me about your clean beauty products"
            - "How do I track my order?"
            - "What are the current promotions?"
            - "Tell me about the Superkind Club"
            - "How can I join the Kind Champion Program?"

    Returns:
        str: The chatbot's response text, or an error message if the request fails.
        The response will provide helpful information about Kindlife.in's products,
        services, and support options.

    Description:
        This function sends a POST request to the Kindlife.in customer support chatbot
        API endpoint. It handles queries about:
        1. Product Information (clean beauty, healthy snacks, wellness essentials)
        2. Order Support (tracking, order details, issue resolution)
        3. Promotions and Discounts (sales, discounts, Kinders loyalty program)
        4. Membership Programs (Superkind Club, Kind Champion Program)
        5. Community and Resources (community engagement, clean beauty and wellness resources)
    """
    url = "https://portal.demo.cygnusalpha.one/api/v1/api-controller/invoke-service/my-account-chat/"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Bearer kl-my-acc-c398e977-a645-4429-8543-16290ce51d4a",
        "Cookie": "sessionid=lrqk2nf3v9k3dqgn82x17nb9ed8eftbe"
    }
    body = {
        "mobile": "1234567899",
        "text": query,
        "session_id": "i11",
        "client_identifier": "insights-5"
    }
    print("body:\n", body)
    try:
        response = requests.post(url, headers=headers, data=body, timeout=40)
        time.sleep(10)
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        return response.text
    except Exception as e:
        print(f"Exception occurred: {e}")
        print(traceback.format_exc())
        return str(e)

if __name__ == "__main__":
    kindlife__bizz_chat()