from pathlib import Path
from typing import Dict, Any
import yaml

class Config:
    """Configuration manager for AI agents."""

    def __init__(self):
        self._root_dir = Path(__file__).parent.parent
        self._global_config = self._load_yaml(self._root_dir / 'config.yaml')
        self._agents_config = {}
        for config_path in self._root_dir.rglob('config.yaml'):
            config_data = self._load_yaml(config_path)
            if 'name' in config_data:
                self._agents_config[config_data['name']] = config_data

    def _load_yaml(self, path: Path) -> Dict[str, Any]:
        """Load a YAML configuration file."""
        try:
            with open(path, 'r') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Warning: Could not load config from {path}: {e}")
            return {}

    def _get_agent_config(self, agent_name: str) -> Dict[str, Any]:
        """Get or load agent-specific configuration."""

        if agent_name not in self._agents_config:
            agent_config_path = self._root_dir / 'agents' / agent_name / 'config.yaml'
            self._agents_config[agent_name] = self._load_yaml(agent_config_path)
        return self._agents_config[agent_name]

    def get_model_config(self) -> Dict[str, Any]:
        """Get combined model configuration."""
        global_model = self._global_config.get('model', {})
        agents_model = self._agents_config.get('model', {})
        return {**global_model, **agents_model}  # agents-config overrides global config

    def get_storage_config(self) -> Dict[str, Any]:
        """Get combined storage configuration."""
        global_storage = self._global_config.get('storage', {})
        agents_storage = self._agents_config.get('storage', {})
        return {**global_storage, **agents_storage}

    def get_agent_config(self, agent_name: str) -> Dict[str, Any]:
        """
        Get combined configuration for a specific agent.
        Merges global config with agent-specific config.
        """
        agent_config = self._get_agent_config(agent_name)
        return {
            'name': agent_config.get('name', agent_name),
            'prettyname': agent_config.get('prettyname', agent_name),
            'instructions': agent_config.get('instructions', '').split('\n'),
            'model': self.get_model_config(),
            'storage': self.get_storage_config()
        }

# Create a singleton instance
config = Config()

# Export the instance methods directly
get_model_config = config.get_model_config
get_storage_config = config.get_storage_config
get_agent_config = config.get_agent_config