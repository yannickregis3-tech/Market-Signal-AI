from app.core.config import Settings
from app.data_engine.factory import build_provider_registry


def test_deriv_provider_is_not_enabled_without_verified_symbol_map():
    config = Settings(deriv_symbol_map_json="{}")
    registry = build_provider_registry(config)
    assert registry.names() == ()


def test_deriv_provider_is_registered_only_with_explicit_symbol_mapping():
    config = Settings(deriv_symbol_map_json='{"DERIV_VOL10":"R_10"}')
    registry = build_provider_registry(config)
    assert registry.names() == ("deriv",)
    assert registry.get("deriv").name == "deriv"


def test_invalid_deriv_symbol_map_json_is_rejected():
    config = Settings(deriv_symbol_map_json="not-json")
    try:
        config.deriv_symbol_map
    except ValueError as exc:
        assert "valid JSON" in str(exc)
    else:
        raise AssertionError("Invalid JSON must be rejected.")
