# Earnings Calculation API

This project is an API that calculates earnings for couriers based on their activity logs. It's built using FastAPI, a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.

## Requirements

- Python 3.10.7
- FastAPI 0.68.1
- Uvicorn 0.15.0
- Pydantic 1.9.0
- HTTPX 0.21.0

For testing:

- pytest 7.4.4
- pytest-cov 3.0.0
- iso8601 0.1.16
- requests

## Installation

1. Clone the repository.
2. Install the requirements using pip: `pip install -r requirements.txt`
3. Run the application: `uvicorn main:app --reload`

## Usage

The API endpoint is at `/earnings/{tier}` where `{tier}` is one of the rate card IDs such as `silver_tier`. The body of the POST request should be an activity log.

## Testing

Unit tests are located in the `tests` directory. You can run them using pytest: `pytest`

## Contributing

Contributions are welcome. Please submit a pull request.

## License

MIT
