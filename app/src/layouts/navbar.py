import dash_bootstrap_components as dbc
from src.layouts import emotion_during_class,overall,student,compare_gg

layout = dbc.NavbarSimple(
    children=[
        dbc.DropdownMenu(
            nav=True,
            in_navbar=True,
            label='Emotion',
            children = [
                dbc.NavItem(dbc.NavLink("Emotion during class",href=emotion_during_class.__name__.split('.')[-1])),
                #dbc.NavItem(dbc.NavLink("Overall class stats", href=overall.__name__.split('.')[-1])),
                dbc.NavItem(dbc.NavLink("Student", href=student.__name__.split('.')[-1])),
                dbc.NavItem(dbc.NavLink("Compare Google", href=compare_gg.__name__.split('.')[-1])),
            ]
    )],
    brand="Kidtopi",
    brand_href="#",
    sticky="top",
)

