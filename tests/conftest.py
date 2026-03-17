import pytest
from unittest.mock import patch

# Socket emit mock
class SocketEmitMock:
    def __init__(self):
        self.emissions = []
    
    def __call__(self, user_id, event, data):
        self.emissions.append({
            'user_id': user_id,
            'event': event,
            'data': data
        })
    
    def clear(self):
        self.emissions = []
    
    def get_emissions_for_user(self, user_id):
        return [e for e in self.emissions if e['user_id'] == user_id]
    
    def get_emissions_by_event(self, event):
        return [e for e in self.emissions if e['event'] == event]


@pytest.fixture
def mock_socket_emit():
    """Create a mock for WebSocket emit function."""
    mock = SocketEmitMock()
    with patch('app.matches.set_socket_emit') as mock_set_emit:
        mock_set_emit.side_effect = lambda func: None
    with patch('app.matches.socket_emit', mock):
        yield mock


@pytest.fixture
def mock_socket_emit_direct():
    """Direct mock that patches socket_emit in matches module."""
    mock = SocketEmitMock()
    with patch('app.matches.socket_emit', mock):
        yield mock
