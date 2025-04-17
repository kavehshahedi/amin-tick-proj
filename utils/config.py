"""
Configuration module for TicketAssist application.

This module handles loading configuration from environment variables,
Docker secrets, and provides a unified interface for accessing configuration
throughout the application.
"""
import os
from pathlib import Path
from typing import Any, Dict, Optional, Union
import logging

logger = logging.getLogger(__name__)


class AppConfig:
    """
    Application configuration manager.
    
    Handles loading and accessing configuration from environment variables
    and Docker secrets.
    """
    
    # Default configurations
    DEFAULTS = {
        "REPLICATE_API_TOKEN": "",
        "STREAMLIT_AUTH_USER": "admin",
        "STREAMLIT_AUTH_PASSWORD": "admin",
        "LLM_MODEL": "llama3.1:8b",
        "LLM_TEMPERATURE": 0.1,
        "LLM_MAX_TOKENS": 512,
        "LLM_TOP_P": 0.9,
        "APP_TITLE": "TicketAssist",
        "DEBUG_MODE": False,
        "OLLAMA_API_HOST": "http://localhost:11434",
    }
    
    def __init__(self) -> None:
        """Initialize the application config from environment and secrets."""
        self._config = self.DEFAULTS.copy()
        self._load_from_environment()
        self._load_from_secrets()
        
        # Log configuration (excluding sensitive values)
        self._log_configuration()
    
    def _load_from_environment(self) -> None:
        """Load configuration from environment variables."""
        for key in self._config.keys():
            env_value = os.environ.get(key)
            if env_value is not None:
                # Convert environment variable values to appropriate types
                if isinstance(self._config[key], bool):
                    self._config[key] = env_value.lower() in ('true', 'yes', '1')
                elif isinstance(self._config[key], int):
                    try:
                        self._config[key] = int(env_value)
                    except ValueError:
                        logger.warning(f"Could not convert {key}={env_value} to int, using default")
                elif isinstance(self._config[key], float):
                    try:
                        self._config[key] = float(env_value)
                    except ValueError:
                        logger.warning(f"Could not convert {key}={env_value} to float, using default")
                else:
                    self._config[key] = env_value
    
    def _load_from_secrets(self) -> None:
        """Load configuration from Docker secrets."""
        secrets_dir = Path('/run/secrets')
        if not secrets_dir.exists():
            return
        
        # Mapping of secret files to config keys (lowercase secret name to uppercase config key)
        secret_mapping = {
            'replicate_api_token': 'REPLICATE_API_TOKEN',
            'streamlit_auth_user': 'STREAMLIT_AUTH_USER',
            'streamlit_auth_password': 'STREAMLIT_AUTH_PASSWORD',
        }
        
        for secret_file, config_key in secret_mapping.items():
            secret_path = secrets_dir / secret_file
            if secret_path.exists():
                try:
                    self._config[config_key] = secret_path.read_text().strip()
                    logger.info(f"Loaded configuration for {config_key} from Docker secret")
                except Exception as e:
                    logger.error(f"Error reading secret {secret_file}: {e}")
    
    def _log_configuration(self) -> None:
        """Log the current configuration (excluding sensitive data)."""
        safe_config = {k: '********' if 'TOKEN' in k or 'PASSWORD' in k else v 
                       for k, v in self._config.items()}
        logger.info(f"Application configuration: {safe_config}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key: The configuration key
            default: Default value if key doesn't exist
            
        Returns:
            The configuration value or default
        """
        return self._config.get(key, default)
    
    def __getitem__(self, key: str) -> Any:
        """
        Get a configuration value using dictionary syntax.
        
        Args:
            key: The configuration key
            
        Returns:
            The configuration value
            
        Raises:
            KeyError: If the key doesn't exist
        """
        return self._config[key]
    
    def as_dict(self) -> Dict[str, Any]:
        """
        Get the complete configuration as a dictionary.
        
        Returns:
            Configuration dictionary
        """
        return self._config.copy()


# Create a singleton instance
config = AppConfig()