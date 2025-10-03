# 🌍 DemoGraphix

DemoGraphix is an interactive **data visualization app** built with **Streamlit**. It allows users to explore **world population growth and migration trends** across countries over the years. Users can filter data, visualize trends, compare metrics, and download the dataset.

---


## 🌐 Live Demo

You can explore the app online here: [DemoGraphix App](https://demographix-hxyshpoydoyleaqubksvum.streamlit.app/)

---

## **Features**

- 🌏 **World Population Map**: Interactive choropleth map showing population per country.  
- 📈 **Population Growth**: Line chart of population growth over selected years for any country.  
- 📊 **Migration Flows**: Bar chart of top countries by net migration.  
- ⚖️ **Growth vs Migration**: Scatter plot showing population growth vs net migration, sized by population.  
- 📥 **Download Data**: Download filtered dataset as CSV.  
- 🔎 **Filters**: Filter by year range and country.  
- 📊 **Key Metrics**: Sidebar shows total world population, highest growth country, and highest net migration.

---

## **Project Structure**


DemoGraphix/
│
├── app.py # Main Streamlit app
├── population.csv # Population dataset
├── migration.csv # Migration dataset
├── requirements.txt # Python dependencies
└── README.md # Project documentation


---

## **Dependencies**

- Python 3.9+
- streamlit
- pandas
- numpy
- plotly

Install dependencies with:

```bash
pip install -r requirements.txt

