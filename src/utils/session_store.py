import uuid
from typing import Dict, Any

class SessionStore:
    _instance = None
    _store: Dict[str, Dict[str, Any]] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SessionStore, cls).__new__(cls)
        return cls._instance

    def create_session(self, data: Dict[str, Any]) -> str:
        session_id = str(uuid.uuid4())
        self._store[session_id] = data
        return session_id

    def get_session(self, session_id: str) -> Dict[str, Any]:
        return self._store.get(session_id, {})

    def update_session(self, session_id: str, data: Dict[str, Any]):
        if session_id in self._store:
            self._store[session_id].update(data)

    def session_exists(self, session_id: str) -> bool:
        return session_id in self._store

# Singleton instance
session_store = SessionStore()
