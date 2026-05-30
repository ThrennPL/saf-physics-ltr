from tools.route_model import select_model


def test_route_model_smoke_default() -> None:
    config = {
        "default": "low-cost",
        "agent_overrides": {},
        "escalation_rules": [],
    }
    assert select_model(config, agent="any-agent", gate=None, risk=None) == "low-cost"
