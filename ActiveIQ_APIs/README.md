# ActiveIQ API Examples

This folder contains example Python scripts for interacting with the NetApp ActiveIQ API.

## Getting Started

### Prerequisites

- Python 3.x
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [requests](https://pypi.org/project/requests/)

Install dependencies:
```bash
pip install python-dotenv requests

```markdown
# ActiveIQ API Examples

This folder contains example Python scripts for interacting with the NetApp ActiveIQ API.

## Getting Started

### Prerequisites

- Python 3.x
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [requests](https://pypi.org/project/requests/)

Install dependencies:
```bash
pip install python-dotenv requests
```

### API Token

1. Obtain an API token from NetApp ActiveIQ.
2. Create a `.env` file in this directory with the following content:
   ```
   AIQ_API_ACCESS_TOKEN=your_api_token_here
   ```

### Usage

Run the example script:
```bash
python aiq_api_example.py
```

The script will attempt to connect to the ActiveIQ API and list customers accessible to your token.

### Notes

- **Do not commit your `.env` file or API tokens to version control.**


## References

- [NetApp ActiveIQ API Documentation](https://api.activeiq.netapp.com/docs/)
```
