# URL Shortener Project

## Description
This project is a Django web application for shortening URLs using a REST API.

## Installation
1. Clone the repository.
2. Install the required dependencies using `pip install -r requirements.txt`.

## Usage
1. Run the Django development server using `python manage.py runserver`.
2. Access the API endpoints to shorten URLs and retrieve the original URLs.

### API Endpoints
- Shorten URL:
  - Endpoint: `/shorten/`
  - Method: POST
  - Request Body: 
    ```json
    {
      "original_url": "http://example.com"
    }
    ```
  - Example curl command:
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"original_url": "http://example.com"}' https://slackurlshortner-fd74f723a2da.herokuapp.com/shorten/
    ```

- Redirect to URL:
  - Endpoint: `/redir/<short_code>/`
  - Method: GET
  - Example curl command:
    ```bash
    curl https://slackurlshortner-fd74f723a2da.herokuapp.com/redir/<short_code>/
    ```

## Testing
1. Run the test cases using `python manage.py test`.

## License
This project is licensed under the MIT License - see the LICENSE file for details.