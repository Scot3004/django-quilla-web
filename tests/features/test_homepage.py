"""Test de homepage usando Playwright (reemplazo de ScreenPy/Selenium)."""

from ..helpers.osano import mock_osano
from playwright.sync_api import expect



def test_homepage_title(page):
    """Verificamos que en homepage se pueda ver Python Barranquilla usando Playwright.

    Navegamos a la raíz `/` y confiamos en que `pytest-playwright` haya
    configurado `base_url` para resolverla automáticamente.
    """
    mock_osano(page)
    page.goto("/")
    # guardar captura de pantalla similar a SaveScreenshot
    page.screenshot(path="screenshots/homepage.png", full_page=True)
    expect(page).to_have_title("Python Barranquilla")
    expect(page.get_by_role("heading", level=1)).to_have_text("Python Barranquilla.")
