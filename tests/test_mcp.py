from adapters.mcp import MCPAdapter
from hac.engine import HACEngine
from hac.models import ActionType
from scenarios.common import base_state


def test_mcp_normalizes_tool_request():
    adapter = MCPAdapter(HACEngine(base_state()))
    action = adapter.normalize({"id": "m1", "agent_id": "agent-a", "tool": "read_resource", "arguments": {"resource": "repo"}})
    assert action.action_type == ActionType.READ_RESOURCE


def test_mcp_authorizes_safe_request():
    adapter = MCPAdapter(HACEngine(base_state()))
    decision = adapter.authorize_tool_request({"id": "m1", "agent_id": "agent-a", "tool": "read_resource", "arguments": {"resource": "repo"}})
    assert decision.allowed


def test_mcp_malformed_request_fails_closed():
    adapter = MCPAdapter(HACEngine(base_state()))
    decision = adapter.authorize_tool_request({"id": "m1", "agent_id": "agent-a", "arguments": {"resource": "repo"}})
    assert not decision.allowed