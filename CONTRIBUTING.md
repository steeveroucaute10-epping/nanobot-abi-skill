# Contributing to Autonomous Business Intelligence Skill

## Welcome Contributors!

We appreciate your interest in contributing to the Autonomous Business Intelligence Skill for nanobot.

## Development Setup

### Prerequisites
- Python 3.9+
- Git
- Virtual environment tool (venv/conda)

### Local Setup
1. Clone the repository
```bash
git clone https://github.com/steeveroucaute10-epping/nanobot-abi-skill.git
cd nanobot-abi-skill
```

2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install development dependencies
```bash
pip install -e .[test]
```

## Contribution Guidelines

### Reporting Issues
- Use GitHub Issues
- Provide a clear description
- Include reproduction steps
- Specify your environment details

### Pull Request Process
1. Fork the repository
2. Create a feature branch
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes
4. Write or update tests
5. Ensure all tests pass
   ```bash
   python -m unittest discover tests
   ```
6. Update documentation if needed
7. Commit with a clear, descriptive message
8. Push to your fork
9. Create a Pull Request

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for all functions
- Maintain high test coverage

### Testing
- Write unit tests for new functionality
- Ensure 100% test coverage for new code
- Use mock objects for external dependencies

## Code of Conduct
- Be respectful
- Collaborate constructively
- Welcome diverse perspectives

## Questions?
Open an issue or contact the maintainer directly.

## Thank You!
Your contributions help improve this skill for everyone.