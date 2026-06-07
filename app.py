"""
Dashboard — Olist Brazilian E-commerce
Data-Driven Decision Making — Phase 5 & 6
Membre 3 : Data Storyteller & Décision Analyst
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Olist — Churn & LTV Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Fonts & base ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ── Background ── */
    .main { background: #0d0f1a; }
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #12152a 0%, #0d0f1a 100%);
        border-right: 1px solid #1e2340;
    }

    /* ── KPI Cards ── */
    .kpi-card {
        background: linear-gradient(135deg, #1a1d35 0%, #12152a 100%);
        border: 1px solid #252847;
        border-radius: 16px;
        padding: 22px 20px 18px;
        position: relative;
        overflow: hidden;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 32px rgba(99,102,241,0.18);
    }
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        border-radius: 16px 16px 0 0;
    }
    .kpi-card.blue::before  { background: linear-gradient(90deg, #6366f1, #8b5cf6); }
    .kpi-card.green::before { background: linear-gradient(90deg, #10b981, #34d399); }
    .kpi-card.red::before   { background: linear-gradient(90deg, #ef4444, #f97316); }
    .kpi-card.yellow::before{ background: linear-gradient(90deg, #f59e0b, #fbbf24); }
    .kpi-card.cyan::before  { background: linear-gradient(90deg, #06b6d4, #3b82f6); }

    .kpi-label  { font-size: 11px; font-weight: 600; letter-spacing: 1.2px; text-transform: uppercase; color: #6b7280; margin-bottom: 6px; }
    .kpi-value  { font-size: 32px; font-weight: 800; color: #f1f5f9; line-height: 1; }
    .kpi-delta  { font-size: 12px; margin-top: 6px; color: #9ca3af; }
    .kpi-delta.pos { color: #10b981; }
    .kpi-delta.neg { color: #ef4444; }
    .kpi-icon   { font-size: 28px; position: absolute; right: 16px; top: 20px; opacity: 0.25; }

    /* ── Section headers ── */
    .section-title {
        font-size: 18px; font-weight: 700; color: #e2e8f0;
        margin: 8px 0 16px; padding-bottom: 10px;
        border-bottom: 1px solid #1e2340;
        display: flex; align-items: center; gap: 10px;
    }
    .section-title span { color: #6366f1; }

    /* ── Insight boxes ── */
    .insight-box {
        background: linear-gradient(135deg, #1a1d35 0%, #12152a 100%);
        border: 1px solid #252847;
        border-left: 4px solid #6366f1;
        border-radius: 10px;
        padding: 14px 16px;
        margin-bottom: 10px;
        font-size: 14px;
        color: #cbd5e1;
        line-height: 1.6;
    }
    .insight-box.green  { border-left-color: #10b981; }
    .insight-box.red    { border-left-color: #ef4444; }
    .insight-box.yellow { border-left-color: #f59e0b; }

    /* ── Recommendation cards ── */
    .reco-card {
        background: linear-gradient(135deg, #1a1d35 0%, #12152a 100%);
        border: 1px solid #252847;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 14px;
        position: relative;
    }
    .reco-badge {
        display: inline-block;
        background: #6366f1;
        color: white;
        font-size: 10px; font-weight: 700;
        letter-spacing: 1px; text-transform: uppercase;
        padding: 3px 10px; border-radius: 20px;
        margin-bottom: 10px;
    }
    .reco-badge.green  { background: #10b981; }
    .reco-badge.yellow { background: #f59e0b; color: #1a1a1a; }
    .reco-title { font-size: 15px; font-weight: 700; color: #f1f5f9; margin-bottom: 8px; }
    .reco-body  { font-size: 13px; color: #94a3b8; line-height: 1.6; }
    .reco-impact { font-size: 12px; color: #10b981; font-weight: 600; margin-top: 10px; }

    /* ── Badge ── */
    .badge {
        display: inline-block; padding: 3px 10px; border-radius: 20px;
        font-size: 11px; font-weight: 600;
    }
    .badge.green  { background: rgba(16,185,129,0.15); color: #10b981; }
    .badge.red    { background: rgba(239,68,68,0.15);  color: #ef4444; }
    .badge.yellow { background: rgba(245,158,11,0.15); color: #f59e0b; }

    /* ── Sidebar tweaks ── */
    .sidebar-logo {
        text-align: center; padding: 10px 0 20px;
        font-size: 22px; font-weight: 800;
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }

    /* ── Tab overrides ── */
    .stTabs [data-baseweb="tab-list"] {
        background: #12152a;
        border-radius: 12px;
        padding: 4px;
        gap: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: #6b7280;
        font-weight: 600;
        font-size: 13px;
        padding: 8px 18px;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
    }

    /* ── Plotly charts background ── */
    .js-plotly-plot { border-radius: 12px; overflow: hidden; }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #0d0f1a; }
    ::-webkit-scrollbar-thumb { background: #252847; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
#  DATA GENERATION (basée sur les résultats réels des phases 1-4)
# ══════════════════════════════════════════════════════════════════════════

@st.cache_data
def generate_data():
    np.random.seed(42)

    # ── Churn scores (19 165 clients du jeu test) ──
    n = 4000
    scores = np.concatenate([
        np.random.beta(8, 2, int(n * 0.57)),   # haut risque
        np.random.beta(3, 5, int(n * 0.11)),   # risque modéré
        np.random.beta(1, 6, int(n * 0.32)),   # faible risque
    ])
    scores = np.clip(scores, 0, 1)

    churn_df = pd.DataFrame({
        'score_churn': scores,
        'Monetary': np.random.exponential(165, n),
        'review_score': np.random.choice([1,2,3,4,5], n, p=[0.11,0.08,0.09,0.20,0.52]),
        'is_late': np.random.choice([0,1], n, p=[0.932, 0.068]),
        'Cluster_KMeans': np.random.choice([0,1], n, p=[0.03, 0.97]),
        'churn_reel': np.where(scores > 0.5, 1, 0),
    })
    churn_df['churn_predit'] = (churn_df['score_churn'] >= 0.5).astype(int)
    churn_df['zone_risque'] = pd.cut(churn_df['score_churn'],
        bins=[0, 0.40, 0.70, 1.0],
        labels=['Vert — Faible risque', 'Jaune — Risque modéré', 'Rouge — Haut risque'])

    # ── Série temporelle CA mensuel ──
    months = pd.date_range('2016-10', periods=25, freq='ME')
    ca_base = [200, 400, 700, 900, 700, 800, 900, 950, 1000, 1100,
               1050, 1200, 800, 1000, 1050, 1100, 1050, 1080, 1050,
               1200, 900, 700, 600, 400, 300]
    ca_monthly = pd.DataFrame({'month': months, 'CA': [x * 1000 * (1 + np.random.normal(0,0.05)) for x in ca_base[:25]]})

    # ── Satisfaction vs retard ──
    delivery_delta = np.arange(-30, 61)
    review_mean = np.where(delivery_delta < 0, 4.5 - 0.02*np.abs(delivery_delta),
                           np.maximum(1.0, 4.2 - 0.05*delivery_delta))
    sat_df = pd.DataFrame({'delivery_delta': delivery_delta, 'review_mean': review_mean})

    # ── Top catégories ──
    categories = {
        'bed_bath_table': 1713293, 'health_beauty': 1501657,
        'computers_accessories': 1424490, 'sports_leisure': 1307022,
        'furniture_decor': 1200450, 'housewares': 1100789,
        'auto': 980234, 'garden_tools': 900123,
        'watches_gifts': 870453, 'cool_stuff': 760234
    }
    cat_df = pd.DataFrame(list(categories.items()), columns=['category','CA'])

    # ── Géo par état ──
    states = {'SP':42.0,'RJ':12.0,'MG':11.0,'RS':5.0,'PR':5.0,
              'SC':3.5,'BA':3.0,'GO':2.0,'DF':2.0,'Autres':14.5}
    geo_df = pd.DataFrame(list(states.items()), columns=['state','pct'])

    # ── Profils cluster RFM ──
    rfm_profiles = pd.DataFrame({
        'Cluster': ['Cluster 0\n(Champions)', 'Cluster 1\n(One-shot)'],
        'Recency': [269.6, 287.7],
        'Frequency': [2.11, 1.00],
        'Monetary': [329.5, 160.1],
        'Size': [2810, 90548],
    })

    # ── Jours/heures ──
    dow = pd.DataFrame({
        'jour': ['Lun','Mar','Mer','Jeu','Ven','Sam','Dim'],
        'count': [15800, 15400, 14900, 14700, 14500, 10800, 13300]
    })
    hours = pd.DataFrame({
        'heure': list(range(24)),
        'count': [100, 60, 40, 30, 50, 200, 900, 2800, 4200, 5000,
                  5800, 6000, 5900, 6100, 5800, 5600, 5700, 6200,
                  6800, 7000, 6900, 6200, 5100, 3200]
    })

    # ── Modèles performance ──
    models_df = pd.DataFrame({
        'Modèle': ['Régression Logistique', 'Random Forest', 'XGBoost (optimisé)'],
        'AUC-ROC': [0.749, 0.971, 0.977],
        'F1-Score': [0.749, 0.927, 0.938],
        'Précision': [0.805, 0.943, 0.949],
        'Rappel': [0.701, 0.911, 0.927],
    })

    # ── SHAP importance ──
    shap_df = pd.DataFrame({
        'feature': ['purchase_month','Cluster_KMeans','total_freight',
                    'delivery_days','delivery_delta','review_score',
                    'is_peak_hour','installments','purchase_hour',
                    'total_price','freight_ratio','Monetary'],
        'importance': [4.15, 1.08, 0.62, 0.38, 0.35, 0.18,
                       0.14, 0.12, 0.11, 0.10, 0.09, 0.08]
    }).sort_values('importance', ascending=True)

    return churn_df, ca_monthly, sat_df, cat_df, geo_df, rfm_profiles, dow, hours, models_df, shap_df

churn_df, ca_monthly, sat_df, cat_df, geo_df, rfm_profiles, dow_df, hours_df, models_df, shap_df = generate_data()

# ── Plotly dark theme base ──
CHART_THEME = {
    'paper_bgcolor': 'rgba(0,0,0,0)',
    'plot_bgcolor':  'rgba(0,0,0,0)',
    'font': {'color': '#94a3b8', 'family': 'Inter'},
    'xaxis': {'gridcolor': '#1e2340', 'linecolor': '#1e2340', 'zerolinecolor': '#1e2340'},
    'yaxis': {'gridcolor': '#1e2340', 'linecolor': '#1e2340', 'zerolinecolor': '#1e2340'},
}

COLORS = {
    'primary': '#6366f1', 'green': '#10b981', 'red': '#ef4444',
    'yellow': '#f59e0b', 'cyan': '#06b6d4', 'purple': '#8b5cf6',
    'gradient': ['#6366f1','#8b5cf6','#06b6d4','#10b981','#f59e0b'],
}


# ══════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown('<div class="sidebar-logo">🛒 Olist Analytics</div>', unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("**🎯 Navigation**")
    page = st.radio("", [
        "📊 Vue Générale",
        "🔴 Analyse du Churn",
        "🤖 Modèles ML",
        "💡 Recommandations",
        "─────────────────",
        "🏢 Direction",
        "⚙️ Opérations",
        "📣 Marketing",
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown("**🔎 Filtres**")

    score_seuil = st.slider("Seuil de risque churn", 0.0, 1.0, 0.7, 0.05,
                            help="Seuil au-dessus duquel un client est en zone rouge")

    cluster_filter = st.multiselect("Segment client",
        ['Cluster 0 — Champions', 'Cluster 1 — One-shot'],
        default=['Cluster 0 — Champions', 'Cluster 1 — One-shot'])

    st.markdown("---")
    st.caption("Dataset : Olist Brazilian E-commerce")
    st.caption("96 478 commandes · 93 358 clients")


# ══════════════════════════════════════════════════════════════════════════
#  HELPER : KPI card
# ══════════════════════════════════════════════════════════════════════════

def kpi(label, value, delta="", color="blue", icon=""):
    delta_class = "pos" if delta.startswith("+") else ("neg" if delta.startswith("-") else "")
    st.markdown(f"""
    <div class="kpi-card {color}">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-delta {delta_class}">{delta}</div>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
#  PAGE 1 — VUE GÉNÉRALE
# ══════════════════════════════════════════════════════════════════════════

if page == "📊 Vue Générale":
    st.markdown("## 📊 Vue Générale — Olist E-commerce")
    st.markdown("*Tableau de bord opérationnel · Données 2016-2018*")
    st.markdown("")

    # ── KPI row ──
    c1,c2,c3,c4,c5 = st.columns(5)
    with c1: kpi("CA Total","R$ 16M","+9.4% potentiel","blue","💰")
    with c2: kpi("Commandes","99 441","Dataset complet","green","📦")
    with c3: kpi("Taux de Churn","96.9%","⚠ critique","red","⚡")
    with c4: kpi("Satisfaction","4.16 / 5","std : 1.28","yellow","⭐")
    with c5: kpi("Délai moyen","12.1 jours","6.8% retards","cyan","🚚")

    st.markdown("<br>", unsafe_allow_html=True)
    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown('<div class="section-title"><span>📈</span> Évolution du CA Mensuel (BRL)</div>', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=ca_monthly['month'], y=ca_monthly['CA'],
            mode='lines+markers',
            line=dict(color='#6366f1', width=3),
            marker=dict(size=5, color='#8b5cf6'),
            fill='tozeroy',
            fillcolor='rgba(99,102,241,0.08)',
            name='CA mensuel',
            hovertemplate='%{x|%b %Y}<br>CA : R$ %{y:,.0f}<extra></extra>'
        ))
        # Peak annotation
        peak_idx = ca_monthly['CA'].idxmax()
        fig.add_annotation(
            x=ca_monthly.loc[peak_idx,'month'], y=ca_monthly.loc[peak_idx,'CA'],
            text="📈 Pic Nov 2017",
            showarrow=True, arrowhead=2, arrowcolor='#6366f1',
            font=dict(color='#6366f1', size=11),
            bgcolor='rgba(99,102,241,0.1)', bordercolor='#6366f1', borderwidth=1
        )
        fig.update_layout(**CHART_THEME, height=300, margin=dict(l=0,r=0,t=10,b=0),
                          showlegend=False)
        fig.update_xaxes(**CHART_THEME['xaxis'])
        fig.update_yaxes(**CHART_THEME['yaxis'], tickprefix='R$ ', tickformat=',.0f')
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.markdown('<div class="section-title"><span>🗺️</span> Répartition Géographique</div>', unsafe_allow_html=True)
        fig2 = go.Figure(go.Pie(
            labels=geo_df['state'], values=geo_df['pct'],
            hole=0.55,
            marker=dict(colors=['#6366f1','#8b5cf6','#06b6d4','#10b981','#f59e0b',
                                  '#ef4444','#f97316','#84cc16','#ec4899','#64748b']),
            textfont=dict(color='#94a3b8', size=11),
            hovertemplate='%{label}: %{value:.1f}%<extra></extra>'
        ))
        fig2.update_layout(**CHART_THEME, height=300, margin=dict(l=0,r=0,t=10,b=0),
                           showlegend=True,
                           legend=dict(font=dict(size=10, color='#94a3b8'), orientation='v', x=1))
        fig2.add_annotation(text="42% SP<br><span style='font-size:10px'>Biais géo</span>",
                            x=0.5, y=0.5, showarrow=False, font=dict(size=12, color='#f59e0b'))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown('<div class="section-title"><span>🕐</span> Commandes par Heure</div>', unsafe_allow_html=True)
        fig3 = go.Figure(go.Bar(
            x=hours_df['heure'], y=hours_df['count'],
            marker=dict(
                color=hours_df['count'],
                colorscale=[[0,'#1e2340'],[0.5,'#6366f1'],[1,'#8b5cf6']],
                showscale=False
            ),
            hovertemplate='%{x}h : %{y:,} commandes<extra></extra>'
        ))
        fig3.update_layout(**CHART_THEME, height=220, margin=dict(l=0,r=0,t=0,b=0))
        fig3.update_xaxes(**CHART_THEME['xaxis'], title_text="Heure")
        fig3.update_yaxes(**CHART_THEME['yaxis'])
        st.plotly_chart(fig3, use_container_width=True)

    with c2:
        st.markdown('<div class="section-title"><span>📅</span> Commandes par Jour</div>', unsafe_allow_html=True)
        fig4 = go.Figure(go.Bar(
            x=dow_df['jour'], y=dow_df['count'],
            marker=dict(
                color=dow_df['count'],
                colorscale=[[0,'#1e2340'],[0.5,'#06b6d4'],[1,'#3b82f6']],
                showscale=False
            ),
            hovertemplate='%{x} : %{y:,} commandes<extra></extra>'
        ))
        fig4.update_layout(**CHART_THEME, height=220, margin=dict(l=0,r=0,t=0,b=0))
        fig4.update_xaxes(**CHART_THEME['xaxis'])
        fig4.update_yaxes(**CHART_THEME['yaxis'])
        st.plotly_chart(fig4, use_container_width=True)

    with c3:
        st.markdown('<div class="section-title"><span>🏷️</span> Top 5 Catégories (CA)</div>', unsafe_allow_html=True)
        top5 = cat_df.nlargest(5,'CA')
        fig5 = go.Figure(go.Bar(
            x=top5['CA'], y=top5['category'],
            orientation='h',
            marker=dict(
                color=['#6366f1','#8b5cf6','#06b6d4','#10b981','#f59e0b'],
            ),
            hovertemplate='%{y}<br>R$ %{x:,.0f}<extra></extra>'
        ))
        fig5.update_layout(**CHART_THEME, height=220, margin=dict(l=0,r=0,t=0,b=0))
        fig5.update_xaxes(**CHART_THEME['xaxis'], tickprefix='R$', tickformat=',.0s')
        fig5.update_yaxes(**CHART_THEME['yaxis'])
        st.plotly_chart(fig5, use_container_width=True)

    # ── Key insights ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title"><span>💡</span> Insights Clés</div>', unsafe_allow_html=True)
    i1, i2, i3 = st.columns(3)
    with i1:
        st.markdown('<div class="insight-box red">⚡ <b>Taux de churn critique : 96.9%</b><br>Seulement 3.1% des clients rachètent. La rétention est le levier prioritaire pour augmenter le CA.</div>', unsafe_allow_html=True)
    with i2:
        st.markdown('<div class="insight-box yellow">🚚 <b>Livraison = facteur clé</b><br>Corrélation forte entre retard de livraison et satisfaction (r=-0.39). 6.8% des commandes sont en retard.</div>', unsafe_allow_html=True)
    with i3:
        st.markdown('<div class="insight-box green">📍 <b>Biais géographique São Paulo</b><br>42% des clients sont concentrés en SP. Opportunité de croissance dans les autres États brésiliens.</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
#  PAGE 2 — ANALYSE DU CHURN
# ══════════════════════════════════════════════════════════════════════════

elif page == "🔴 Analyse du Churn":
    st.markdown("## 🔴 Analyse du Churn Client")
    st.markdown("*Variable cible : Recency > 180 jours ET Frequency = 1*")
    st.markdown("")

    # ── KPIs churn ──
    n_rouge = (churn_df['zone_risque'] == 'Rouge — Haut risque').sum()
    n_jaune = (churn_df['zone_risque'] == 'Jaune — Risque modéré').sum()
    n_vert  = (churn_df['zone_risque'] == 'Vert — Faible risque').sum()
    n_total = len(churn_df)

    c1,c2,c3,c4 = st.columns(4)
    with c1: kpi("Zone Rouge","57.2%",f"~{n_rouge:,} clients","red","🔴")
    with c2: kpi("Zone Jaune","11.0%",f"~{n_jaune:,} clients","yellow","🟡")
    with c3: kpi("Zone Verte","31.8%",f"~{n_vert:,} clients","green","🟢")
    with c4: kpi("Score Moyen","0.642","Seuil critique : 0.70","blue","📊")

    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_r = st.columns([2,3])

    with col_l:
        st.markdown('<div class="section-title"><span>📊</span> Distribution des Zones de Risque</div>', unsafe_allow_html=True)
        zone_counts = churn_df['zone_risque'].value_counts()
        labels = ['Haut risque 🔴', 'Risque modéré 🟡', 'Faible risque 🟢']
        values = [zone_counts.get('Rouge — Haut risque', 0),
                  zone_counts.get('Jaune — Risque modéré', 0),
                  zone_counts.get('Vert — Faible risque', 0)]
        fig = go.Figure(go.Pie(
            labels=labels, values=values, hole=0.60,
            marker=dict(colors=['#ef4444','#f59e0b','#10b981']),
            textfont=dict(color='white', size=12),
            hovertemplate='%{label}<br>%{value:,} clients (%{percent})<extra></extra>'
        ))
        fig.add_annotation(text=f"<b>{n_total:,}</b><br>clients", x=0.5, y=0.5,
                           showarrow=False, font=dict(size=14, color='#f1f5f9'))
        fig.update_layout(**CHART_THEME, height=300, margin=dict(l=0,r=0,t=10,b=0),
                          showlegend=True, legend=dict(orientation='h', y=-0.05,
                          font=dict(size=11, color='#94a3b8')))
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown('<div class="section-title"><span>📉</span> Distribution des Scores de Churn</div>', unsafe_allow_html=True)
        fig2 = go.Figure()
        # Background zones
        fig2.add_vrect(x0=0, x1=0.4, fillcolor='rgba(16,185,129,0.05)', line_width=0)
        fig2.add_vrect(x0=0.4, x1=score_seuil, fillcolor='rgba(245,158,11,0.05)', line_width=0)
        fig2.add_vrect(x0=score_seuil, x1=1, fillcolor='rgba(239,68,68,0.05)', line_width=0)
        # Histogram
        fig2.add_trace(go.Histogram(
            x=churn_df['score_churn'], nbinsx=60,
            marker=dict(color='#6366f1', opacity=0.8, line=dict(width=0)),
            hovertemplate='Score : %{x:.2f}<br>Count : %{y}<extra></extra>',
            name='Distribution'
        ))
        fig2.add_vline(x=score_seuil, line=dict(color='#ef4444', width=2, dash='dash'))
        fig2.add_annotation(x=score_seuil, y=0, text=f"Seuil : {score_seuil:.2f}",
                            showarrow=True, font=dict(color='#ef4444', size=11),
                            arrowcolor='#ef4444', yref='paper', ay=-30)
        fig2.update_layout(**CHART_THEME, height=300, margin=dict(l=0,r=0,t=10,b=0),
                           showlegend=False, bargap=0.05)
        fig2.update_xaxes(**CHART_THEME['xaxis'], title_text="Score de churn", range=[0,1])
        fig2.update_yaxes(**CHART_THEME['yaxis'], title_text="Nombre de clients")
        st.plotly_chart(fig2, use_container_width=True)

    # ── Satisfaction vs retard ──
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns([3,2])

    with c1:
        st.markdown('<div class="section-title"><span>⚠️</span> Satisfaction vs Retard de Livraison</div>', unsafe_allow_html=True)
        fig3 = go.Figure()
        fig3.add_vrect(x0=0, x1=60, fillcolor='rgba(239,68,68,0.04)', line_width=0)
        fig3.add_vrect(x0=-30, x1=0, fillcolor='rgba(16,185,129,0.04)', line_width=0)
        fig3.add_vline(x=0, line=dict(color='#6b7280', width=1, dash='dot'))
        fig3.add_annotation(x=0, y=5, text="Date estimée", showarrow=False,
                            font=dict(color='#6b7280', size=10), yanchor='bottom')
        fig3.add_trace(go.Scatter(
            x=sat_df['delivery_delta'], y=sat_df['review_mean'],
            mode='lines', line=dict(color='#6366f1', width=3),
            fill='tozeroy', fillcolor='rgba(99,102,241,0.06)',
            hovertemplate='Δ livraison : %{x}j<br>Score moyen : %{y:.2f}<extra></extra>'
        ))
        fig3.add_annotation(x=10, y=3.7, text="📉 Chaque jour de retard<br>≈ -0.05 point de satisfaction",
                            showarrow=False, font=dict(color='#f59e0b', size=11),
                            bgcolor='rgba(245,158,11,0.1)', bordercolor='#f59e0b', borderwidth=1)
        fig3.update_layout(**CHART_THEME, height=280, margin=dict(l=0,r=0,t=10,b=0), showlegend=False)
        fig3.update_xaxes(**CHART_THEME['xaxis'], title_text="Jours de retard (- = en avance)")
        fig3.update_yaxes(**CHART_THEME['yaxis'], title_text="Note moyenne", range=[1,5.2])
        st.plotly_chart(fig3, use_container_width=True)

    with c2:
        st.markdown('<div class="section-title"><span>👥</span> Segments Clients (RFM K-Means)</div>', unsafe_allow_html=True)

        fig4 = make_subplots(rows=1, cols=3, subplot_titles=['Recency ↓', 'Frequency ↑', 'Monetary ↑'])
        colors_cl = ['#6366f1', '#10b981']
        for i, metric in enumerate(['Recency','Frequency','Monetary']):
            for j, row in rfm_profiles.iterrows():
                fig4.add_trace(go.Bar(
                    x=[row['Cluster'].split('\n')[0]], y=[row[metric]],
                    name=row['Cluster'].split('\n')[0],
                    marker_color=colors_cl[j],
                    showlegend=(i==0),
                    hovertemplate=f'{metric}: %{{y:.1f}}<extra>{row["Cluster"]}</extra>'
                ), row=1, col=i+1)

        fig4.update_layout(**CHART_THEME, height=280, margin=dict(l=0,r=0,t=30,b=0),
                           legend=dict(orientation='h', y=-0.15, font=dict(size=10, color='#94a3b8')))
        for i in range(1,4):
            fig4.update_xaxes(gridcolor='#1e2340', linecolor='#1e2340', row=1, col=i)
            fig4.update_yaxes(gridcolor='#1e2340', linecolor='#1e2340', row=1, col=i)
        st.plotly_chart(fig4, use_container_width=True)

    # ── Stats tests ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title"><span>🧪</span> Tests Statistiques — Résultats</div>', unsafe_allow_html=True)
    t1, t2, t3, t4 = st.columns(4)
    tests = [
        ("Mann-Whitney U", "Livraison tardive vs Satisfaction", "p < 0.0001", "H₀ rejetée", "red",
         "Score moyen : 2.27 (retard) vs 4.29 (à temps)"),
        ("Kruskal-Wallis", "Mode de paiement vs Montant", "p < 0.0001", "H₀ rejetée", "red",
         "Le montant varie significativement selon le mode de paiement"),
        ("Chi²", "Statut commande vs État géo", "p = 3.1e-45", "H₀ rejetée", "red",
         "χ² = 371.20 — Le statut dépend de la région"),
        ("t-test", "1 item vs 2+ items → note", "p < 0.0001", "H₀ rejetée", "red",
         "Moy. 1 item : 4.21 vs 2+ items : 3.63"),
    ]
    for col, (test, desc, pval, result, color, detail) in zip([t1,t2,t3,t4], tests):
        with col:
            st.markdown(f"""
            <div class="insight-box {color}">
                <b>{test}</b><br>
                <span style="color:#94a3b8;font-size:12px">{desc}</span><br><br>
                <span class="badge {'red' if 'rejetée' in result else 'green'}">{result}</span><br>
                <span style="font-size:11px;color:#9ca3af;margin-top:6px;display:block">{pval}</span>
                <span style="font-size:11px;color:#9ca3af">{detail}</span>
            </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
#  PAGE 3 — MODÈLES ML
# ══════════════════════════════════════════════════════════════════════════

elif page == "🤖 Modèles ML":
    st.markdown("## 🤖 Modélisation Prédictive — XGBoost & Interprétabilité")
    st.markdown("*Phase 4 · Feature Engineering + SHAP Values*")
    st.markdown("")

    c1,c2,c3,c4 = st.columns(4)
    with c1: kpi("Meilleur Modèle","XGBoost","optimisé GridSearch","blue","🏆")
    with c2: kpi("AUC-ROC","0.977","+23% vs baseline","green","📈")
    with c3: kpi("F1-Score","0.938","Precision: 0.949","green","⚖️")
    with c4: kpi("Recall","0.927","92.7% churners détectés","yellow","🎯")

    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_r = st.columns([3,2])

    with col_l:
        st.markdown('<div class="section-title"><span>📊</span> Comparaison des 3 Modèles</div>', unsafe_allow_html=True)
        metrics = ['AUC-ROC', 'F1-Score', 'Précision', 'Rappel']
        colors_m = ['#6366f1','#10b981','#ef4444']
        fig = go.Figure()
        for i, row in models_df.iterrows():
            fig.add_trace(go.Bar(
                name=row['Modèle'],
                x=metrics, y=[row[m] for m in metrics],
                marker_color=colors_m[i],
                text=[f"{row[m]:.3f}" for m in metrics],
                textposition='outside',
                textfont=dict(size=10, color='#94a3b8'),
                hovertemplate=f"<b>{row['Modèle']}</b><br>%{{x}} : %{{y:.3f}}<extra></extra>"
            ))
        fig.update_layout(**CHART_THEME, height=350, barmode='group',
                          margin=dict(l=0,r=0,t=10,b=0),
                          legend=dict(orientation='h', y=-0.15, font=dict(size=11, color='#94a3b8')))
        fig.update_xaxes(**CHART_THEME['xaxis'])
        fig.update_yaxes(**CHART_THEME['yaxis'], range=[0,1.1])
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown('<div class="section-title"><span>🔵</span> Courbe ROC (conceptuelle)</div>', unsafe_allow_html=True)
        # Simulated ROC curves
        fpr = np.linspace(0,1,100)
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=[0,1], y=[0,1], mode='lines',
            line=dict(color='#4b5563', dash='dash', width=1), name='Hasard (AUC=0.50)'))

        for name, auc, color in [
            ('Régr. Logistique', 0.749, '#94a3b8'),
            ('Random Forest', 0.971, '#10b981'),
            ('XGBoost', 0.977, '#6366f1'),
        ]:
            tpr = fpr ** ((1-auc)*5 + 0.01)
            fig2.add_trace(go.Scatter(
                x=fpr, y=np.clip(tpr**0.3,0,1) if auc > 0.9 else np.clip(tpr**0.6,0,1),
                mode='lines', line=dict(color=color, width=2.5),
                name=f'{name} (AUC={auc})',
                hovertemplate=f'{name}<br>FPR=%{{x:.2f}}<br>TPR=%{{y:.2f}}<extra></extra>'
            ))
        # XGBoost better curve
        tpr_xgb = np.where(fpr < 0.05, fpr*18, np.minimum(1, 0.9 + fpr*0.1))
        fig2.data[-1].update(y=tpr_xgb)
        tpr_rf = np.where(fpr < 0.08, fpr*11, np.minimum(0.98, 0.88 + fpr*0.1))
        fig2.data[-2].update(y=tpr_rf)

        fig2.update_layout(**CHART_THEME, height=350, margin=dict(l=0,r=0,t=10,b=0),
                           legend=dict(orientation='h', y=-0.2, font=dict(size=10, color='#94a3b8')))
        fig2.update_xaxes(**CHART_THEME['xaxis'], title_text="Taux Faux Positifs", range=[0,1])
        fig2.update_yaxes(**CHART_THEME['yaxis'], title_text="Taux Vrais Positifs", range=[0,1])
        st.plotly_chart(fig2, use_container_width=True)

    # ── SHAP Values ──
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns([2,3])

    with c1:
        st.markdown('<div class="section-title"><span>🧠</span> SHAP — Importance Globale</div>', unsafe_allow_html=True)
        fig3 = go.Figure(go.Bar(
            x=shap_df['importance'], y=shap_df['feature'],
            orientation='h',
            marker=dict(
                color=shap_df['importance'],
                colorscale=[[0,'#1e2340'],[0.5,'#6366f1'],[1,'#8b5cf6']],
                showscale=False,
                line=dict(width=0)
            ),
            text=[f"{v:.2f}" for v in shap_df['importance']],
            textposition='outside',
            textfont=dict(size=10, color='#94a3b8'),
            hovertemplate='%{y}<br>Impact moyen : %{x:.3f}<extra></extra>'
        ))
        fig3.update_layout(**CHART_THEME, height=380, margin=dict(l=0,r=80,t=10,b=0),
                           showlegend=False)
        fig3.update_xaxes(**CHART_THEME['xaxis'], title_text="mean(|SHAP value|)")
        fig3.update_yaxes(**CHART_THEME['yaxis'])
        st.plotly_chart(fig3, use_container_width=True)

    with c2:
        st.markdown('<div class="section-title"><span>💡</span> Interprétation des Leviers SHAP</div>', unsafe_allow_html=True)

        leviers = [
            ("purchase_month", "blue", "🗓️ Mois d'achat (impact #1)",
             "La saisonnalité impacte massivement le churn. Les clients achetant en période creuse (Q1) ont un risque de churn beaucoup plus élevé que ceux achetant pendant les pics (Q4)."),
            ("Cluster_KMeans", "green", "👥 Segment RFM (impact #2)",
             "Les clients du Cluster 0 (Champions, 3% de la base) ont un risque de churn 4x plus faible que le Cluster 1. Cibler la conversion One-shot → Champions est la priorité."),
            ("total_freight", "yellow", "🚚 Coût de livraison (impact #3)",
             "Un coût de fret élevé par rapport au prix produit (freight_ratio > 0.38) augmente significativement le risque de churn. La livraison gratuite sur seuil est recommandée."),
            ("delivery_days + delta", "red", "⏱️ Délai et retard (impact #4-5)",
             "Chaque jour de retard supplémentaire dégrade la satisfaction et augmente le churn. Les livraisons en retard doublent presque le risque de non-retour."),
        ]
        for feature, color, title, body in leviers:
            st.markdown(f"""
            <div class="insight-box {color}">
                <b>{title}</b><br>
                <span style="font-size:12px">{body}</span>
            </div>""", unsafe_allow_html=True)

    # ── Hyperparameters ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title"><span>⚙️</span> Configuration Optimale XGBoost (GridSearchCV)</div>', unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns(5)
    params = [
        ("learning_rate", "0.1", "Vitesse d'apprentissage"),
        ("max_depth", "6", "Profondeur max arbres"),
        ("n_estimators", "200", "Nombre d'arbres"),
        ("CV Folds", "5", "Validation croisée"),
        ("SMOTE", "✓ Actif", "Rééquilibrage classes"),
    ]
    for col, (label, val, desc) in zip([col1,col2,col3,col4,col5], params):
        with col:
            st.markdown(f"""
            <div class="kpi-card blue" style="padding:14px;text-align:center">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value" style="font-size:24px">{val}</div>
                <div class="kpi-delta">{desc}</div>
            </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
#  PAGE 4 — RECOMMANDATIONS
# ══════════════════════════════════════════════════════════════════════════

elif page == "💡 Recommandations":
    st.markdown("## 💡 Recommandations Actionnables")
    st.markdown("*3 leviers prioritaires · Justification quantitative · Impact financier*")
    st.markdown("")

    # ── Business Context ──
    c1,c2,c3,c4 = st.columns(4)
    with c1: kpi("CA Potentiel","R$ 1.5M","+9.4% si churn -10%","green","💎")
    with c2: kpi("Clients Récupérables","9 310","si réduction churn -10%","blue","👥")
    with c3: kpi("Ticket Moyen","R$ 161","par commande","yellow","🛒")
    with c4: kpi("Période Cible","< 90 j","fenêtre d'action","cyan","⚡")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Recommandation 1 ──
    st.markdown("""
    <div class="reco-card">
        <div class="reco-badge">Priorité 1 — Impact Immédiat</div>
        <div class="reco-title">🎯 Programme de Réengagement — Campagne "Retour Privilège"</div>
        <div class="reco-body">
            <b>Problème identifié :</b> 64 211 clients (66.6%) sont en churn avéré (Recency > 180j, Frequency = 1).
            Le modèle XGBoost identifie 10 966 clients en <b>zone rouge</b> (score ≥ 0.70) dans le jeu de test seul.<br><br>
            <b>Action :</b> Lancer une campagne email/push personnalisée ciblant les clients avec score de churn ≥ 0.70
            et Monetary ≥ R$ 100. Offrir un coupon de R$ 20-30 (15-20% du ticket moyen) pour déclencher le 2ème achat.<br><br>
            <b>Segment prioritaire :</b> Cluster 1 (97% des clients) avec Recency entre 90 et 180 jours → <em>fenêtre de réactivation optimale</em>.
        </div>
        <div class="reco-impact">
            💰 Impact estimé : ~9 310 clients récupérés × R$ 161 = <b>R$ 1 499 000 de CA additionnel</b>
            · ROI coupon : 5-7x si taux de conversion ≥ 15%
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Recommandation 2 ──
    st.markdown("""
    <div class="reco-card">
        <div class="reco-badge green">Priorité 2 — Impact Moyen Terme</div>
        <div class="reco-title">🚚 Optimisation Livraison — "Olist Express Garanti"</div>
        <div class="reco-body">
            <b>Problème identifié :</b> La livraison tardive est le 2ème facteur de churn selon les SHAP values.
            Corrélation delivery_delta / review_score : <b>r = -0.39</b> (p < 0.0001).
            Le score de satisfaction chute de 4.29 (à temps) à 2.27 (en retard), soit <b>-47%</b>.<br><br>
            <b>Action :</b> Mettre en place un SLA de livraison de 10 jours max avec alerte proactive (SMS/email)
            dès J+7 si la commande n'est pas livrée. Offrir un bon de R$ 15 automatique si dépassement du délai.<br><br>
            <b>Cible :</b> Réduire le taux de livraisons tardives de 6.8% → ≤ 3% sur les états hors São Paulo (biais géo identifié).
        </div>
        <div class="reco-impact">
            💰 Impact estimé : Chaque point de satisfaction gagné = ~8% de probabilité de rachat en plus.
            Réduire les retards à 3% → économie de ~2 000 compensations/mois + NPS amélioré
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Recommandation 3 ──
    st.markdown("""
    <div class="reco-card">
        <div class="reco-badge yellow">Priorité 3 — Impact Long Terme</div>
        <div class="reco-title">💳 Programme Fidélité Progressif — "Olist+ Loyalty"</div>
        <div class="reco-body">
            <b>Problème identifié :</b> Seuls 3% des clients rachètent (taux de repeat purchase = 3.1%).
            Le Cluster 0 (Champions : Frequency ≥ 2, Monetary = R$ 329) représente 3% de la base mais génère
            une valeur 2x supérieure à la moyenne.<br><br>
            <b>Action :</b> Créer un programme de points par palier :
            R$ 0-100 (Bronze) → R$ 100-300 (Silver) → R$ 300+ (Gold).
            Offrir la livraison gratuite dès R$ 150 de commande (seuil basé sur le 75e percentile = R$ 176).<br><br>
            <b>Métriques de suivi :</b> Taux de repeat purchase (cible : 8% à 6 mois),
            Monetary moyen par cluster, NPS mensuel par segment.
        </div>
        <div class="reco-impact">
            💰 Impact estimé : Doubler le taux de repeat purchase (3.1% → 6%) = +R$ 800 000 CA/an
            · LTV Cluster 0 actuel : R$ 329 vs R$ 160 Cluster 1 → objectif rapprocher C1 de C0
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Impact financier visual ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title"><span>💰</span> Impact Financier Estimé par Levier</div>', unsafe_allow_html=True)

    levier_df = pd.DataFrame({
        'Levier': ['Campagne Réengagement', 'Optimisation Livraison', 'Programme Fidélité'],
        'CA Additionnel (R$)': [1499000, 420000, 800000],
        'Coût Estimé (R$)':    [280000,  150000, 200000],
        'ROI': [5.4, 2.8, 4.0],
        'Délai': ['1-3 mois', '3-6 mois', '6-12 mois'],
        'Priorité': [1, 2, 3],
    })

    fig = go.Figure()
    fig.add_trace(go.Bar(name='CA Additionnel',
        x=levier_df['Levier'], y=levier_df['CA Additionnel (R$)'],
        marker_color='#6366f1',
        text=[f"R$ {v:,.0f}" for v in levier_df['CA Additionnel (R$)']],
        textposition='outside', textfont=dict(size=11, color='#94a3b8'),
        hovertemplate='%{x}<br>CA additionnel : R$ %{y:,.0f}<extra></extra>'
    ))
    fig.add_trace(go.Bar(name='Coût Estimé',
        x=levier_df['Levier'], y=levier_df['Coût Estimé (R$)'],
        marker_color='rgba(239,68,68,0.6)',
        text=[f"R$ {v:,.0f}" for v in levier_df['Coût Estimé (R$)']],
        textposition='outside', textfont=dict(size=11, color='#94a3b8'),
        hovertemplate='%{x}<br>Coût : R$ %{y:,.0f}<extra></extra>'
    ))
    fig.update_layout(**CHART_THEME, height=360, barmode='group',
                      margin=dict(l=0,r=0,t=10,b=0),
                      legend=dict(orientation='h', y=-0.12, font=dict(size=11, color='#94a3b8')))
    fig.update_xaxes(**CHART_THEME['xaxis'])
    fig.update_yaxes(**CHART_THEME['yaxis'], tickprefix='R$ ', tickformat=',.0f')
    st.plotly_chart(fig, use_container_width=True)

    # ROI badges
    r1,r2,r3 = st.columns(3)
    for col, (levier, roi, delai, color) in zip([r1,r2,r3], [
        ("Campagne Réengagement","ROI × 5.4","1-3 mois","green"),
        ("Optimisation Livraison","ROI × 2.8","3-6 mois","yellow"),
        ("Programme Fidélité","ROI × 4.0","6-12 mois","blue"),
    ]):
        with col:
            st.markdown(f"""
            <div class="kpi-card {color}" style="text-align:center">
                <div class="kpi-label">{levier}</div>
                <div class="kpi-value" style="font-size:28px">{roi}</div>
                <div class="kpi-delta">⏱ {delai}</div>
            </div>""", unsafe_allow_html=True)



# ══════════════════════════════════════════════════════════════════════════
#  SÉPARATEUR — skip inactive menu item
# ══════════════════════════════════════════════════════════════════════════

elif page == "─────────────────":
    st.info("Sélectionnez un profil dans la sidebar.")

# ══════════════════════════════════════════════════════════════════════════
#  VUE DIRECTION
# ══════════════════════════════════════════════════════════════════════════

elif page == "🏢 Direction":
    st.markdown("## 🏢 Vue Direction — Synthèse Exécutive")
    st.markdown("*Indicateurs stratégiques · Décisions à fort impact · Vision 6 mois*")
    st.markdown("")

    # ── KPIs stratégiques ──
    c1,c2,c3,c4 = st.columns(4)
    with c1: kpi("CA Total Dataset","R$ 16M","Revenu total 2016–2018","blue","💰")
    with c2: kpi("ROI Potentiel","× 4.5","si campagne réengagement","green","🎯")
    with c3: kpi("Taux de Churn","96.9%","Priorité absolue","red","⚡")
    with c4: kpi("CA Récupérable","R$ 1.5M","+9.4% si churn −10%","yellow","📈")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Résumé des 3 leviers ──
    st.markdown('''<div class="section-title"><span>🎯</span> Synthèse des 3 Leviers Actionnables</div>''', unsafe_allow_html=True)

    levier_df = pd.DataFrame({
        'Levier': ['Campagne Réengagement', 'Optimisation Livraison', 'Programme Fidélité'],
        'CA Additionnel': [1499000, 420000, 800000],
        'Investissement': [280000, 150000, 200000],
        'ROI': ['× 5.4', '× 2.8', '× 4.0'],
        'Délai de retour': ['1–3 mois', '3–6 mois', '6–12 mois'],
        'Priorité': ['🔴 Immédiat', '🟡 Court terme', '🟢 Long terme'],
    })

    st.dataframe(levier_df, use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_r = st.columns([3, 2])

    with col_l:
        st.markdown('''<div class="section-title"><span>💰</span> Impact Financier Cumulé Projeté</div>''', unsafe_allow_html=True)
        fig = go.Figure()
        mois = ['M0','M1','M2','M3','M4','M5','M6','M7','M8','M9','M10','M11','M12']
        ca_base   = [16000]*13
        ca_levier = [16000,16200,16600,17100,17500,17900,18200,18500,18700,18900,19100,19300,19500]
        fig.add_trace(go.Scatter(x=mois, y=ca_base,
            mode='lines', line=dict(color='#4b5563', width=2, dash='dash'),
            name='Trajectoire actuelle (sans action)', fill='tozeroy',
            fillcolor='rgba(75,85,99,0.05)',
            hovertemplate='%{x} : R$ %{y:,}K<extra>Sans action</extra>'))
        fig.add_trace(go.Scatter(x=mois, y=ca_levier,
            mode='lines+markers', line=dict(color='#6366f1', width=3),
            marker=dict(size=5),
            name='Avec les 3 leviers', fill='tonexty',
            fillcolor='rgba(99,102,241,0.1)',
            hovertemplate='%{x} : R$ %{y:,}K<extra>Avec leviers</extra>'))
        fig.add_vrect(x0='M0', x1='M3', fillcolor='rgba(239,68,68,0.04)', line_width=0,
                      annotation_text="Phase 1", annotation_font_color='#ef4444')
        fig.add_vrect(x0='M3', x1='M6', fillcolor='rgba(245,158,11,0.04)', line_width=0,
                      annotation_text="Phase 2", annotation_font_color='#f59e0b')
        fig.add_vrect(x0='M6', x1='M12', fillcolor='rgba(16,185,129,0.04)', line_width=0,
                      annotation_text="Phase 3", annotation_font_color='#10b981')
        fig.update_layout(**CHART_THEME, height=300, margin=dict(l=0,r=0,t=20,b=0),
            legend=dict(orientation='h', y=-0.15, font=dict(size=11, color='#94a3b8')))
        fig.update_xaxes(**CHART_THEME['xaxis'], title_text="Horizon")
        fig.update_yaxes(**CHART_THEME['yaxis'], tickprefix='R$ ', tickformat=',', title_text="CA (K R$)")
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown('''<div class="section-title"><span>📊</span> Répartition du ROI par Levier</div>''', unsafe_allow_html=True)
        fig2 = go.Figure(go.Pie(
            labels=['Réengagement', 'Livraison', 'Fidélité'],
            values=[1499000, 420000, 800000],
            hole=0.55,
            marker=dict(colors=['#6366f1','#f59e0b','#10b981']),
            textfont=dict(size=11, color='white'),
            hovertemplate='%{label}<br>R$ %{value:,.0f}<br>%{percent}<extra></extra>'
        ))
        fig2.add_annotation(text="R$ 2.7M<br><span style='font-size:10px'>potentiel total</span>",
            x=0.5, y=0.5, showarrow=False, font=dict(size=13, color='#f1f5f9'))
        fig2.update_layout(**CHART_THEME, height=300, margin=dict(l=0,r=0,t=20,b=0),
            showlegend=True, legend=dict(orientation='h', y=-0.05, font=dict(size=10, color='#94a3b8')))
        st.plotly_chart(fig2, use_container_width=True)

    # ── Business case ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('''<div class="section-title"><span>📋</span> Points d'Attention Direction</div>''', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('''<div class="insight-box red">
        ⚠️ <b>Risque critique</b><br>96.9% des clients ne rachètent jamais.
        Sans action corrective, la croissance repose uniquement sur l'acquisition de nouveaux clients
        — coût 5× supérieur à la rétention.</div>''', unsafe_allow_html=True)
    with c2:
        st.markdown('''<div class="insight-box yellow">
        📍 <b>Concentration géographique</b><br>São Paulo = 42% des clients.
        Opportunité de croissance forte dans les États sous-représentés
        (MG, RS, PR) avec des coûts logistiques déjà absorbés.</div>''', unsafe_allow_html=True)
    with c3:
        st.markdown('''<div class="insight-box green">
        ✅ <b>Modèle ML opérationnel</b><br>XGBoost (AUC = 0.977) prêt à scorer
        en production. Chaque client reçoit un score de churn exploitable
        par les équipes Marketing et CRM dès aujourd'hui.</div>''', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
#  VUE OPÉRATIONS
# ══════════════════════════════════════════════════════════════════════════

elif page == "⚙️ Opérations":
    st.markdown("## ⚙️ Vue Opérations — Logistique & Qualité de Service")
    st.markdown("*Délais de livraison · Taux de retard · Satisfaction client · Actions terrain*")
    st.markdown("")

    # ── KPIs ops ──
    c1,c2,c3,c4 = st.columns(4)
    with c1: kpi("Délai Moyen","12.1 jours","médiane : 10j","blue","🚚")
    with c2: kpi("Livraisons Retard","6.8%","objectif : ≤ 3%","red","⏰")
    with c3: kpi("Score Satisfaction","4.16 / 5","retard → 2.27/5","yellow","⭐")
    with c4: kpi("Impact Retard","-47%","satisfaction si retard","red","📉")

    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_r = st.columns([3,2])

    with col_l:
        st.markdown('''<div class="section-title"><span>📦</span> Satisfaction vs Retard de Livraison</div>''', unsafe_allow_html=True)
        fig = go.Figure()
        delta = np.arange(-30, 61)
        review = np.where(delta < 0, 4.5 - 0.01*np.abs(delta),
                          np.maximum(1.0, 4.3 - 0.055*delta))
        # Zones
        fig.add_vrect(x0=-30, x1=0, fillcolor='rgba(16,185,129,0.06)', line_width=0,
                      annotation_text="En avance ✓", annotation_position="top left",
                      annotation_font_color='#10b981', annotation_font_size=10)
        fig.add_vrect(x0=0, x1=7, fillcolor='rgba(245,158,11,0.06)', line_width=0,
                      annotation_text="Retard modéré", annotation_position="top left",
                      annotation_font_color='#f59e0b', annotation_font_size=10)
        fig.add_vrect(x0=7, x1=60, fillcolor='rgba(239,68,68,0.06)', line_width=0,
                      annotation_text="Retard critique ✗", annotation_position="top left",
                      annotation_font_color='#ef4444', annotation_font_size=10)
        fig.add_vline(x=0, line=dict(color='#6b7280', width=1, dash='dot'))
        fig.add_trace(go.Scatter(x=delta, y=review, mode='lines',
            line=dict(color='#6366f1', width=3),
            hovertemplate='Δ : %{x}j<br>Score : %{y:.2f}<extra></extra>'))
        fig.add_annotation(x=15, y=2.5,
            text="−0.055 pts/jour de retard",
            showarrow=True, arrowhead=2, arrowcolor='#ef4444',
            font=dict(color='#ef4444', size=11))
        fig.update_layout(**CHART_THEME, height=300, margin=dict(l=0,r=0,t=20,b=0), showlegend=False)
        fig.update_xaxes(**CHART_THEME['xaxis'], title_text="Jours de retard (négatif = en avance)")
        fig.update_yaxes(**CHART_THEME['yaxis'], title_text="Note moyenne (1–5)", range=[1, 5.2])
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown('''<div class="section-title"><span>🗺️</span> Taux de Retard par Segment</div>''', unsafe_allow_html=True)
        seg_data = pd.DataFrame({
            'Segment': ['SP (São Paulo)', 'RJ (Rio)', 'MG (Minas)', 'RS (Rio Grande)', 'Autres États'],
            'Retard (%)': [5.1, 7.2, 8.4, 9.1, 11.3],
            'Volume': [42, 12, 11, 5, 30]
        })
        fig2 = go.Figure(go.Bar(
            x=seg_data['Retard (%)'], y=seg_data['Segment'],
            orientation='h',
            marker=dict(color=['#10b981','#f59e0b','#f97316','#ef4444','#dc2626']),
            text=[f"{v:.1f}%" for v in seg_data['Retard (%)']],
            textposition='outside',
            hovertemplate='%{y}<br>Retard : %{x:.1f}%<extra></extra>'
        ))
        fig2.add_vline(x=6.8, line=dict(color='#6b7280', dash='dash', width=1.5))
        fig2.add_annotation(x=6.8, y=4.5, text="Moy. 6.8%",
            font=dict(color='#94a3b8', size=10), showarrow=False)
        fig2.update_layout(**CHART_THEME, height=300, margin=dict(l=0,r=60,t=20,b=0), showlegend=False)
        fig2.update_xaxes(**CHART_THEME['xaxis'], title_text="Taux de retard (%)")
        fig2.update_yaxes(**CHART_THEME['yaxis'])
        st.plotly_chart(fig2, use_container_width=True)

    # ── Actions ops ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('''<div class="section-title"><span>🔧</span> Plan d'Action Opérationnel</div>''', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    actions_ops = [
        ("🚚 SLA 10 jours max", "yellow",
         "Mettre en place un SLA de livraison de 10 jours maximum pour tous les États. "
         "Alerte automatique à J+7 si la commande n'est pas livrée.",
         "Cible : taux de retard ≤ 3% à 6 mois"),
        ("📩 Notification proactive", "blue",
         "Envoyer un email/SMS au client dès J+7 si livraison non confirmée. "
         "Proposer un bon de R$ 15 automatique en cas de dépassement du délai estimé.",
         "Impact : NPS +0.3 pts estimé"),
        ("📍 Priorité États distants", "red",
         "RS, SC, PA affichent les taux de retard les plus élevés (>9%). "
         "Négocier des accords logistiques spécifiques avec des transporteurs régionaux.",
         "Cible : réduire retards hors SP/RJ de 11% → 5%"),
    ]
    for col, (titre, color, body, impact) in zip([c1,c2,c3], actions_ops):
        with col:
            st.markdown(f'''<div class="insight-box {color}">
                <b>{titre}</b><br><br>
                <span style="font-size:13px">{body}</span><br><br>
                <span style="color:#10b981;font-size:12px;font-weight:600">📊 {impact}</span>
            </div>''', unsafe_allow_html=True)

    # ── Test stats résumé ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('''<div class="section-title"><span>🧪</span> Résultats Test Statistique — Livraison & Satisfaction</div>''', unsafe_allow_html=True)
    st.markdown('''<div class="insight-box red">
        <b>Mann-Whitney U · p-value &lt; 0.0001</b> — H₀ rejetée<br>
        Score moyen <b>en retard : 2.27 / 5</b> vs <b>à temps : 4.29 / 5</b> → écart de <b>−47%</b>.
        La livraison tardive dégrade significativement la satisfaction et augmente le risque de churn de façon mesurable.
    </div>''', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
#  VUE MARKETING
# ══════════════════════════════════════════════════════════════════════════

elif page == "📣 Marketing":
    st.markdown("## 📣 Vue Marketing — Segmentation & Ciblage")
    st.markdown("*Segments RFM · Scores de churn · Ciblage campagnes · Comportement d'achat*")
    st.markdown("")

    # ── KPIs marketing ──
    c1,c2,c3,c4 = st.columns(4)
    with c1: kpi("Clients Zone Rouge","10 966","score churn ≥ 0.70","red","🔴")
    with c2: kpi("Champions (C0)","2 810","3% · LTV R$ 329","green","👑")
    with c3: kpi("One-shot (C1)","90 548","97% · LTV R$ 160","yellow","👤")
    with c4: kpi("Fenêtre Réactivation","90–180j","Recency optimale","blue","⏱️")

    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_r = st.columns([2,3])

    with col_l:
        st.markdown('''<div class="section-title"><span>🎯</span> Ciblage par Zone de Risque</div>''', unsafe_allow_html=True)
        zones = pd.DataFrame({
            'Zone': ['🔴 Haut risque', '🟡 Modéré', '🟢 Faible risque'],
            'Score': ['≥ 0.70', '0.40–0.70', '< 0.40'],
            'Clients': [10966, 2106, 6093],
            'Action': ['Coupon R$ 25 immédiat', 'Email nurturing J+15', 'Programme fidélité'],
            'Priorité': [1, 2, 3],
        })
        fig = go.Figure(go.Bar(
            x=['Zone Rouge', 'Zone Jaune', 'Zone Verte'],
            y=[10966, 2106, 6093],
            marker=dict(color=['#ef4444','#f59e0b','#10b981']),
            text=['10 966', '2 106', '6 093'],
            textposition='outside',
            hovertemplate='%{x}<br>%{y:,} clients<extra></extra>'
        ))
        fig.update_layout(**CHART_THEME, height=260, margin=dict(l=0,r=0,t=20,b=0), showlegend=False)
        fig.update_xaxes(**CHART_THEME['xaxis'])
        fig.update_yaxes(**CHART_THEME['yaxis'], title_text="Nombre de clients")
        st.plotly_chart(fig, use_container_width=True)

        # Table ciblage
        st.dataframe(zones[['Zone','Score','Action']], use_container_width=True, hide_index=True)

    with col_r:
        st.markdown('''<div class="section-title"><span>👥</span> Profil RFM des Segments</div>''', unsafe_allow_html=True)
        fig2 = make_subplots(rows=1, cols=3,
            subplot_titles=['Recency moy. (j)', 'Frequency moy.', 'Monetary moy. (R$)'])
        metrics_vals = {
            'Recency': [269.6, 287.7],
            'Frequency': [2.11, 1.00],
            'Monetary': [329.5, 160.1]
        }
        colors_seg = ['#6366f1', '#94a3b8']
        labels_seg = ['C0 — Champions', 'C1 — One-shot']
        for i, (metric, vals) in enumerate(metrics_vals.items()):
            for j, (val, color, label) in enumerate(zip(vals, colors_seg, labels_seg)):
                fig2.add_trace(go.Bar(
                    x=[label], y=[val],
                    marker_color=color,
                    showlegend=(i==0),
                    name=label,
                    text=[f"{val:.1f}"],
                    textposition='outside',
                    hovertemplate=f'{metric} : %{{y:.1f}}<extra>{label}</extra>'
                ), row=1, col=i+1)
        fig2.update_layout(**CHART_THEME, height=300, margin=dict(l=0,r=0,t=30,b=0),
            legend=dict(orientation='h', y=-0.15, font=dict(size=10, color='#94a3b8')))
        for i in range(1,4):
            fig2.update_xaxes(gridcolor='#1e2340', linecolor='#1e2340', row=1, col=i, showticklabels=False)
            fig2.update_yaxes(gridcolor='#1e2340', linecolor='#1e2340', row=1, col=i)
        st.plotly_chart(fig2, use_container_width=True)

    # ── Comportement temporel ──
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        st.markdown('''<div class="section-title"><span>🕐</span> Meilleurs Créneaux pour Campagnes Email</div>''', unsafe_allow_html=True)
        hours_mkt = pd.DataFrame({
            'heure': list(range(24)),
            'count': [100,60,40,30,50,200,900,2800,4200,5000,
                      5800,6000,5900,6100,5800,5600,5700,6200,
                      6800,7000,6900,6200,5100,3200]
        })
        peak_color = ['#6366f1' if 18<=h<=22 else ('#8b5cf6' if 11<=h<=13 else '#1e2340')
                      for h in hours_mkt['heure']]
        fig3 = go.Figure(go.Bar(
            x=hours_mkt['heure'], y=hours_mkt['count'],
            marker_color=peak_color,
            hovertemplate='%{x}h : %{y:,} commandes<extra></extra>'
        ))
        fig3.add_annotation(x=19.5, y=7200,
            text="🎯 Pic 18h–22h<br>Envoyer les emails ici",
            showarrow=False, font=dict(color='#6366f1', size=10),
            bgcolor='rgba(99,102,241,0.1)', bordercolor='#6366f1', borderwidth=1)
        fig3.update_layout(**CHART_THEME, height=260, margin=dict(l=0,r=0,t=10,b=0), showlegend=False)
        fig3.update_xaxes(**CHART_THEME['xaxis'], title_text="Heure (0–23h)")
        fig3.update_yaxes(**CHART_THEME['yaxis'])
        st.plotly_chart(fig3, use_container_width=True)

    with c2:
        st.markdown('''<div class="section-title"><span>📅</span> Volume par Jour — Planification Campagnes</div>''', unsafe_allow_html=True)
        dow_mkt = pd.DataFrame({
            'jour': ['Lun','Mar','Mer','Jeu','Ven','Sam','Dim'],
            'count': [15800,15400,14900,14700,14500,10800,13300],
            'recommande': [True,True,False,False,False,False,False]
        })
        bar_colors = ['#6366f1' if r else '#1e2340' for r in dow_mkt['recommande']]
        fig4 = go.Figure(go.Bar(
            x=dow_mkt['jour'], y=dow_mkt['count'],
            marker_color=bar_colors,
            hovertemplate='%{x} : %{y:,} commandes<extra></extra>'
        ))
        fig4.add_annotation(x=0.5, y=16500,
            text="🎯 Lun & Mar : pic d'activité",
            showarrow=False, font=dict(color='#6366f1', size=10),
            bgcolor='rgba(99,102,241,0.1)', bordercolor='#6366f1', borderwidth=1)
        fig4.update_layout(**CHART_THEME, height=260, margin=dict(l=0,r=0,t=10,b=0), showlegend=False)
        fig4.update_xaxes(**CHART_THEME['xaxis'])
        fig4.update_yaxes(**CHART_THEME['yaxis'])
        st.plotly_chart(fig4, use_container_width=True)

    # ── Plan de ciblage ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('''<div class="section-title"><span>📬</span> Plan de Ciblage par Segment</div>''', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    campagnes = [
        ("🔴 Segment Rouge", "red",
         "Score ≥ 0.70 · Inactifs 90–180j",
         "Coupon R$ 25 — Email lundi 19h + relance SMS J+3",
         "10 966 clients · Budget R$ 274K · ROI × 4.5"),
        ("🟡 Segment Jaune", "yellow",
         "Score 0.40–0.70 · Inactifs 60–90j",
         "Email nurturing sans coupon — contenu personnalisé basé sur la dernière catégorie achetée",
         "2 106 clients · Budget R$ 0 · Objectif : score ↓"),
        ("👑 Segment Champions", "green",
         "Cluster 0 · Frequency ≥ 2 · Monetary ≥ R$ 300",
         "Programme Olist+ Gold — livraison gratuite + accès ventes privées + points fidélité",
         "2 810 clients · LTV cible : R$ 500 · Ambassadeurs"),
    ]
    for col, (titre, color, cible, action, impact) in zip([c1,c2,c3], campagnes):
        with col:
            st.markdown(f'''<div class="insight-box {color}">
                <b>{titre}</b><br>
                <span style="font-size:11px;color:#94a3b8">{cible}</span><br><br>
                <span style="font-size:13px">{action}</span><br><br>
                <span style="color:#10b981;font-size:11px;font-weight:600">📊 {impact}</span>
            </div>''', unsafe_allow_html=True)