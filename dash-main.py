import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

from analyzer import TokenSwapAnalyzer
import get_transaction_data

# Initialize app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
server = app.server
app.title = "DeFi Tools"

analyzer = TokenSwapAnalyzer()

# Layout for Token Risk Analyzer
def token_analyzer_layout():
    return dbc.Container([
        html.H2("🔍 DeFi Token Risk Analyzer", className="my-4"),
        html.P("Enter two token names (e.g., bitcoin, ethereum) and generate a risk report."),
        dbc.Input(id="from-token", placeholder="Token we are converting from", value="bitcoin", className="mb-2"),
        dbc.Input(id="to-token", placeholder="Token we are converting to", value="ethereum", className="mb-2"),
        dbc.Button("Generate Report", id="generate-button", color="primary", className="mb-3"),
        html.Div(id="report-status", className="text-info mb-2"),
        html.Pre(id="report-output", style={"whiteSpace": "pre-wrap"})
    ])

# Layout for Ethereum Transaction Viewer
def transaction_viewer_layout():
    txs = get_transaction_data.get_transaction_data()
    tx_items = []

    for tx in txs[:10]:  # show top 10
        tx_items.append(dbc.Card([
            dbc.CardBody([
                html.H5(f"From: {tx['from']} → To: {tx['to']}"),
                html.P(f"Value: {int(tx['value']) / 1e18:.5f} ETH"),
                html.P(f"Gas Used: {tx['gasUsed']}"),
                html.P(f"Status: {'✅ Success' if tx['isError'] == '0' else '❌ Fail'}")
            ])
        ], className="mb-3"))

    return dbc.Container([
        html.H2("📡 Ethereum Transaction Viewer", className="my-4"),
        *tx_items
    ])

# Main layout with navigation
app.layout = dbc.Container([
    dbc.NavbarSimple(
        brand="🧠 DeFi Intelligence Suite",
        color="primary",
        dark=True,
        className="mb-4"
    ),
    dcc.Tabs(id="tabs", value="analyzer", children=[
        dcc.Tab(label="Token Risk Analyzer", value="analyzer"),
        dcc.Tab(label="Transaction Viewer", value="transactions"),
    ]),
    html.Div(id="tab-content", className="p-4")
], fluid=True)

# Callbacks for rendering tab content
@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "value")
)
def render_tab(tab):
    if tab == "analyzer":
        return token_analyzer_layout()
    elif tab == "transactions":
        return transaction_viewer_layout()

# Callback for generating report
@app.callback(
    Output("report-status", "children"),
    Output("report-output", "children"),
    Input("generate-button", "n_clicks"),
    State("from-token", "value"),
    State("to-token", "value"),
    prevent_initial_call=True
)
def generate_report(n_clicks, from_token, to_token):
    status = "🔄 Writing report..."
    report = analyzer.compare_tokens(from_token, to_token)
    return "", report

if __name__ == "__main__":
    app.run(debug=True)

