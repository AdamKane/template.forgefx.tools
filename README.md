# SlackAPI 

SlackAPI is our in-house Python-based wrapper for the official Slack API, providing an easy-to-use interface for developers to interact with Slack's features.

## Core Features!
- Bookmark management (add, update, delete, list)
- Message sending to specific channels
- Channel administration (create, invite users, archive/delete)
- Channel search by bookmark.link URL across all channels

## Technology Stack
- Python
- FastAPI for REST API framework
- Python Slack SDK
- Python Slack SDK API 
- JSON for data serialization

## Technology Statck Documentation
- Python Slack SDK Manual (See: https://slack.dev/python-slack-sdk/)
- Python Slack SDK API (slack_sdk) (See: https://slack.dev/python-slack-sdk/api-docs/slack_sdk/)

## Architecture
- REST API built with FastAPI and Python
- Bot token authentication using slack-sdk
- JSON response format
- Support latest Slack API version only
- `slack_wrapper.py`: All slack-related code in the SlackAPI class
- `slack_wrapper_tests.py`: All slack-related tests

## Setup and Running
- Install dependencies: `pip install -r requirements.txt`
- Run the application: `uvicorn main:app --reload`

## Testing
- To run tests, simply run `pytest` from the command line. (or use Ctrl+Shift+T)

## Contributing
- We DO NOT use mocks or mock-based testing
- Always use pytest for testing (never use unittest)

## Next Steps







