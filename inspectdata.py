import pandas as pd

# ----------- Population -------------
population = pd.read_csv("population.csv")

# Drop unnecessary columns
population = population.drop(columns=["Indicator Name", "Indicator Code"])

# Melt wide -> long format
population_long = population.melt(
    id_vars=["Country Name", "Country Code"],
    var_name="Year",
    value_name="Population"
)
population_long.rename(columns={"Country Name": "Country"}, inplace=True)
population_long["Year"] = population_long["Year"].astype(int)
population_long["Population"] = pd.to_numeric(population_long["Population"], errors='coerce')
population_long = population_long.dropna(subset=["Population"])

# ----------- Migration -------------
migration = pd.read_csv("migration.csv")

# Drop unnecessary columns
migration = migration.drop(columns=["Indicator Name", "Indicator Code"])

# Melt wide -> long format
migration_long = migration.melt(
    id_vars=["Country Name", "Country Code"],
    var_name="Year",
    value_name="NetMigration"
)
migration_long.rename(columns={"Country Name": "Country"}, inplace=True)
migration_long["Year"] = migration_long["Year"].astype(int)
migration_long["NetMigration"] = pd.to_numeric(migration_long["NetMigration"], errors='coerce')
migration_long = migration_long.dropna(subset=["NetMigration"])

# ----------- Merge Datasets -------------
df = pd.merge(population_long, migration_long, on=["Country", "Year"])
df["PopGrowthRate"] = df.groupby("Country")["Population"].pct_change() * 100

print(df.head())
