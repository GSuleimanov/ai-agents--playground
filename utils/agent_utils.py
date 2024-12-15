from utils import config
from phi.storage.agent.sqlite import SqlAgentStorage


def parameters(name: str):
    """Boilerplate configuration for agents, which are:
    - model
    - storage
    - instructions
    - prettyname
    - name
    """
    model_config = config.get_model_config()
    storage_config = config.get_storage_config()
    agent_config = config.get_agent_config(name)

    # Configure the model based on provider
    provider = model_config.get('provider', 'ollama')
    model_params = {
        'id': model_config.get('name'),
        'temperature': model_config.get('temperature', 0.7),
        'stream': model_config.get('stream', True)
    }

    match provider:
        case 'ollama':
            from phi.model.ollama import Ollama
            model = Ollama(**model_params)
        case 'openai':
            from phi.model.openai import OpenAI
            model = OpenAI(**model_params)
        case _:
            raise ValueError(f"Unsupported model provider: {provider}")

    # Configure storage
    if storage_config.get('type') == 'sqlite':
        storage = SqlAgentStorage(
            table_name=agent_config.get('name'),
            db_file=storage_config.get('db_file', 'agents/history.db')
        )
    else:
        raise ValueError(f"Unsupported storage type: {storage_config.get('type')}")

    return {
        'instructions': agent_config.get('instructions'),
        'prettyname': agent_config.get('prettyname'),
        'name': agent_config.get('name'),
        'storage': storage,
        'model': model
    }
