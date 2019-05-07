import dash
import dash_bootstrap_components as dbc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets,)
server = app.server
app.config.suppress_callback_exceptions = True

#app.config.update({
#    # as the proxy server will remove the prefix
#    'routes_pathname_prefix': '/dashboard/',
#
#    # the front-end will prefix this string to the requests
#    # that are made to the proxy server
#    'requests_pathname_prefix': '/dashboard/'
#})
