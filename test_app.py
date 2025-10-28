import pytest
from unittest.mock import patch
import pandas as pd

# -------------------------
# Fixture for dummy data
# -------------------------
@pytest.fixture
def dummy_df():
    return pd.DataFrame({
        "date": pd.date_range("2025-01-01", periods=3),
        "region": ["north", "south", "all"],
        "sales": [100, 200, 300]
    })


# -------------------------
# Fixture to patch CSV load and create app
# -------------------------
@pytest.fixture
def patched_app(dummy_df):
    with patch("app.pd.read_csv", return_value=dummy_df):
        # Re-import app after patching so it uses dummy data
        import app as patched
        yield patched.app


# -------------------------
# Test that key elements exist
# -------------------------
@pytest.mark.parametrize("element_id", ["h1", "#region-selector", "#visualization"])
def test_element_exists(dash_duo, patched_app, element_id):
    dash_duo.start_server(patched_app)

    if element_id == "#visualization":
        # Wait for the inner SVG to appear (Plotly renders charts as <svg>)
        dash_duo.wait_for_element("#visualization .main-svg", timeout=10)
        element = dash_duo.find_element("#visualization")
    else:
        element = dash_duo.wait_for_element(element_id, timeout=10)

    assert element.is_displayed()


# -------------------------
# Test that the graph is rendered
# -------------------------
def test_graph_rendered_fast(dash_duo, patched_app):
    dash_duo.start_server(patched_app)

    # Wait for the Graph component
    graph_div = dash_duo.wait_for_element("#visualization", timeout=10)

    # Wait for the inner SVG to appear (Plotly renders charts as <svg>)
    svg = dash_duo.wait_for_element("#visualization .main-svg", timeout=10)

    # Assert the SVG exists, meaning the chart rendered
    assert svg.is_displayed()
