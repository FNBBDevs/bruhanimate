from bruhanimate.bruheffect.registry import effect_registry


def test_registry_not_empty():
    """Ensure the registry is populated with effects."""
    assert len(effect_registry.names()) > 0


def test_registry_contains_standard_effects():
    """Verify that common effects are registered."""
    expected_effects = ["static", "noise", "stars", "plasma", "snow"]
    names = effect_registry.names()
    for effect in expected_effects:
        assert effect in names


def test_registry_get_valid_effect():
    """Test getting an entry for a known effect."""
    entry = effect_registry.get("static")
    assert entry.name == "static"
    assert entry.effect_cls is not None


def test_registry_get_invalid_effect():
    """Test that a KeyError is raised for unknown effects."""
    import pytest

    with pytest.raises(KeyError):
        effect_registry.get("non_existent_effect_xyz")


def test_registry_presets():
    """Test retrieving presets for an effect."""
    presets = effect_registry.presets("noise")
    assert isinstance(presets, dict)
    assert "sparse" in presets
