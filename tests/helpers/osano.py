from playwright.sync_api import Page


def mock_osano(page: Page, domain: str = "pybaq.co") -> None:
    """Mockea Osano evitando que el banner interfiera en los tests.

    - Intercepta peticiones al CDN de Osano y devuelve un script stub.
    - Inyecta un script de inicialización que simula consentimiento.
    - Añade una cookie indicadora de consentimiento (opcional).

    Llama este helper antes de `page.goto(...)`.
    """

    # Interceptar y devolver un script vacío/estub para el CDN de Osano
    page.route("**/cmp.osano.com/**", lambda route: route.fulfill(
        status=200,
        content_type="application/javascript",
        body="window.__osano_mocked = true;",
    ))

    # Inyectar un script de inicialización que deje el objeto Osano benigno
    page.add_init_script(
        """
        // Stub minimal de Osano para tests
        window.Osano = window.Osano || {};
        window.Osano.consent = window.Osano.consent || { accepted: true };
        window.__osano_mocked = true;
        """
    )

    # Añadir cookie de consentimiento (útil si la app lee cookies)
    page.context.add_cookies([
        {"name": "osano_consent", "value": "accepted", "domain": domain, "path": "/"}
    ])

