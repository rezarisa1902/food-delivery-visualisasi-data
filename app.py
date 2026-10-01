from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from data_processing import WEEKDAYS_ID, clean_data, load_raw_data


ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "synthetic_fooddelivery_dataset.csv"
COLORS = {
    "green": "#1f6b57",
    "lime": "#d7e7a8",
    "coral": "#e66e56",
    "gold": "#e8b64e",
    "ink": "#20352f",
    "muted": "#6d7d77",
    "grid": "#e7ece8",
}

st.set_page_config(
    page_title="Food Delivery | Data to Insight",
    page_icon="🍜",
    layout="wide",
    initial_sidebar_state="auto",
)

title_column, theme_control = st.columns([5, 2], vertical_alignment="center")
with title_column:
    st.markdown("# Data to Insight · Food Delivery")
    st.caption(
        "Analisis operasional pesanan, waktu pengiriman, harga, dan pengalaman pelanggan "
        "· Dataset sintetis, Januari–Desember 2024"
    )
with theme_control:
        display_theme = st.segmented_control(
                "Tampilan",
                options=["Light", "Dark", "System"],
                default="System",
                label_visibility="collapsed",
                key="display_theme",
        )

if display_theme == "Dark":
        theme_css = """
        :root {
            color-scheme: dark;
            --app-bg: #141c19;
            --panel-bg: #1d2924;
            --sidebar-bg: #18231f;
            --app-text: #e5eee9;
            --muted-text: #a5b6ae;
            --grid-color: #3b4a43;
            --border-color: #3b4a43;
            --metric-accent: #72b69d;
            --selected-bg: #1f6b57;
            --toolbar-icon-filter: brightness(0) invert(1);
        }
        """
elif display_theme == "Light":
        theme_css = """
        :root {
            color-scheme: light;
            --app-bg: #ffffff;
            --panel-bg: #f1f5ef;
            --sidebar-bg: #f1f5ef;
            --app-text: #20352f;
            --muted-text: #6d7d77;
            --grid-color: #e7ece8;
            --border-color: #dce5dd;
            --metric-accent: #1f6b57;
            --selected-bg: #1f6b57;
            --toolbar-icon-filter: none;
        }
        """
else:
        theme_css = """
        :root {
            color-scheme: light dark;
            --app-bg: #ffffff;
            --panel-bg: #f1f5ef;
            --sidebar-bg: #f1f5ef;
            --app-text: #20352f;
            --muted-text: #6d7d77;
            --grid-color: #e7ece8;
            --border-color: #dce5dd;
            --metric-accent: #1f6b57;
            --selected-bg: #1f6b57;
            --toolbar-icon-filter: none;
        }
        @media (prefers-color-scheme: dark) {
            :root {
                --app-bg: #141c19;
                --panel-bg: #1d2924;
                --sidebar-bg: #18231f;
                --app-text: #e5eee9;
                --muted-text: #a5b6ae;
                --grid-color: #3b4a43;
                --border-color: #3b4a43;
                --metric-accent: #72b69d;
                --selected-bg: #1f6b57;
                --toolbar-icon-filter: brightness(0) invert(1);
            }
        }
        """

st.markdown(
        f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
        {theme_css}
        html, body, [data-testid="stAppViewContainer"] {{
            background: var(--app-bg) !important;
            color: var(--app-text) !important;
            font-family: 'DM Sans', sans-serif;
        }}
        [data-testid="stHeader"] {{ background: var(--app-bg); }}
        [data-testid="stMain"] {{ background: var(--app-bg); }}
        [data-testid="stSidebar"] {{ background: var(--sidebar-bg); }}
        [data-testid="stHeader"] button,
        [data-testid="stHeader"] a {{
            color: var(--app-text) !important;
            opacity: 1 !important;
            filter: none !important;
        }}
        [data-testid="stToolbarActions"] button *,
        [data-testid="stToolbarActions"] a *,
        [data-testid="stMainMenuButton"] * {{
            color: var(--app-text) !important;
            opacity: 1 !important;
        }}
        [data-testid="stHeader"] svg {{
            color: var(--app-text) !important;
            filter: var(--toolbar-icon-filter) !important;
            opacity: 1 !important;
        }}
        [data-testid="stHeader"] button:hover,
        [data-testid="stHeader"] a:hover {{
            background: var(--panel-bg) !important;
            border-radius: 6px;
        }}
        h1, h2, h3, p, label, [data-testid="stMarkdownContainer"] {{ color: var(--app-text); }}
        h1, h2, h3 {{ font-family: 'Manrope', sans-serif; letter-spacing: 0; }}
        h1 {{ font-size: 2.15rem !important; line-height: 1.2; }}
        .block-container {{ padding-top: 4rem; padding-bottom: 3rem; max-width: 1440px; }}
        [data-testid="stMetric"] {{ background: var(--panel-bg); padding: 16px 18px; border-radius: 6px; border-left: 3px solid var(--metric-accent); }}
        [data-testid="stMetricLabel"], [data-testid="stCaptionContainer"] {{ color: var(--muted-text) !important; }}
        div[data-testid="stExpander"] {{ border-color: var(--border-color); }}
        [data-variant="segmented_control"] {{
            background: var(--panel-bg) !important;
            color: var(--muted-text) !important;
            border-color: var(--border-color) !important;
        }}
        [data-variant="segmented_control"][aria-checked="true"] {{
            background: var(--selected-bg) !important;
            color: #ffffff !important;
        }}
        [data-variant="segmented_control"][aria-checked="true"] * {{ color: #ffffff !important; }}
        [data-baseweb="select"] > div, [data-baseweb="input"] > div {{
            background: var(--panel-bg);
            color: var(--app-text);
            border-color: var(--border-color);
        }}
        [data-testid="stDateInputField"],
        [data-testid="stMultiSelect"] > div [role="group"],
        [data-testid="stSelectbox"] [role="group"] {{
            background: var(--panel-bg) !important;
            color: var(--app-text) !important;
            border-color: var(--border-color) !important;
        }}
        [data-testid="stDateInputField"] input {{
            background: var(--panel-bg) !important;
            color: var(--app-text) !important;
        }}
        [data-testid="stDateInputField"] *,
        [data-testid="stSelectbox"] [role="group"] * {{ color: var(--app-text) !important; }}
        [data-testid="stMultiSelect"] [role="group"] * {{ color: var(--app-text) !important; }}
        [data-testid="stMultiSelect"] [data-tag],
        [data-testid="stMultiSelect"] [data-tag] * {{ color: #ffffff !important; }}
        [data-baseweb="tag"] {{ background: var(--selected-bg); color: #ffffff; }}
        [role="listbox"], [role="option"], [role="dialog"] {{
            background: var(--panel-bg);
            color: var(--app-text);
        }}
        [data-testid="stDataFrame"] {{ border-color: var(--border-color); }}
        .js-plotly-plot .plotly text {{ fill: var(--app-text) !important; }}
        .js-plotly-plot .plotly .xgrid, .js-plotly-plot .plotly .ygrid {{ stroke: var(--grid-color); }}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner="Membaca dan membersihkan data...")
def get_data(path: str) -> pd.DataFrame:
    return clean_data(load_raw_data(path))


def apply_plot_style(fig: go.Figure, dark_mode: bool) -> go.Figure:
    text_color = "#e5eee9" if dark_mode else COLORS["ink"]
    grid_color = "#3b4a43" if dark_mode else COLORS["grid"]
    fig.update_layout(
        margin=dict(l=12, r=12, t=28, b=12),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans, sans-serif", color=text_color),
        legend_title_text="",
    )
    fig.update_xaxes(showgrid=False, linecolor=grid_color, tickfont_color=text_color, title_font_color=text_color)
    fig.update_yaxes(gridcolor=grid_color, zeroline=False, tickfont_color=text_color, title_font_color=text_color)
    return fig


dark_charts = display_theme == "Dark"


if not DATA_PATH.exists():
    st.error(f"Dataset tidak ditemukan: {DATA_PATH.name}")
    st.stop()

data = get_data(str(DATA_PATH))
valid_dates = data["Waktu_Transaksi"].dropna()
if valid_dates.empty:
    st.error("Tidak ada timestamp yang dapat dibaca dari dataset.")
    st.stop()

st.sidebar.markdown("## Filter Analisis")
date_range = st.sidebar.date_input(
    "Rentang tanggal",
    value=(valid_dates.min().date(), valid_dates.max().date()),
    min_value=valid_dates.min().date(),
    max_value=valid_dates.max().date(),
)
categories = st.sidebar.multiselect(
    "Kategori menu",
    options=sorted(data["Kategori_Menu"].dropna().unique()),
    default=sorted(data["Kategori_Menu"].dropna().unique()),
)
statuses = st.sidebar.multiselect(
    "Status pesanan",
    options=sorted(data["Status_Pesanan"].dropna().unique()),
    default=sorted(data["Status_Pesanan"].dropna().unique()),
)
promo_filter = st.sidebar.selectbox(
    "Promo",
    options=["Semua", "Dengan promo", "Tanpa promo"],
)

if isinstance(date_range, tuple):
    start_date, end_date = date_range
else:
    start_date = end_date = date_range

filtered = data.loc[
    data["Waktu_Transaksi"].notna()
    & data["Waktu_Transaksi"].dt.date.between(start_date, end_date)
    & data["Kategori_Menu"].isin(categories)
    & data["Status_Pesanan"].isin(statuses)
].copy()
if promo_filter == "Dengan promo":
    filtered = filtered.loc[filtered["Status_Promo"].eq(True)]
elif promo_filter == "Tanpa promo":
    filtered = filtered.loc[filtered["Status_Promo"].eq(False)]

st.divider()

if filtered.empty:
    st.warning("Tidak ada pesanan untuk kombinasi filter ini.")
    st.stop()

completed = filtered.loc[filtered["Status_Pesanan"].eq("Selesai")]
financial = completed.loc[~completed["Anomali_Sumber_Kaggle"]]
average_wait = filtered["Waktu_Tunggu_Menit"].mean()
average_rating = filtered["Rating_Pelanggan"].mean()
completion_rate = filtered["Status_Pesanan"].eq("Selesai").mean() * 100
revenue = financial["Harga_Pesanan"].sum()

metric_columns = st.columns(4)
metric_columns[0].metric("Total pesanan", f"{len(filtered):,}".replace(",", "."))
metric_columns[1].metric("Pesanan selesai", f"{completion_rate:.1f}%")
metric_columns[2].metric("Rata-rata tunggu", f"{average_wait:.1f} menit" if pd.notna(average_wait) else "—")
metric_columns[3].metric("Rata-rata rating", f"{average_rating:.2f} / 5" if pd.notna(average_rating) else "—")
st.caption(
    f"Nilai pesanan selesai yang lolos pemeriksaan harga: Rp{revenue:,.0f}".replace(",", ".")
    + ". "
    "KPI memakai aturan sumber: harga nol atau di atas Rp500.000 tidak dihitung."
)

left, right = st.columns(2)
with left:
    st.subheader("1 · Apakah jumlah pesanan berubah dari bulan ke bulan?")
    monthly = filtered.groupby("Bulan", as_index=False).size().rename(columns={"size": "Jumlah Pesanan"})
    monthly = monthly.sort_values("Bulan")
    figure = px.line(
        monthly,
        x="Bulan",
        y="Jumlah Pesanan",
        markers=True,
        color_discrete_sequence=[COLORS["green"]],
    )
    st.plotly_chart(apply_plot_style(figure, dark_charts), width="stretch")

with right:
    st.subheader("2 · Kategori mana yang paling banyak dipesan?")
    by_category = (
        filtered.groupby("Kategori_Menu", as_index=False)
        .size()
        .rename(columns={"size": "Jumlah Pesanan"})
        .sort_values("Jumlah Pesanan")
    )
    figure = px.bar(
        by_category,
        x="Jumlah Pesanan",
        y="Kategori_Menu",
        orientation="h",
        color="Jumlah Pesanan",
        color_continuous_scale=[COLORS["lime"], COLORS["green"]],
    )
    figure.update_layout(coloraxis_showscale=False)
    st.plotly_chart(apply_plot_style(figure, dark_charts), width="stretch")

left, right = st.columns(2)
with left:
    st.subheader("3 · Bagaimana sebaran waktu tunggu tiap kategori?")
    figure = px.box(
        filtered.dropna(subset=["Waktu_Tunggu_Menit"]),
        x="Kategori_Menu",
        y="Waktu_Tunggu_Menit",
        color="Kategori_Menu",
        color_discrete_sequence=[COLORS["green"], COLORS["coral"], COLORS["gold"], "#6e9bb5"],
        points="outliers",
    )
    figure.update_layout(showlegend=False)
    figure.update_yaxes(title="Waktu tunggu (menit)")
    st.plotly_chart(apply_plot_style(figure, dark_charts), width="stretch")

with right:
    st.subheader("4 · Apakah jarak kirim berkaitan dengan waktu tunggu?")
    figure = px.scatter(
        filtered.dropna(subset=["Jarak_Kirim_KM", "Waktu_Tunggu_Menit"]),
        x="Jarak_Kirim_KM",
        y="Waktu_Tunggu_Menit",
        color="Kategori_Menu",
        hover_data=["ID_Pesanan", "Status_Pesanan"],
        color_discrete_sequence=[COLORS["green"], COLORS["coral"], COLORS["gold"], "#6e9bb5"],
        opacity=0.65,
    )
    figure.update_xaxes(title="Jarak kirim (km)")
    figure.update_yaxes(title="Waktu tunggu (menit)")
    st.plotly_chart(apply_plot_style(figure, dark_charts), width="stretch")

left, right = st.columns(2)
with left:
    st.subheader("5 · Bagaimana distribusi rating pelanggan?")
    ratings = filtered.dropna(subset=["Rating_Pelanggan"])
    figure = px.histogram(
        ratings,
        x="Rating_Pelanggan",
        nbins=5,
        histfunc="count",
        color_discrete_sequence=[COLORS["coral"]],
    )
    figure.update_xaxes(title="Rating (1–5)", dtick=1)
    figure.update_yaxes(title="Jumlah rating")
    st.plotly_chart(apply_plot_style(figure, dark_charts), width="stretch")

with right:
    st.subheader("6 · Kapan waktu tunggu rata-rata paling tinggi?")
    heat_data = filtered.dropna(subset=["Hari", "Jam", "Waktu_Tunggu_Menit"])
    heatmap = heat_data.pivot_table(
        index="Hari",
        columns="Jam",
        values="Waktu_Tunggu_Menit",
        aggfunc="mean",
    ).reindex(WEEKDAYS_ID)
    figure = px.imshow(
        heatmap,
        labels={"x": "Jam transaksi", "y": "Hari", "color": "Menit"},
        color_continuous_scale=["#edf3e8", COLORS["gold"], COLORS["coral"]],
        aspect="auto",
    )
    st.plotly_chart(apply_plot_style(figure, dark_charts), width="stretch")

with st.expander("Kualitas data dan hasil cleaning"):
    quality_columns = st.columns(4)
    quality_columns[0].metric("Baris dipertahankan", f"{len(data):,}".replace(",", "."))
    quality_columns[1].metric("Timestamp gagal", f"{data['Waktu_Transaksi'].isna().sum():,}")
    quality_columns[2].metric("Jarak kosong", f"{data['Jarak_Kirim_KM'].isna().sum():,}")
    quality_columns[3].metric("Anomali sumber", f"{data['Anomali_Sumber_Kaggle'].sum():,}")
    st.write(
        "Nilai kosong rating dan ulasan tidak diimputasi. Baris dengan jarak kosong tetap "
        "dipakai untuk analisis lain, tetapi otomatis tidak muncul pada scatter plot jarak. "
        "Harga anomali menurut aturan sumber dipertahankan untuk audit dan dikecualikan dari total nilai pesanan. "
        "Kandidat outlier IQR tersedia sebagai pembanding statistik."
    )
    missing_table = (
        data.isna().sum().rename("Jumlah kosong").to_frame().query("`Jumlah kosong` > 0")
    )
    st.dataframe(missing_table, width="stretch")

st.download_button(
    "Unduh data hasil cleaning (CSV)",
    data=data.to_csv(index=False).encode("utf-8-sig"),
    file_name="food_delivery_cleaned.csv",
    mime="text/csv",
)
st.caption("Sumber: synthetic_fooddelivery_dataset.csv · Seluruh hasil menggambarkan data simulasi, bukan transaksi nyata.")