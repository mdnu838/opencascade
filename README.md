# OpenCascade

**Free Multi-Source GenAI Orchestration Library**

OpenCascade is a Python library that automatically selects, routes, and combines outputs from free GenAI models and API providers. It creates a unified interface for discovering, connecting, and using open-access models across the AI ecosystem — including OpenRouter, HuggingFace, Together AI, Mistral, Ollama, LM Studio, and other publicly available sources.

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Code Coverage](https://img.shields.io/badge/coverage-90%25%2B-brightgreen)](docs/TESTING_STRATEGY.md)

---

## 🌟 Features

Smart Model Selector is a unified interface for discovering, connecting, and using open-access models across the AI ecosystem. It automatically selects, routes, and combines outputs from free GenAI models and API providers.

## Features

- **Automatic Provider Discovery**
  - Maintains updated list of free GenAI model providers
  - Automatic metadata updates from central registry
  - Focus on free and open-source endpoints

- **Task Auto-Classification**
  - Intelligent query analysis for task classification
  - Supports: chat, code, tts, audio, embeddings, image
  - Lightweight local classifier with manual override options

- **Model Auto-Selection**
  - Smart model selection based on capability metadata
  - Response quality tracking
  - Latency and uptime monitoring
  - Transparent selection reasoning

- **Multi-Model Routing**
  - Parallel query processing across multiple models
  - Configurable response combination methods
  - Support for text and embeddings (multimodal planned)

- **Offline & Local Fallback**
  - Local model hosting support via Ollama, LM Studio
  - Bundled lightweight open models
  - Hardware-aware automatic mode switching
  - Configurable fallback settings

## Project Structure

```
smart_model_selector/
├── core/               # Core functionality
│   ├── selector.py     # Model selection logic
│   ├── router.py      # Query routing
│   └── combiner.py    # Response combination
├── providers/         # Provider implementations
│   ├── base.py       # Base provider interface
│   ├── openrouter.py # OpenRouter integration
│   ├── huggingface.py # HuggingFace integration
│   └── ollama.py     # Ollama integration
├── classifier/        # Task classification
│   ├── classifier.py # Main classifier
│   └── models.py     # Classification models
└── utils/            # Utility functions
    ├── config.py     # Configuration management
    ├── security.py   # Security utilities
    └── logging.py    # Logging utilities
```

## Installation

```bash
pip install smart-model-selector
# or
uv pip install smart-model-selector
```

## Quick Start

```python
from smart_model_selector import ModelSelector

# Initialize the selector
selector = ModelSelector()

# Auto-select and use the best model for a task
response = selector.process("Write a Python function to sort a list")

# Use multiple models and combine responses
responses = selector.process_multi(
    "Explain quantum computing",
    num_models=3,
    combination_method="summarize"
)
```

## Development

1. Clone the repository
2. Set up the development environment:
```bash
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

## Contributing

Contributions are welcome! Please read our contributing guidelines and code of conduct.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
