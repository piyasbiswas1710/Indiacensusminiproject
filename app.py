import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="India Census 2011 Dashboard",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Noto+Sans:wght@300;400;500&display=swap');

    html, body, [class*="css"] { font-family: 'Noto Sans', sans-serif; }
    h1, h2, h3 { font-family: 'Rajdhani', sans-serif; }

    .main { background-color: #0f1117; }
    .stApp { background-color: #0f1117; }

    .metric-card {
        background: linear-gradient(135deg, #1a1f2e 0%, #16213e 100%);
        border: 1px solid #2a3550;
        border-radius: 12px;
        padding: 18px 20px;
        text-align: center;
        transition: transform 0.2s;
    }
    .metric-card:hover { transform: translateY(-2px); border-color: #e8b84b; }
    .metric-title { font-size: 11px; color: #7a8aaa; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 6px; }
    .metric-value { font-size: 26px; font-weight: 700; color: #e8b84b; font-family: 'Rajdhani', sans-serif; }
    .metric-sub { font-size: 11px; color: #5a6a8a; margin-top: 4px; }

    .section-title {
        font-family: 'Rajdhani', sans-serif;
        font-size: 22px;
        font-weight: 700;
        color: #e8b84b;
        border-left: 4px solid #e8b84b;
        padding-left: 12px;
        margin: 24px 0 16px 0;
    }
    .stSelectbox label, .stSlider label, .stMultiSelect label {
        color: #aab4cc !important;
        font-size: 12px !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton>button {
        background: linear-gradient(135deg, #e8b84b, #c9942a);
        color: #0f1117;
        font-weight: 700;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-family: 'Rajdhani', sans-serif;
        font-size: 15px;
        letter-spacing: 1px;
        width: 100%;
    }
    .stButton>button:hover { opacity: 0.9; }
    div[data-testid="stSidebar"] { background-color: #0a0e1a; border-right: 1px solid #1e2840; }
    .stTabs [data-baseweb="tab"] {
        color: #6a7a9a;
        font-family: 'Rajdhani', sans-serif;
        font-size: 15px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    .stTabs [aria-selected="true"] { color: #e8b84b !important; border-bottom-color: #e8b84b !important; }
</style>
""", unsafe_allow_html=True)

# ── Load & Merge Data ─────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    census = pd.read_csv('india-districts-census-2011.csv')
    centroids = pd.read_csv('district wise centroids.csv')
    census['_state_key'] = census['State name'].str.upper().str.strip()
    census['_dist_key']  = census['District name'].str.upper().str.strip()
    centroids['_state_key'] = centroids['State'].str.upper().str.strip()
    centroids['_dist_key']  = centroids['District'].str.upper().str.strip()
    df = pd.merge(census, centroids[['_state_key','_dist_key','Latitude','Longitude']],
                  on=['_state_key','_dist_key'], how='left')
    df.drop(columns=['_state_key','_dist_key'], inplace=True)

    # Derived metrics
    df['Sex_Ratio']       = (df['Female'] / df['Male'] * 1000).round(1)
    df['Literacy_Rate']   = (df['Literate'] / df['Population'] * 100).round(2)
    df['Worker_Rate']     = (df['Workers'] / df['Population'] * 100).round(2)
    df['Urban_Pct']       = (df['Urban_Households'] / df['Households'] * 100).round(2)
    df['Internet_Pct']    = (df['Households_with_Internet'] / df['Households'] * 100).round(2)
    df['Electric_Pct']    = (df['Housholds_with_Electric_Lighting'] / df['Households'] * 100).round(2)
    df['Graduate_Pct']    = (df['Graduate_Education'] / df['Total_Education'] * 100).round(2)
    return df

df = load_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🇮🇳 Census 2011")
    st.markdown("---")

    states = sorted(df['State name'].str.title().unique())
    states_all = ['Overall India'] + states
    selected_state = st.selectbox('📍 Select State', states_all)

    st.markdown("---")
    st.markdown("### 🗺️ Map Settings")
    map_primary   = st.selectbox('Primary (bubble size)',  sorted(df.select_dtypes(include=np.number).columns))
    map_secondary = st.selectbox('Secondary (colour)',     sorted(df.select_dtypes(include=np.number).columns))
    plot_btn = st.button('🗺️ PLOT MAP')

    st.markdown("---")
    st.markdown("### 📊 Rankings")
    top_n = st.slider('Top N Districts', 5, 30, 10)

    st.markdown("---")
    st.markdown("### 🔄 Compare States")
    compare_states = st.multiselect('Pick 2 States to Compare',
                                    states, default=states[:2], max_selections=2)
    compare_metric = st.selectbox('Comparison Metric',
                                  ['Literacy_Rate','Sex_Ratio','Internet_Pct','Electric_Pct',
                                   'Urban_Pct','Worker_Rate','Graduate_Pct'])

# ── Filter data by selected state ─────────────────────────────────────────────
if selected_state == 'Overall India':
    view_df = df.copy()
    view_title = 'Overall India'
else:
    view_df = df[df['State name'].str.title() == selected_state].copy()
    view_title = selected_state

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(f"<h1 style='font-family:Rajdhani;color:#e8b84b;font-size:36px;margin-bottom:4px;'>🇮🇳 India Census 2011 — {view_title}</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#5a6a8a;font-size:13px;margin-bottom:20px;'>District-level demographic & socioeconomic analysis</p>", unsafe_allow_html=True)

# ── KPI Cards ─────────────────────────────────────────────────────────────────
total_pop       = view_df['Population'].sum()
avg_literacy    = (view_df['Literate'].sum() / view_df['Population'].sum() * 100)
avg_sex_ratio   = (view_df['Female'].sum() / view_df['Male'].sum() * 1000)
avg_internet    = (view_df['Households_with_Internet'].sum() / view_df['Households'].sum() * 100)
avg_electric    = (view_df['Housholds_with_Electric_Lighting'].sum() / view_df['Households'].sum() * 100)
n_districts     = len(view_df)

cols = st.columns(6)
kpis = [
    ("Total Population",  f"{total_pop/1e6:.1f}M",     "2011 Census"),
    ("Districts",         f"{n_districts}",              "In selection"),
    ("Literacy Rate",     f"{avg_literacy:.1f}%",        "% of population"),
    ("Sex Ratio",         f"{avg_sex_ratio:.0f}",        "Females per 1000 males"),
    ("Internet Access",   f"{avg_internet:.1f}%",        "% of households"),
    ("Electrification",   f"{avg_electric:.1f}%",        "% of households"),
]
for col, (title, val, sub) in zip(cols, kpis):
    col.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{val}</div>
        <div class="metric-sub">{sub}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "🗺️ Map", "📊 Rankings", "🎓 Education", "🕌 Religion",
    "💰 Income", "🏠 Assets", "🔬 Deep Dive", "🔄 Compare"
])

TEMPLATE = "plotly_dark"
GOLD = "#e8b84b"

# ═══════════════════════════════════════════════════════════════
# TAB 1 — MAP
# ═══════════════════════════════════════════════════════════════
with tab1:
    map_df = view_df.dropna(subset=['Latitude','Longitude'])
    if plot_btn or True:   # always show a default map
        valid = map_df[map_df[map_primary] > 0].copy()
        zoom = 3 if selected_state == 'Overall India' else 6
        fig = px.scatter_mapbox(
            valid, lat="Latitude", lon="Longitude",
            color=map_secondary, size=map_primary,
            color_continuous_scale=px.colors.sequential.Plasma,
            size_max=35, zoom=zoom,
            hover_name='District name',
            hover_data={'State name': True, map_primary: True, map_secondary: True,
                        'Latitude': False, 'Longitude': False},
            mapbox_style="carto-darkmatter",
            title=f"{map_primary} (size) vs {map_secondary} (colour)"
        )
        fig.update_layout(
            height=680, template=TEMPLATE,
            paper_bgcolor='#0f1117', plot_bgcolor='#0f1117',
            title_font_color=GOLD, title_font_size=16
        )
        st.plotly_chart(fig, use_container_width=True)
    st.caption("💡 Use the sidebar to change Primary (bubble size) and Secondary (colour) parameters, then re-plot.")

# ═══════════════════════════════════════════════════════════════
# TAB 2 — RANKINGS
# ═══════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-title">Top & Bottom District Rankings</div>', unsafe_allow_html=True)

    rank_metric = st.selectbox('Metric to Rank By',
                               ['Literacy_Rate','Sex_Ratio','Internet_Pct','Electric_Pct',
                                'Population','Graduate_Pct','Urban_Pct','Worker_Rate'],
                               key='rank_metric')

    c1, c2 = st.columns(2)
    with c1:
        top = view_df.nlargest(top_n, rank_metric)[['District name','State name', rank_metric]].copy()
        fig = px.bar(top.sort_values(rank_metric), x=rank_metric, y='District name',
                     orientation='h', color=rank_metric,
                     color_continuous_scale='YlOrBr',
                     title=f"Top {top_n} — {rank_metric}",
                     hover_data=['State name'])
        fig.update_layout(template=TEMPLATE, height=420,
                          paper_bgcolor='#0f1117', plot_bgcolor='#0f1117',
                          title_font_color=GOLD, yaxis_title='', xaxis_title=rank_metric,
                          showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        bot = view_df.nsmallest(top_n, rank_metric)[['District name','State name', rank_metric]].copy()
        fig = px.bar(bot.sort_values(rank_metric, ascending=False), x=rank_metric, y='District name',
                     orientation='h', color=rank_metric,
                     color_continuous_scale='Blues',
                     title=f"Bottom {top_n} — {rank_metric}",
                     hover_data=['State name'])
        fig.update_layout(template=TEMPLATE, height=420,
                          paper_bgcolor='#0f1117', plot_bgcolor='#0f1117',
                          title_font_color=GOLD, yaxis_title='', xaxis_title=rank_metric,
                          showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    # Scatter: Literacy vs Internet
    st.markdown('<div class="section-title">Literacy Rate vs Internet Access</div>', unsafe_allow_html=True)
    scat = view_df.dropna(subset=['Literacy_Rate','Internet_Pct']).copy()
    fig = px.scatter(scat, x='Literacy_Rate', y='Internet_Pct',
                     size='Population', color='State name',
                     hover_name='District name',
                     title='Literacy Rate vs Internet Access (bubble = population)',
                     labels={'Literacy_Rate':'Literacy Rate (%)','Internet_Pct':'Internet Access (% HH)'},
                     size_max=40)
    fig.update_layout(template=TEMPLATE, height=480,
                      paper_bgcolor='#0f1117', plot_bgcolor='#0f1117',
                      title_font_color=GOLD)
    st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════════════════════
# TAB 3 — EDUCATION
# ═══════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-title">Education Funnel</div>', unsafe_allow_html=True)

    edu_cols   = ['Below_Primary_Education','Primary_Education','Middle_Education',
                  'Secondary_Education','Higher_Education','Graduate_Education']
    edu_labels = ['Below Primary','Primary','Middle','Secondary','Higher','Graduate']
    edu_vals   = [view_df[c].sum() for c in edu_cols]

    fig = go.Figure(go.Funnel(
        y=edu_labels, x=edu_vals,
        textposition='inside', textinfo='value+percent previous',
        marker=dict(color=['#e8b84b','#d4a03a','#c08a2a','#ac741b','#985f0c','#844a00']),
        connector=dict(line=dict(color='#2a3550', width=2))
    ))
    fig.update_layout(template=TEMPLATE, height=420,
                      paper_bgcolor='#0f1117', plot_bgcolor='#0f1117',
                      title='Education Funnel — Drop-off at Each Level',
                      title_font_color=GOLD)
    st.plotly_chart(fig, use_container_width=True)

    # Education bar by state (overall only)
    if selected_state == 'Overall India':
        st.markdown('<div class="section-title">Education Level by State</div>', unsafe_allow_html=True)
        state_edu = df.groupby('State name')[edu_cols].sum().reset_index()
        # normalise each row
        state_edu[edu_cols] = state_edu[edu_cols].div(state_edu[edu_cols].sum(axis=1), axis=0) * 100
        state_edu['State name'] = state_edu['State name'].str.title()
        fig = px.bar(state_edu, x='State name', y=edu_cols,
                     labels={c: l for c, l in zip(edu_cols, edu_labels)},
                     title='Education Distribution by State (%)',
                     color_discrete_sequence=px.colors.sequential.YlOrBr)
        fig.update_layout(template=TEMPLATE, height=480, barmode='stack',
                          paper_bgcolor='#0f1117', plot_bgcolor='#0f1117',
                          title_font_color=GOLD,
                          xaxis_tickangle=-45, legend_title='Level')
        st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════════════════════
# TAB 4 — RELIGION
# ═══════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-title">Religious Composition</div>', unsafe_allow_html=True)

    rel_cols   = ['Hindus','Muslims','Christians','Sikhs','Buddhists','Jains',
                  'Others_Religions','Religion_Not_Stated']
    rel_labels = ['Hindu','Muslim','Christian','Sikh','Buddhist','Jain','Others','Not Stated']
    rel_vals   = [view_df[c].sum() for c in rel_cols]

    c1, c2 = st.columns([1, 1])
    with c1:
        fig = px.pie(values=rel_vals, names=rel_labels,
                     title=f'Religious Composition — {view_title}',
                     hole=0.45,
                     color_discrete_sequence=px.colors.sequential.YlOrBr_r)
        fig.update_layout(template=TEMPLATE, height=420,
                          paper_bgcolor='#0f1117', title_font_color=GOLD)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        rel_df = pd.DataFrame({'Religion': rel_labels, 'Population': rel_vals})
        rel_df['%'] = (rel_df['Population'] / rel_df['Population'].sum() * 100).round(2)
        fig = px.bar(rel_df.sort_values('Population'), x='Population', y='Religion',
                     orientation='h', color='Population',
                     color_continuous_scale='YlOrBr',
                     text='%', title='Population by Religion')
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(template=TEMPLATE, height=420,
                          paper_bgcolor='#0f1117', plot_bgcolor='#0f1117',
                          title_font_color=GOLD, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    # State-wise religion heatmap (overall only)
    if selected_state == 'Overall India':
        st.markdown('<div class="section-title">Religion Share by State (%)</div>', unsafe_allow_html=True)
        sr = df.groupby('State name')[rel_cols].sum()
        sr = sr.div(sr.sum(axis=1), axis=0) * 100
        sr.index = sr.index.str.title()
        sr.columns = rel_labels
        fig = px.imshow(sr.round(1), aspect='auto',
                        color_continuous_scale='YlOrBr',
                        title='Religion Share Heatmap by State (%)',
                        text_auto='.1f')
        fig.update_layout(template=TEMPLATE, height=600,
                          paper_bgcolor='#0f1117',
                          title_font_color=GOLD)
        st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════════════════════
# TAB 5 — INCOME
# ═══════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-title">Income / Power Parity Distribution</div>', unsafe_allow_html=True)

    inc_cols   = ['Power_Parity_Less_than_Rs_45000',
                  'Power_Parity_Rs_45000_90000',
                  'Power_Parity_Rs_90000_150000',
                  'Power_Parity_Rs_150000_240000',
                  'Power_Parity_Rs_240000_330000',
                  'Power_Parity_Rs_330000_425000',
                  'Power_Parity_Rs_425000_545000',
                  'Power_Parity_Above_Rs_545000']
    inc_labels = ['<45K','45–90K','90–1.5L','1.5–2.4L','2.4–3.3L','3.3–4.25L','4.25–5.45L','>5.45L']
    inc_vals   = [view_df[c].sum() for c in inc_cols]

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(x=inc_labels, y=inc_vals,
                     color=inc_vals, color_continuous_scale='YlOrBr',
                     title=f'Income Distribution — {view_title}',
                     labels={'x':'Annual Income (₹)','y':'Households'})
        fig.update_layout(template=TEMPLATE, height=380,
                          paper_bgcolor='#0f1117', plot_bgcolor='#0f1117',
                          title_font_color=GOLD, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.pie(values=inc_vals, names=inc_labels, hole=0.4,
                     title='Income Share by Bracket',
                     color_discrete_sequence=px.colors.sequential.Plasma)
        fig.update_layout(template=TEMPLATE, height=380,
                          paper_bgcolor='#0f1117', title_font_color=GOLD)
        st.plotly_chart(fig, use_container_width=True)

    # State income heatmap (overall)
    if selected_state == 'Overall India':
        st.markdown('<div class="section-title">Income Bracket Share by State (%)</div>', unsafe_allow_html=True)
        si = df.groupby('State name')[inc_cols].sum()
        si = si.div(si.sum(axis=1), axis=0) * 100
        si.index = si.index.str.title()
        si.columns = inc_labels
        fig = px.imshow(si.round(1), aspect='auto',
                        color_continuous_scale='Plasma',
                        title='Income Distribution Heatmap by State (%)',
                        text_auto='.1f')
        fig.update_layout(template=TEMPLATE, height=600,
                          paper_bgcolor='#0f1117', title_font_color=GOLD)
        st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════════════════════
# TAB 6 — ASSETS
# ═══════════════════════════════════════════════════════════════
with tab6:
    st.markdown('<div class="section-title">Household Asset Ownership</div>', unsafe_allow_html=True)

    asset_cols   = ['Households_with_Bicycle','Households_with_Car_Jeep_Van',
                    'Households_with_Radio_Transistor','Households_with_Scooter_Motorcycle_Moped',
                    'Households_with_Television','Households_with_Computer',
                    'Households_with_Internet','Households_with_Telephone_Mobile_Phone_Mobile_only']
    asset_labels = ['Bicycle','Car/Jeep','Radio','Scooter/Bike','TV','Computer','Internet','Mobile Phone']

    total_hh    = view_df['Households'].sum()
    asset_pcts  = [view_df[c].sum() / total_hh * 100 for c in asset_cols]

    fig = px.bar(x=asset_pcts, y=asset_labels,
                 orientation='h',
                 color=asset_pcts,
                 color_continuous_scale='YlOrBr',
                 text=[f"{v:.1f}%" for v in asset_pcts],
                 title=f'Asset Ownership (% of Households) — {view_title}',
                 labels={'x':'% of Households','y':''})
    fig.update_traces(textposition='outside')
    fig.update_layout(template=TEMPLATE, height=420,
                      paper_bgcolor='#0f1117', plot_bgcolor='#0f1117',
                      title_font_color=GOLD, coloraxis_showscale=False,
                      xaxis_range=[0, max(asset_pcts)*1.2])
    st.plotly_chart(fig, use_container_width=True)

    # Age distribution
    st.markdown('<div class="section-title">Age Group Distribution</div>', unsafe_allow_html=True)
    age_cols   = ['Age_Group_0_29','Age_Group_30_49','Age_Group_50']
    age_labels = ['0–29 yrs','30–49 yrs','50+ yrs']
    age_vals   = [view_df[c].sum() for c in age_cols]

    c1, c2 = st.columns(2)
    with c1:
        fig = px.pie(values=age_vals, names=age_labels, hole=0.4,
                     title=f'Age Distribution — {view_title}',
                     color_discrete_sequence=['#e8b84b','#c08a2a','#7a5010'])
        fig.update_layout(template=TEMPLATE, height=360,
                          paper_bgcolor='#0f1117', title_font_color=GOLD)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        # Water sources
        water_cols   = ['Main_source_of_drinking_water_Tapwater_Households',
                        'Main_source_of_drinking_water_Handpump_Tubewell_Borewell_Households',
                        'Main_source_of_drinking_water_River_Canal_Households',
                        'Main_source_of_drinking_water_Spring_Households',
                        'Main_source_of_drinking_water_Tank_Pond_Lake_Households',
                        'Main_source_of_drinking_water_Un_covered_well_Households']
        water_labels = ['Tap Water','Handpump/Borewell','River/Canal','Spring','Tank/Pond','Open Well']
        water_vals   = [view_df[c].sum() for c in water_cols if c in view_df.columns]
        wl_avail     = [l for c,l in zip(water_cols, water_labels) if c in view_df.columns]
        fig = px.pie(values=water_vals, names=wl_avail, hole=0.4,
                     title='Drinking Water Sources',
                     color_discrete_sequence=px.colors.sequential.Blues_r)
        fig.update_layout(template=TEMPLATE, height=360,
                          paper_bgcolor='#0f1117', title_font_color=GOLD)
        st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════════════════════
# TAB 7 — DISTRICT DEEP DIVE
# ═══════════════════════════════════════════════════════════════
with tab7:
    st.markdown('<div class="section-title">District Deep Dive</div>', unsafe_allow_html=True)

    district_list = sorted(view_df['District name'].str.title().unique())
    sel_dist = st.selectbox('Select a District', district_list, key='deep_dive_dist')

    dist_row   = view_df[view_df['District name'].str.title() == sel_dist].iloc[0]
    state_avg  = view_df.mean(numeric_only=True)
    india_avg  = df.mean(numeric_only=True)

    metrics = {
        'Population':      ('Population',    '',    1),
        'Literacy Rate':   ('Literacy_Rate', '%',   1),
        'Sex Ratio':       ('Sex_Ratio',     '',    1),
        'Internet Access': ('Internet_Pct',  '%',   1),
        'Electrification': ('Electric_Pct',  '%',   1),
        'Graduate %':      ('Graduate_Pct',  '%',   1),
        'Urban %':         ('Urban_Pct',     '%',   1),
        'Worker Rate':     ('Worker_Rate',   '%',   1),
    }

    cols = st.columns(4)
    for i, (label, (col, unit, rnd)) in enumerate(metrics.items()):
        val  = dist_row[col]
        ref  = state_avg[col] if selected_state != 'Overall India' else india_avg[col]
        delta = val - ref
        cols[i % 4].metric(label,
                           f"{val:,.{rnd}f}{unit}",
                           f"{delta:+.{rnd}f}{unit} vs avg")

    st.markdown('<div class="section-title">District vs State vs India Comparison</div>', unsafe_allow_html=True)

    compare_cols = ['Literacy_Rate','Sex_Ratio','Internet_Pct','Electric_Pct',
                    'Urban_Pct','Worker_Rate','Graduate_Pct']
    compare_labels = ['Literacy','Sex Ratio','Internet','Electric','Urban','Workers','Graduate']

    dist_vals  = [dist_row[c] for c in compare_cols]
    state_vals = [state_avg[c] for c in compare_cols]
    india_vals = [india_avg[c] for c in compare_cols]

    fig = go.Figure()
    fig.add_trace(go.Bar(name=sel_dist,       x=compare_labels, y=dist_vals,  marker_color='#e8b84b'))
    fig.add_trace(go.Bar(name=f'{view_title}',x=compare_labels, y=state_vals, marker_color='#4a7aff'))
    fig.add_trace(go.Bar(name='India Avg',    x=compare_labels, y=india_vals, marker_color='#2a3a6a'))
    fig.update_layout(template=TEMPLATE, barmode='group', height=400,
                      paper_bgcolor='#0f1117', plot_bgcolor='#0f1117',
                      title=f'{sel_dist} vs Averages', title_font_color=GOLD,
                      legend=dict(bgcolor='#1a1f2e'))
    st.plotly_chart(fig, use_container_width=True)

    # Religion breakdown for district
    st.markdown('<div class="section-title">Religion in This District</div>', unsafe_allow_html=True)
    rel_vals_d = [dist_row[c] for c in rel_cols]
    fig = px.pie(values=rel_vals_d, names=rel_labels, hole=0.4,
                 title=f'Religious Composition — {sel_dist}',
                 color_discrete_sequence=px.colors.sequential.YlOrBr_r)
    fig.update_layout(template=TEMPLATE, height=360,
                      paper_bgcolor='#0f1117', title_font_color=GOLD)
    c1, c2 = st.columns([1,2])
    c1.plotly_chart(fig, use_container_width=True)
    with c2:
        edu_vals_d = [dist_row[c] for c in edu_cols]
        fig2 = go.Figure(go.Funnel(
            y=edu_labels, x=edu_vals_d,
            textinfo='value+percent previous',
            marker=dict(color=['#e8b84b','#d4a03a','#c08a2a','#ac741b','#985f0c','#844a00'])
        ))
        fig2.update_layout(template=TEMPLATE, height=360,
                           paper_bgcolor='#0f1117', title='Education Funnel',
                           title_font_color=GOLD)
        st.plotly_chart(fig2, use_container_width=True)

# ═══════════════════════════════════════════════════════════════
# TAB 8 — COMPARE TWO STATES
# ═══════════════════════════════════════════════════════════════
with tab8:
    st.markdown('<div class="section-title">State-to-State Comparison</div>', unsafe_allow_html=True)

    if len(compare_states) == 2:
        s1, s2 = compare_states
        df1 = df[df['State name'].str.title() == s1]
        df2 = df[df['State name'].str.title() == s2]

        # KPI comparison
        kpi_cols = ['Literacy_Rate','Sex_Ratio','Internet_Pct','Electric_Pct',
                    'Urban_Pct','Worker_Rate','Graduate_Pct','Population']
        kpi_lbl  = ['Literacy %','Sex Ratio','Internet %','Electric %',
                    'Urban %','Workers %','Graduate %','Population']

        vals1 = [df1[c].mean() if c != 'Population' else df1[c].sum() for c in kpi_cols]
        vals2 = [df2[c].mean() if c != 'Population' else df2[c].sum() for c in kpi_cols]

        fig = go.Figure()
        fig.add_trace(go.Bar(name=s1, y=kpi_lbl, x=vals1, orientation='h', marker_color='#e8b84b'))
        fig.add_trace(go.Bar(name=s2, y=kpi_lbl, x=vals2, orientation='h', marker_color='#4a7aff'))
        fig.update_layout(template=TEMPLATE, barmode='group', height=440,
                          paper_bgcolor='#0f1117', plot_bgcolor='#0f1117',
                          title=f'{s1} vs {s2} — Key Metrics', title_font_color=GOLD,
                          legend=dict(bgcolor='#1a1f2e'))
        st.plotly_chart(fig, use_container_width=True)

        # Per-district scatter of chosen metric
        st.markdown(f'<div class="section-title">District-level: {compare_metric}</div>', unsafe_allow_html=True)
        comb = pd.concat([
            df1[['District name', compare_metric]].assign(State=s1),
            df2[['District name', compare_metric]].assign(State=s2)
        ])
        fig = px.strip(comb, x='State', y=compare_metric, color='State',
                       hover_name='District name',
                       color_discrete_map={s1:'#e8b84b', s2:'#4a7aff'},
                       title=f'District-level Distribution of {compare_metric}')
        fig.update_layout(template=TEMPLATE, height=420,
                          paper_bgcolor='#0f1117', plot_bgcolor='#0f1117',
                          title_font_color=GOLD, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

        # Religion side by side
        st.markdown('<div class="section-title">Religion Comparison</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        for col_w, state_n, sdf in [(c1, s1, df1), (c2, s2, df2)]:
            rv = [sdf[c].sum() for c in rel_cols]
            fig = px.pie(values=rv, names=rel_labels, hole=0.4,
                         title=f'{state_n}',
                         color_discrete_sequence=px.colors.sequential.YlOrBr_r)
            fig.update_layout(template=TEMPLATE, height=340,
                              paper_bgcolor='#0f1117', title_font_color=GOLD)
            col_w.plotly_chart(fig, use_container_width=True)

    else:
        st.info("👈 Please select exactly 2 states from the sidebar to compare.")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("<p style='text-align:center;color:#3a4a6a;font-size:12px;'>India Census 2011 • District-level Data • Built with Streamlit & Plotly</p>",
            unsafe_allow_html=True)