# Contributing Guidelines

Thank you for your interest in contributing to Instapaper Bookmark Organizer!

## How to Contribute

### Bug Reports

If you find a bug, please create an Issue with the following information:

- Brief description of the problem
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment information (Python version, OS, etc.)

### Feature Requests

New feature proposals are welcome! Create an Issue including:

- Feature description
- Use cases
- Implementation ideas, if possible

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Create a Pull Request

#### Coding Conventions

- Follow PEP 8 style guide
- Use type hints (Python 3.7+)
- Add docstrings
- Maintain consistency with existing code style

#### Commit Messages

- Write clear and concise messages
- Use present tense ("Add feature" not "Added feature")
- Include detailed description if necessary

## Development Environment Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/instapaper-bookmark-organizer.git
cd instapaper-bookmark-organizer

# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Install development packages (optional)
uv add --dev black flake8 mypy pytest
```

## Testing

When making changes, please verify functionality:

```bash
# Basic functionality check
uv run python main.py

# Code style checks (optional)
uv run flake8 main.py
uv run black --check main.py
uv run mypy main.py
```

## Questions

If you have questions, feel free to create an Issue!

## Code of Conduct

- Be respectful
- Provide constructive feedback
- Maintain an open and inclusive community

Thank you for your cooperation!
