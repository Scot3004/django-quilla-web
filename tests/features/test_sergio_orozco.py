"""Test de homepage usando Playwright (reemplazo de ScreenPy/Selenium)."""

from ..helpers.osano import mock_osano
from playwright.sync_api import expect

def test_homepage_title(page):
    """
    Verificar el perfil de Sergio Orozco
    """
    mock_osano(page)
    page.goto("/")
    page.get_by_role("link", name="NOSOTROS").click()
    page.get_by_text("Sergio Orozco").click()
    expect(page.get_by_role("heading", name="Sergio Orozco")).to_be_visible()
    expect(page.get_by_role("heading", name="Organizador")).to_be_visible()
    expect(page.get_by_role("heading", name="Contribuciones")).to_be_visible()
    expect(page.get_by_role("heading", name="Proyectos que organiza")).to_be_visible()
    expect(page.get_by_role("heading", name="Charlas")).to_be_visible()
