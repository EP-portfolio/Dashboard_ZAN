# -*- coding: utf-8 -*-
"""
DASHBOARD DE PILOTAGE ZAN - Application Principale
===================================================
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent))

from components.header import render_header, render_section_header
from components.kpis import render_kpis
from components.charts import (
    render_evolution_chart,
    render_repartition_chart,
    render_top_communes_chart,
    render_trajectory_chart,
)
from components.filters import render_filters
from components.tables import render_data_table
from utils.data_loader import load_data
from utils.calculations import calculate_zan_metrics
from utils.metadata import get_data_source_text, get_data_source_html, get_footer_text, get_data_last_update

# Configuration
st.set_page_config(
    page_title="Dashboard ZAN - Pilotage Artificialisation",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS
def load_css():
    css_file = Path(__file__).parent / "assets" / "styles.css"
    if css_file.exists():
        with open(css_file, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Données
@st.cache_data(ttl=3600)
def get_data():
    return load_data()

try:
    df_scot, df_cc = get_data()
    data_loaded = True
except Exception as e:
    st.error(f"Erreur lors du chargement des donnees : {e}")
    data_loaded = False

# Interface principale
if data_loaded:
    render_header()
    
    # Sidebar
    with st.sidebar:
        st.markdown('''
<div style="text-align: center; margin-bottom: 1.5rem;">
<span style="font-size: 3rem;">🏗️</span>
<div style="color: #1E3A5F; margin-top: 0.5rem; font-size: 1.1rem; font-weight: 700;">Dashboard ZAN</div>
</div>
''', unsafe_allow_html=True)
        
        filters = render_filters(df_scot, df_cc)
    
    # Sélection périmètre
    if filters["perimetre"] == "SCoT Rives du Rhône":
        df_filtered = df_scot.copy()
        titre_perimetre = "SCoT des Rives du Rhone"
    else:
        df_filtered = df_cc.copy()
        titre_perimetre = "CC Porte de DromeArdeche"
    
    # Filtres
    if filters.get("communes"):
        df_filtered = df_filtered[df_filtered["idcomtxt"].isin(filters["communes"])]
    if filters.get("departements"):
        df_filtered = df_filtered[df_filtered["iddeptxt"].isin(filters["departements"])]
    
    # Métriques
    metrics = calculate_zan_metrics(df_filtered)
    
    # SECTION 1: KPIs
    render_section_header(f"Indicateurs Cles - {titre_perimetre}", icon="📊", description="Vue synthetique des principaux indicateurs de suivi ZAN")
    render_kpis(metrics)
    
    # SECTION 2: Trajectoire ZAN
    render_section_header("Trajectoire vers l objectif ZAN 2031", icon="📈", description="Suivi de la consommation d espaces par rapport a l objectif de reduction de 50%")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        render_trajectory_chart(df_filtered, metrics)
    
    with col2:
        # Objectif
        html_obj = f'''
<div style="background: linear-gradient(135deg, #FFFBEB 0%, #FEF3E2 100%); border: 1px solid #F6AD55; border-left: 4px solid #D4820A; border-radius: 12px; padding: 1.25rem; margin-bottom: 1rem;">
<div style="color: #744210; margin-bottom: 1rem; font-size: 1rem; font-weight: 700;">🎯 Objectif -50% (Loi Climat)</div>
<table style="width: 100%; border-collapse: collapse;">
<tr><td style="color: #744210; font-size: 0.85rem; padding: 0.4rem 0; border-bottom: 1px solid #ECC94B;">Periode reference</td><td style="color: #744210; font-weight: 700; text-align: right; padding: 0.4rem 0; border-bottom: 1px solid #ECC94B;">2011-2021</td></tr>
<tr><td style="color: #744210; font-size: 0.85rem; padding: 0.4rem 0; border-bottom: 1px solid #ECC94B;">Conso. reference</td><td style="color: #744210; font-weight: 700; text-align: right; padding: 0.4rem 0; border-bottom: 1px solid #ECC94B;">{metrics['conso_reference']:.1f} ha</td></tr>
<tr><td style="color: #744210; font-size: 0.85rem; padding: 0.4rem 0; border-bottom: 1px solid #ECC94B;">Enveloppe 2021-2031</td><td style="color: #744210; font-weight: 700; text-align: right; padding: 0.4rem 0; border-bottom: 1px solid #ECC94B;">{metrics['enveloppe_zan']:.1f} ha</td></tr>
<tr><td style="color: #744210; font-size: 0.85rem; padding: 0.4rem 0; border-bottom: 1px solid #ECC94B;">Deja consomme (21-24)</td><td style="color: #744210; font-weight: 700; text-align: right; padding: 0.4rem 0; border-bottom: 1px solid #ECC94B;">{metrics['conso_2021_2024']:.1f} ha</td></tr>
<tr><td style="color: #744210; font-size: 0.85rem; font-weight: 600; padding: 0.4rem 0;">Reste disponible</td><td style="color: #1D7A4B; font-weight: 800; font-size: 1.1rem; text-align: right; padding: 0.4rem 0;">{metrics['reste_disponible']:.1f} ha</td></tr>
</table>
</div>
'''
        st.markdown(html_obj, unsafe_allow_html=True)
        
        # Jauge
        progress = min(metrics['conso_2021_2024'] / metrics['enveloppe_zan'] * 100, 100) if metrics['enveloppe_zan'] > 0 else 0
        
        if progress < 30:
            progress_color = "#1D7A4B"
            status_text = "Trajectoire maitrisee"
        elif progress < 50:
            progress_color = "#D4820A"
            status_text = "Vigilance recommandee"
        else:
            progress_color = "#C53030"
            status_text = "Attention: risque de depassement"
        
        html_gauge = f'''
<div style="background: white; border: 1px solid #E2E8F0; border-radius: 10px; padding: 1rem;">
<table style="width: 100%; margin-bottom: 0.5rem;"><tr>
<td style="color: #4A5568; font-size: 0.85rem; font-weight: 600;">Progression</td>
<td style="color: {progress_color}; font-weight: 700; text-align: right;">{progress:.1f}%</td>
</tr></table>
<div style="background: #E2E8F0; border-radius: 10px; height: 12px; overflow: hidden;">
<div style="background: {progress_color}; height: 100%; width: {progress}%; border-radius: 10px;"></div>
</div>
<div style="color: #718096; font-size: 0.75rem; margin-top: 0.5rem; text-align: center;">{status_text}</div>
</div>
'''
        st.markdown(html_gauge, unsafe_allow_html=True)
    
    # SECTION 3: Graphiques
    render_section_header("Analyse Detaillee", icon="📊", description="Exploration approfondie des donnees d artificialisation")
    
    tab1, tab2, tab3 = st.tabs(["📈 Evolution Annuelle", "🥧 Repartition par Destination", "🏆 Top Communes"])
    
    with tab1:
        render_evolution_chart(df_filtered)
    
    with tab2:
        render_repartition_chart(metrics)
    
    with tab3:
        render_top_communes_chart(df_filtered, n_top=10)
    
    # SECTION 4: Tableau
    render_section_header("Donnees par Commune", icon="📋", description="Tableau detaille avec options de recherche, tri et export")
    render_data_table(df_filtered)
    
    # Footer avec métadonnées
    footer_text = get_footer_text()
    st.markdown(f'''
<div style="background: linear-gradient(135deg, #F7FAFC 0%, #EDF2F7 100%); border-radius: 10px; padding: 1rem 1.5rem; margin-top: 2rem; text-align: center; border: 1px solid #E2E8F0;">
<div style="color: #718096; font-size: 0.85rem; margin-bottom: 0.5rem;"><strong>Dashboard ZAN</strong> - Suivi de l'artificialisation des sols</div>
<div style="color: #718096; font-size: 0.75rem; font-style: italic;">{footer_text}</div>
</div>
''', unsafe_allow_html=True)

else:
    st.markdown('''
<div style="background: linear-gradient(135deg, #FEE7E7 0%, #FFF5F5 100%); border: 1px solid #FC8181; border-left: 4px solid #C53030; border-radius: 12px; padding: 2rem; text-align: center;">
<span style="font-size: 3rem;">⚠️</span>
<div style="color: #C53030; margin: 1rem 0 0.5rem 0; font-size: 1.2rem; font-weight: 700;">Impossible de charger les donnees</div>
<div style="color: #742A2A;">Verifiez que les fichiers CSV sont presents dans le dossier parent.</div>
</div>
''', unsafe_allow_html=True)
