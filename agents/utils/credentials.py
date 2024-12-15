import os
import sys
import platform
import keyring
import getpass
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

class CredentialStore(ABC):
    """Abstract base class for credential storage implementations."""

    @abstractmethod
    def get(self, service: str, username: str) -> Optional[str]:
        """Get a credential from storage."""
        pass

    @abstractmethod
    def set(self, service: str, username: str, credential: str) -> None:
        """Store a credential."""
        pass

    @abstractmethod
    def delete(self, service: str, username: str) -> None:
        """Delete a credential."""
        pass

class WindowsCredentialStore(CredentialStore):
    """Windows Credential Manager implementation."""

    def get(self, service: str, username: str) -> Optional[str]:
        try:
            import win32cred
            target = f"{service}:{username}"
            cred = win32cred.CredRead(target, win32cred.CRED_TYPE_GENERIC)
            return cred['CredentialBlob'].decode('utf-16')
        except ImportError:
            return keyring.get_password(service, username)
        except Exception:
            return None

    def set(self, service: str, username: str, credential: str) -> None:
        try:
            import win32cred
            target = f"{service}:{username}"
            credential_blob = credential.encode('utf-16')
            cred = {
                'Type': win32cred.CRED_TYPE_GENERIC,
                'TargetName': target,
                'UserName': username,
                'CredentialBlob': credential_blob,
                'Comment': "Stored by AI Agents Credential Manager",
                'Persist': win32cred.CRED_PERSIST_LOCAL_MACHINE
            }
            win32cred.CredWrite(cred, 0)
        except ImportError:
            keyring.set_password(service, username, credential)

    def delete(self, service: str, username: str) -> None:
        try:
            import win32cred
            target = f"{service}:{username}"
            win32cred.CredDelete(target, win32cred.CRED_TYPE_GENERIC)
        except ImportError:
            try:
                keyring.delete_password(service, username)
            except keyring.errors.PasswordDeleteError:
                pass

class MacOSKeychainStore(CredentialStore):
    """macOS Keychain implementation."""

    def get(self, service: str, username: str) -> Optional[str]:
        return keyring.get_password(service, username)

    def set(self, service: str, username: str, credential: str) -> None:
        keyring.set_password(service, username, credential)

    def delete(self, service: str, username: str) -> None:
        try:
            keyring.delete_password(service, username)
        except keyring.errors.PasswordDeleteError:
            pass

class LinuxSecretStore(CredentialStore):
    """Linux Secret Service implementation."""

    def __init__(self):
        try:
            import secretstorage
            self.using_secretstorage = True
        except ImportError:
            self.using_secretstorage = False

    def get(self, service: str, username: str) -> Optional[str]:
        if self.using_secretstorage:
            try:
                import secretstorage
                connection = secretstorage.dbus_init()
                collection = secretstorage.get_default_collection(connection)
                items = collection.search_items({'service': service, 'username': username})
                item = next(items, None)
                return item.get_secret().decode('utf-8') if item else None
            except Exception:
                return keyring.get_password(service, username)
        return keyring.get_password(service, username)

    def set(self, service: str, username: str, credential: str) -> None:
        if self.using_secretstorage:
            try:
                import secretstorage
                connection = secretstorage.dbus_init()
                collection = secretstorage.get_default_collection(connection)
                collection.create_item(
                    f"{service} credential",
                    {'service': service, 'username': username},
                    credential.encode('utf-8'),
                    replace=True
                )
                return
            except Exception:
                pass
        keyring.set_password(service, username, credential)

    def delete(self, service: str, username: str) -> None:
        if self.using_secretstorage:
            try:
                import secretstorage
                connection = secretstorage.dbus_init()
                collection = secretstorage.get_default_collection(connection)
                items = collection.search_items({'service': service, 'username': username})
                for item in items:
                    item.delete()
                return
            except Exception:
                pass
        try:
            keyring.delete_password(service, username)
        except keyring.errors.PasswordDeleteError:
            pass

class Credentials:
    """Modern credential manager for AI agents."""

    # Service names
    OLLAMA = "ai_agents_ollama"
    OPENAI = "ai_agents_openai"
    JIRA = "ai_agents_jira"

    def __init__(self):
        """Initialize with appropriate storage backend based on OS."""
        system = platform.system().lower()

        if system == 'windows':
            self._store = WindowsCredentialStore()
        elif system == 'darwin':
            self._store = MacOSKeychainStore()
        elif system == 'linux':
            self._store = LinuxSecretStore()
        else:
            # Fallback to keyring for unknown systems
            self._store = MacOSKeychainStore()

        self._username = getpass.getuser()

    def get(self, service: str, username: Optional[str] = None) -> Optional[str]:
        """Get a credential."""
        return self._store.get(service, username or self._username)

    def set(self, service: str, credential: str, username: Optional[str] = None) -> None:
        """Set a credential."""
        self._store.set(service, username or self._username, credential)

    def delete(self, service: str, username: Optional[str] = None) -> None:
        """Delete a credential."""
        self._store.delete(service, username or self._username)

    # Convenience methods
    def get_ollama(self) -> Optional[str]:
        """Get Ollama API key."""
        return self.get(self.OLLAMA)

    def set_ollama(self, api_key: str) -> None:
        """Set Ollama API key."""
        self.set(self.OLLAMA, api_key)

    def get_openai(self) -> Optional[str]:
        """Get OpenAI API key."""
        return self.get(self.OPENAI)

    def set_openai(self, api_key: str) -> None:
        """Set OpenAI API key."""
        self.set(self.OPENAI, api_key)

    def get_jira(self) -> Optional[str]:
        """Get JIRA token."""
        return self.get(self.JIRA)

    def set_jira(self, token: str) -> None:
        """Set JIRA token."""
        self.set(self.JIRA, token)