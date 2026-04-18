# Autonomous Business Intelligence Skill

## Overview
A nanobot skill for generating strategic business intelligence insights using web search and intelligent analysis.

## Features
- Automated insight generation on business and technology topics
- Configurable web search and topic selection
- Log rotation for efficient log management
- Flexible dependency injection for testing
- Markdown-formatted insight reports

## Installation

### Prerequisites
- Python 3.9+
- nanobot framework

### Setup
```bash
# Clone the repository
git clone https://github.com/steeveroucaute10-epping/nanobot-abi-skill.git

# Install dependencies
pip install -e .
```

## Usage

### Basic Usage
```python
from nanobot_abi_skill.skill import AutonomousBusinessIntelligenceSkill

# Generate insights with default topics
skill = AutonomousBusinessIntelligenceSkill()
insights = skill.generate_insights()

# Generate insights with custom topics
custom_topics = [
    "AI in Healthcare",
    "Blockchain Technology Trends"
]
insights = skill.generate_insights(topics=custom_topics)
```

### Logging Configuration
```python
# Customize log rotation
skill = AutonomousBusinessIntelligenceSkill(
    log_dir='/path/to/logs',
    max_log_size_bytes=2 * 1024 * 1024,  # 2 MB
    backup_count=10  # Keep 10 backup log files
)
```

## Configuration Options

### `AutonomousBusinessIntelligenceSkill` Parameters
- `insights_dir`: Directory to store generated insights
- `log_dir`: Directory to store log files
- `log_level`: Logging level (default: `logging.INFO`)
- `max_log_size_bytes`: Maximum log file size before rotation (default: 1 MB)
- `backup_count`: Number of backup log files to keep (default: 5)

## Development

### Running Tests
```bash
python -m unittest discover tests
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Logging
- Log files are rotated to prevent unlimited growth
- Configurable log size and backup file count
- Logs include detailed information about insight generation process

## License
(To be added - choose an appropriate open-source license)

## Contact
Maintainer: Steeve Roucaute
GitHub: @steeveroucaute10-epping