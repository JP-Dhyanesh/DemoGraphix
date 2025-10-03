import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------- Load & preprocess data -------------------
@st.cache_data
def load_data():
    # Load CSVs
    population = pd.read_csv("population.csv")
    migration = pd.read_csv("migration.csv")

    # ------------------- Population -------------------
    population = population.drop(columns=["Indicator Name", "Indicator Code"])
    population_long = population.melt(
        id_vars=["Country Name", "Country Code"],
        var_name="Year",
        value_name="Population"
    )
    population_long.rename(columns={"Country Name": "Country"}, inplace=True)
    population_long["Year"] = population_long["Year"].astype(int)
    population_long["Population"] = pd.to_numeric(population_long["Population"], errors='coerce')
    population_long = population_long.dropna(subset=["Population"])

    # ------------------- Migration -------------------
    migration = migration.drop(columns=["Indicator Name", "Indicator Code"])
    migration_long = migration.melt(
        id_vars=["Country Name", "Country Code"],
        var_name="Year",
        value_name="NetMigration"
    )
    migration_long.rename(columns={"Country Name": "Country"}, inplace=True)
    migration_long["Year"] = migration_long["Year"].astype(int)
    migration_long["NetMigration"] = pd.to_numeric(migration_long["NetMigration"], errors='coerce')
    migration_long = migration_long.dropna(subset=["NetMigration"])

    # ------------------- Merge -------------------
    df = pd.merge(population_long, migration_long, on=["Country", "Year"], how="inner")

    # Calculate Population Growth Rate
    df["PopGrowthRate"] = df.groupby("Country")["Population"].pct_change() * 100

    return df

df = load_data()

# ------------------- Page setup -------------------
st.set_page_config(page_title="DemoGraphix 🌍", layout="wide")
st.title("🌍 DemoGraphix")
st.caption("Explore Population Growth & Migration Trends Across the World")

# ------------------- Sidebar filters -------------------
st.sidebar.title("🔎 Filters")

years = st.sidebar.slider(
    "Select Year Range",
    int(df["Year"].min()),
    int(df["Year"].max()),
    (2000, 2020)
)

country_select = st.sidebar.selectbox(
    "Select a Country",
    sorted(df["Country"].unique())
)

# Filter data based on selections
df_filtered = df[(df["Year"] >= years[0]) & (df["Year"] <= years[1])]
country_data = df_filtered[df_filtered["Country"] == country_select]

# ------------------- Key Metrics -------------------
st.markdown("### 📊 Key Metrics")
col1, col2, col3 = st.columns(3)

latest_year = years[1]
latest_data = df_filtered[df_filtered["Year"] == latest_year]

col1.metric("🌐 Total World Population", f"{int(latest_data['Population'].sum()):,}")
top_growth_country = latest_data.sort_values("PopGrowthRate", ascending=False).iloc[0]
col2.metric("🚀 Highest Growth Country", top_growth_country["Country"], f"{top_growth_country['PopGrowthRate']:.2f}%")
top_migration_country = latest_data.sort_values("NetMigration", ascending=False).iloc[0]
col3.metric("🧳 Highest Net Migration", top_migration_country["Country"], f"{int(top_migration_country['NetMigration']):,}")

# ------------------- World Population Map -------------------
st.markdown("### 🌏 World Population Map")

map_data = latest_data.copy()
fig_map = px.choropleth(
    map_data,
    locations="Country",
    locationmode="country names",
    color="Population",
    hover_name="Country",
    hover_data={"Population": True, "NetMigration": True, "PopGrowthRate": True},
    color_continuous_scale="viridis",
    title=f"World Population ({latest_year})"
)
st.plotly_chart(fig_map, use_container_width=True)

# ------------------- Tabs for Visualizations -------------------
tab1, tab2, tab3 = st.tabs(["📈 Population Growth", "📊 Migration Flows", "⚖️ Growth vs Migration"])

with tab1:
    fig = px.line(
        country_data,
        x="Year",
        y="Population",
        title=f"{country_select} Population Growth ({years[0]}-{years[1]})",
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    top_migration = latest_data.sort_values("NetMigration", ascending=False).head(10)
    fig = px.bar(
        top_migration,
        x="NetMigration",
        y="Country",
        orientation="h",
        title=f"Top 10 Migration Inflows ({latest_year})",
        text="NetMigration"
    )
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    fig = px.scatter(
        latest_data,
        x="PopGrowthRate",
        y="NetMigration",
        size="Population",
        hover_name="Country",
        title=f"Population Growth vs Net Migration ({latest_year})",
        size_max=60
    )
    st.plotly_chart(fig, use_container_width=True)

# ------------------- Download Filtered Data -------------------
st.sidebar.download_button(
    label="📥 Download Filtered Data as CSV",
    data=df_filtered.to_csv(index=False).encode("utf-8"),
    file_name="filtered_population_migration.csv",
    mime="text/csv"
)
