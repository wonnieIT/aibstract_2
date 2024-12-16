import dash_bootstrap_components as dbc
from dash import html

navbar = dbc.NavbarSimple(
    [
        dbc.NavItem(
            dbc.NavLink(
                html.Img(
                    src="assets/github-mark-white.png",
                    alt="Source Code",
                    id="github-logo",
                ),
                href="https://github.com/wonnieIT/aibstract_2.git",
                target="_blank",
                className="p-1",
            )
        ),
        dbc.NavItem(
            dbc.NavLink(
                dbc.Button(
                    html.Span(
                        "info",
                        className="material-symbols-outlined d-flex nav-span",
                    ),
                    color="dark",
                    id="page-info-btn",
                    n_clicks=0,
                )
            )
        ),
    ],
    #brand="Kakaogames Store Aibstract",
    brand=html.Span(
        "Kakaogames Store Aibstract",
        style={"color": "#f0c33cw"}  
    ),
    brand_href="https://www.kakaogamescorp.com/",
    id="navbar",
    color = "black",
    #color="#f0c33c",
    dark=True
)
