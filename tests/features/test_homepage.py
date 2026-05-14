"""Test de homepage usando Playwright (reemplazo de ScreenPy/Selenium)."""

def test_homepage_title(page):
    """Verificamos que en homepage se pueda ver Python Barranquilla usando Playwright.

    Navegamos a la raíz `/` y confiamos en que `pytest-playwright` haya
    configurado `base_url` para resolverla automáticamente.
    """
    page.goto("/")
    # guardar captura de pantalla similar a SaveScreenshot
    page.screenshot(path="screenshots/homepage.png", full_page=True)
    assert page.title() == "Python Barranquilla"
    assert page.get_by_role("heading", level=1).inner_text().strip() == "Python Barranquilla."
