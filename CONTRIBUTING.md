# Contributing to NetworkScanner

Thank you for considering contributing to the NetworkScanner project! This document provides guidelines for contributions.

## How to Contribute

1. **Fork the Repository**: Create your own fork of the repository
2. **Create a Branch**: Make your changes in a new branch
3. **Submit a Pull Request**: Once your changes are ready, submit a pull request

## Development Setup

### Prerequisites

- Python 3.6 or higher
- Git

### Local Development

```bash
# Clone the repository
git clone https://github.com/arminmarth/NetworkScanner.git
cd NetworkScanner

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt

# Run the tests
python -m unittest discover tests
```

## Coding Standards

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use meaningful variable and function names
- Add docstrings for all functions, classes, and modules
- Include type hints where appropriate
- Write unit tests for new functionality

## Testing

Before submitting a pull request, please:

1. Run the existing test suite to ensure you haven't broken anything
2. Add tests for any new functionality
3. Ensure all tests pass

## Pull Request Process

1. Update the README.md with details of changes if applicable
2. Update documentation for any new features or changes
3. Add or update tests as necessary
4. Your pull request will be merged once it has been reviewed and approved

## Code of Conduct

- Be respectful and inclusive in all communications
- Focus on constructive feedback
- Respect the original author's design decisions

## Questions?

If you have questions about contributing, please open an issue in the repository.

Thank you for your contributions!
