# 🇮🇳 India Census 2011 — Interactive Dashboard

An interactive data visualization dashboard built with **Streamlit** and **Plotly** that explores India's 2011 Census data at the district level across all states.

>  **Live Demo**: [your-app-link-here.streamlit.app](https://streamlit.io)

---

<img width="1919" height="907" alt="image" src="https://github.com/user-attachments/assets/e675e475-231c-4786-8253-cf79a128746d" />


---

##  Overview

India's 2011 Census is one of the most comprehensive demographic datasets in the world — covering **640 districts** across **35 states and union territories** with 100+ socioeconomic indicators.

This dashboard makes that data explorable and visual, letting anyone understand patterns in literacy, religion, income, infrastructure, and more — at both the national and district level.

---

##  Features

| Tab | What It Shows |
|---|---|
|  **Map** | Interactive scatter map — any metric as bubble size & colour |
|  **Rankings** | Top N / Bottom N districts for any metric + scatter correlations |
|  **Education** | Education funnel (drop-off rates) + state-wise stacked breakdown |
|  **Religion** | Religious composition — donut charts + state heatmap |
|  **Income** | Income/power parity bracket distribution + state heatmap |
|  **Assets** | Household asset ownership, age groups, drinking water sources |
|  **Deep Dive** | Full district profile vs state average vs national average |
|  **Compare** | Side-by-side comparison of any two states |

###  KPI Cards
Every view shows live summary cards for:
- Total Population
- Number of Districts
- Literacy Rate
- Sex Ratio
- Internet Access %
- Electrification %

---

##  Screenshots

###  Interactive Map
> Bubble size = Primary metric | Colour = Secondary metric

<img width="1489" height="533" alt="image" src="https://github.com/user-attachments/assets/85c26dc6-f9cc-4e9e-a088-7dad4cfaf96b" />


---

###  District Rankings
> Top & Bottom N districts for any metric, with scatter plot correlations

<img width="1597" height="518" alt="image" src="https://github.com/user-attachments/assets/451d67d3-433d-42d6-a89c-f73180364f1f" />
<img width="1599" height="505" alt="image" src="https://github.com/user-attachments/assets/1d1e71b9-f1ba-469c-8c44-9027211928b0" />


---

###  Education Funnel
> Visualizes the drop-off from primary school through graduation

<img width="1658" height="898" alt="image" src="https://github.com/user-attachments/assets/95f8ceb6-65e3-48c3-93d5-b24381934ba2" />


---

###  Religious Composition
> Donut chart + state-wise religion heatmap

<img width="1654" height="874" alt="image" src="https://github.com/user-attachments/assets/657c2405-1705-4d42-b43b-ded91875adb9" />


---

###  District Deep Dive
> Full district profile compared to state and national averages

<img width="1629" height="668" alt="image" src="https://github.com/user-attachments/assets/efb28ef7-c737-4f09-b996-3b515e24140c" />



---

###  State Comparison
> Compare any two states across all key metrics

<img width="1619" height="779" alt="image" src="https://github.com/user-attachments/assets/eaf1e172-24f2-49ef-9faa-f47736410e25" />


---

##  Dataset

| File | Description |
|---|---|
| `india-districts-census-2011.csv` | 640 districts × 118 columns — population, religion, education, income, assets, etc. |
| `district wise centroids.csv` | Latitude & Longitude for each district (for map rendering) |

**Source**: Census of India 2011 — Office of the Registrar General & Census Commissioner

---

##  Tech Stack

- **[Streamlit](https://streamlit.io)** — Web app framework
- **[Plotly](https://plotly.com/python/)** — Interactive charts and maps
- **[Pandas](https://pandas.pydata.org/)** — Data loading and transformation
- **[NumPy](https://numpy.org/)** — Numerical operations

---

##  Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/your-username/india-census-dashboard.git
cd india-census-dashboard
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

##  Project Structure

```
india-census-dashboard/
│
├── app.py                              # Main Streamlit application
├── requirements.txt                    # Python dependencies
├── india-districts-census-2011.csv     # Census dataset
├── district_wise_centroids.csv         # District coordinates
├── screenshots/                        # README screenshots
│   ├── map.png
│   ├── rankings.png
│   ├── education.png
│   ├── religion.png
│   ├── deepdive.png
│   └── compare.png
└── README.md
```

---

##  requirements.txt

```
streamlit
pandas
numpy
plotly
```

---

##  Key Insights You Can Explore

- Which districts have the **highest and lowest literacy rates**?
- How does **internet access correlate with education levels**?
- What is the **religious composition** of each state?
- Which states have the most households in the **highest income brackets**?
- How does a district compare to its **state average and national average**?
- How do two states like **Kerala vs Bihar** differ across all metrics?

---

##  About

Built as a data visualization project to explore and understand India's demographic and socioeconomic diversity through the lens of the 2011 Census.

---

