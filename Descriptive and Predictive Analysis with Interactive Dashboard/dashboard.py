import pandas as pd
import numpy as np
import plotly.express as px
from datetime import timedelta
from dash import Dash, dcc, html, Input, Output, callback_context
from sklearn.linear_model import Ridge

DATA_PATH = "../data/us_supermarket.csv"

# Load data
raw = pd.read_csv(DATA_PATH, encoding="latin-1")
raw.columns = [c.strip().replace(" ", "_") for c in raw.columns]

# Identify date column
date_col_candidates = ["Order_Date", "Date"]
for c in date_col_candidates:
    if c in raw.columns:
        date_col = c
        break
else:
    raise ValueError("Order Date column not found.")

raw[date_col] = pd.to_datetime(raw[date_col], errors="coerce")
raw = raw.dropna(subset=[date_col])

raw["Sales"] = pd.to_numeric(raw.get("Sales", 0), errors="coerce").fillna(0.0)
raw["City"] = raw.get("City", "Unknown").astype(str)
raw["Region"] = raw.get("Region", "Unknown").astype(str)
raw["Category"] = raw.get("Category", "Unknown").astype(str)
raw["Sub-Category"] = raw.get("Sub-Category", raw.get("Sub_Category", "Unknown")).astype(str)

payment_col = "Payment" if "Payment" in raw.columns else None

# Prepare daily sales for forecast
raw["Date"] = raw[date_col].dt.date
daily = raw.groupby("Date", as_index=False)["Sales"].sum()
daily["Date"] = pd.to_datetime(daily["Date"])

def add_time_features(df, date_col="Date"):
    out = df.copy()
    out["t"] = (out[date_col] - out[date_col].min()).dt.days
    out["dow"] = out[date_col].dt.dayofweek
    out["month"] = out[date_col].dt.month
    out["dow_sin"] = np.sin(2*np.pi*out["dow"]/7)
    out["dow_cos"] = np.cos(2*np.pi*out["dow"]/7)
    out["mon_sin"] = np.sin(2*np.pi*out["month"]/12)
    out["mon_cos"] = np.cos(2*np.pi*out["month"]/12)
    return out

features = ["t", "dow_sin", "dow_cos", "mon_sin", "mon_cos"]
dtrain = add_time_features(daily, "Date")
model = Ridge(alpha=1.0)
model.fit(dtrain[features], dtrain["Sales"])

horizon = 30
last_date = dtrain["Date"].max()
future_dates = pd.date_range(last_date + timedelta(days=1), periods=horizon, freq="D")
future_df = pd.DataFrame({"Date": future_dates})
future_feat = add_time_features(future_df, "Date")
future_df["Predicted_Sales"] = model.predict(future_feat[features])

app = Dash(__name__)
app.title = "US Supermarket Dashboard"

cities = sorted(raw["City"].dropna().unique().tolist())
products = sorted(raw["Sub-Category"].dropna().unique().tolist())

app.layout = html.Div([
    html.H2("US Supermarket Sales — Descriptive & Predictive Dashboard"),

    html.Div([
        dcc.DatePickerRange(
            id="date-range",
            min_date_allowed=daily["Date"].min(),
            max_date_allowed=daily["Date"].max(),
            start_date=daily["Date"].min(),
            end_date=daily["Date"].max(),
            display_format="YYYY-MM-DD",
        ),
        dcc.Dropdown(options=[{"label": c, "value": c} for c in cities],
                     multi=True, id="city-dd", placeholder="Filter by City"),
        dcc.Dropdown(options=[{"label": p, "value": p} for p in products],
                     multi=True, id="prod-dd", placeholder="Filter by Sub-Category"),
    ], style={"display": "grid", "gridTemplateColumns": "1fr 1fr 1fr", "gap": "12px"}),

    html.Div([dcc.Graph(id="g_trend")]),
    html.Div([
        dcc.Graph(id="g_product"),
        dcc.Graph(id="g_city"),
        dcc.Graph(id="g_dist"),
    ], style={"display": "grid", "gridTemplateColumns": "1fr 1fr 1fr", "gap": "10px"}),
    html.Div([dcc.Graph(id="g_forecast")])
])

def apply_filters(df, start_date, end_date, cities_sel, prods_sel):
    dff = df.copy()
    if start_date:
        dff = dff[dff[date_col] >= pd.to_datetime(start_date)]
    if end_date:
        dff = dff[dff[date_col] <= pd.to_datetime(end_date)]
    if cities_sel:
        dff = dff[dff["City"].isin(cities_sel)]
    if prods_sel:
        dff = dff[dff["Sub-Category"].isin(prods_sel)]
    return dff

@app.callback(
    [Output("g_trend", "figure"),
     Output("g_product", "figure"),
     Output("g_city", "figure"),
     Output("g_dist", "figure")],
    [Input("date-range", "start_date"),
     Input("date-range", "end_date"),
     Input("city-dd", "value"),
     Input("prod-dd", "value")]
)
def render_descriptive(sdate, edate, cities_sel, prods_sel):
    dff = apply_filters(raw, sdate, edate, cities_sel, prods_sel)

    dff["Date"] = dff[date_col].dt.date
    trend_df = dff.groupby("Date", as_index=False)["Sales"].sum()
    trend_df["Date"] = pd.to_datetime(trend_df["Date"])
    fig_trend = px.line(trend_df, x="Date", y="Sales", title="Daily Sales Trend")

    prod_df = dff.groupby("Sub-Category", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False).head(15)
    fig_product = px.bar(prod_df, x="Sub-Category", y="Sales", title="Sales by Sub-Category")

    city_df = dff.groupby("City", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False).head(15)
    fig_city = px.bar(city_df, x="City", y="Sales", title="Sales by City")

    if payment_col:
        pay_df = dff.groupby(payment_col, as_index=False)["Sales"].sum()
        fig_dist = px.pie(pay_df, names=payment_col, values="Sales", title="Sales by Payment Method")
    else:
        hist_df = dff.copy()
        hist_df["Discount"] = pd.to_numeric(hist_df.get("Discount", 0), errors="coerce").fillna(0)
        fig_dist = px.histogram(hist_df, x="Discount", nbins=30, title="Discount Distribution")

    return fig_trend, fig_product, fig_city, fig_dist

@app.callback(
    Output("g_forecast", "figure"),
    [Input("date-range", "start_date"),
     Input("date-range", "end_date")]
)
def render_forecast(sdate, edate):
    hist = daily.copy()
    if sdate and edate:
        hist = hist[(hist["Date"] >= pd.to_datetime(sdate)) & (hist["Date"] <= pd.to_datetime(edate))]

    hist["Type"] = "Actual"
    fc = future_df.rename(columns={"Predicted_Sales": "Sales"}).copy()
    fc["Type"] = "Forecast"
    combined = pd.concat([hist[["Date", "Sales", "Type"]], fc[["Date", "Sales", "Type"]]], ignore_index=True)
    fig_fc = px.line(combined, x="Date", y="Sales", color="Type", title="Sales Forecast (Next 30 Days)")
    return fig_fc

if __name__ == "__main__":
    app.run(debug=True)
