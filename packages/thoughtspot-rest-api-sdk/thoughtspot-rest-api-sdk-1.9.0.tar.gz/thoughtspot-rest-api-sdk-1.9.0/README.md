
# Getting Started with RESTAPI SDK

## Install the Rest API SDK

You must have Python 3 >=3.7, <= 3.9 installed on your system to use this SDK. This SDK package depends on other Python packages like nose, jsonpickle etc. These dependencies are defined in the requirements.txt file that comes with the SDK. To resolve these dependencies, you can use the PIP Dependency manager. Install it by following steps at https://pip.pypa.io/en/stable/installing/.

Python and PIP executables should be defined in your PATH. Open command prompt and type pip --version. This should display the version of the PIP Dependency Manager installed if your installation was successful and the paths are properly defined.

To install the dependencies create requirements.txt with content thoughtspot-rest-api-sdk, run the command `echo thoughtspot-rest-api-sdk > requirements.txt`. Next, run the command `pip install -r requirements.txt`. This should install all the required dependencies.

To install the SDK, run the command `pip install thoughtspot-rest-api-sdk` at the command line.

## Initialize the API Client

**_Note:_** Documentation for the client can be found [here.](https://github.com/thoughtspot/rest-api-sdk/blob/main/Python/doc/client.md)

The following parameters are configurable for the API Client:

| Parameter | Type | Description |
|  --- | --- | --- |
| `content_type` | `string` | body content type for post request<br>*Default*: `'application/json'` |
| `accept_language` | `string` | response format<br>*Default*: `'application/json'` |
| `access_token` | `string` | The OAuth 2.0 Access Token to use for API requests. |
| `base_url` | `string` | *Default*: `'https://localhost:443'` |
| `environment` | Environment | The API environment. <br> **Default: `Environment.PRODUCTION`** |
| `http_client_instance` | `HttpClient` | The Http Client passed from the sdk user for making requests |
| `override_http_client_configuration` | `bool` | The value which determines to override properties of the passed Http Client from the sdk user |
| `timeout` | `float` | The value to use for connection timeout. <br> **Default: 60** |
| `max_retries` | `int` | The number of times to retry an endpoint call if it fails. <br> **Default: 0** |
| `backoff_factor` | `float` | A backoff factor to apply between attempts after the second try. <br> **Default: 2** |
| `retry_statuses` | `Array of int` | The http statuses on which retry is to be done. <br> **Default: [408, 413, 429, 500, 502, 503, 504, 521, 522, 524, 408, 413, 429, 500, 502, 503, 504, 521, 522, 524]** |
| `retry_methods` | `Array of string` | The http methods on which retry is to be done. <br> **Default: ['GET', 'PUT', 'GET', 'PUT']** |

The API client can be initialized as follows:

```python
from restapisdk.restapisdk_client import RestapisdkClient
from restapisdk.configuration import Environment

client = RestapisdkClient(
    content_type='application/json',
    accept_language='application/json',
    access_token='AccessToken',
    environment=Environment.PRODUCTION,
    base_url = 'https://localhost:443',)
```

## Authorization

This API uses `OAuth 2 Bearer token`.

## Guide
[API Reference](https://github.com/thoughtspot/rest-api-sdk/blob/main/Python/doc/README.md)

## Live Playground
We recommend that you browse through the [code playground](https://try-everywhere.thoughtspot.cloud/v2/#/everywhere/api/rest/playgroundV2) before you start constructing your API requests. The playground offers an interactive portal with comprehensive information about the API endpoints, request and response workflows.
