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
    page_icon="📊",
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
    render_section_header(f"Indicateurs Clés - {titre_perimetre}", icon="", description="Vue synthétique des principaux indicateurs de suivi ZAN")
    render_kpis(metrics)
    
    # SECTION 2: Trajectoire ZAN
    render_section_header("Trajectoire vers l'objectif ZAN 2031", icon="", description="Suivi de la consommation d'espaces par rapport à l'objectif de réduction de 50%")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        render_trajectory_chart(df_filtered, metrics)
    
    with col2:
        # Objectif
        html_obj = f'''
<div style="background: #1E293B; border: 1px solid #334155; border-left: 4px solid #ED8936; border-radius: 8px; padding: 1.5rem; margin-bottom: 1rem; box-shadow: 0 2px 8px rgba(0,0,0,0.3);">
<div style="color: #FFFFFF; margin-bottom: 1.25rem; font-size: 1rem; font-weight: 700; letter-spacing: -0.3px; border-bottom: 1px solid #334155; padding-bottom: 0.75rem;">OBJECTIF -50% (LOI CLIMAT ET RÉSILIENCE)</div>
<table style="width: 100%; border-collapse: collapse;">
<tr><td style="color: #94A3B8; font-size: 0.85rem; padding: 0.5rem 0; border-bottom: 1px solid #334155; font-weight: 500;">Période de référence</td><td style="color: #FFFFFF; font-weight: 600; text-align: right; padding: 0.5rem 0; border-bottom: 1px solid #334155; font-family: 'Segoe UI', Arial, sans-serif;">2011-2021</td></tr>
<tr><td style="color: #94A3B8; font-size: 0.85rem; padding: 0.5rem 0; border-bottom: 1px solid #334155; font-weight: 500;">Consommation de référence</td><td style="color: #FFFFFF; font-weight: 600; text-align: right; padding: 0.5rem 0; border-bottom: 1px solid #334155; font-family: 'Segoe UI', Arial, sans-serif;">{metrics['conso_reference']:.1f} ha</td></tr>
<tr><td style="color: #94A3B8; font-size: 0.85rem; padding: 0.5rem 0; border-bottom: 1px solid #334155; font-weight: 500;">Enveloppe 2021-2031</td><td style="color: #FFFFFF; font-weight: 600; text-align: right; padding: 0.5rem 0; border-bottom: 1px solid #334155; font-family: 'Segoe UI', Arial, sans-serif;">{metrics['enveloppe_zan']:.1f} ha</td></tr>
<tr><td style="color: #94A3B8; font-size: 0.85rem; padding: 0.5rem 0; border-bottom: 1px solid #334155; font-weight: 500;">Déjà consommé (2021-2024)</td><td style="color: #FFFFFF; font-weight: 600; text-align: right; padding: 0.5rem 0; border-bottom: 1px solid #334155; font-family: 'Segoe UI', Arial, sans-serif;">{metrics['conso_2021_2024']:.1f} ha</td></tr>
<tr><td style="color: #94A3B8; font-size: 0.85rem; font-weight: 600; padding: 0.5rem 0;">Reste disponible</td><td style="color: #48BB78; font-weight: 700; font-size: 1.1rem; text-align: right; padding: 0.5rem 0; font-family: 'Segoe UI', Arial, sans-serif;">{metrics['reste_disponible']:.1f} ha</td></tr>
</table>
</div>
'''
        st.markdown(html_obj, unsafe_allow_html=True)
        
        # Jauge
        progress = min(metrics['conso_2021_2024'] / metrics['enveloppe_zan'] * 100, 100) if metrics['enveloppe_zan'] > 0 else 0
        
        if progress < 30:
            progress_color = "#48BB78"
            status_text = "Trajectoire maîtrisée"
        elif progress < 50:
            progress_color = "#ED8936"
            status_text = "Vigilance recommandée"
        else:
            progress_color = "#F56565"
            status_text = "Attention : risque de dépassement"
        
        html_gauge = f'''
<div style="background: #1E293B; border: 1px solid #334155; border-radius: 8px; padding: 1.25rem; box-shadow: 0 2px 8px rgba(0,0,0,0.3);">
<table style="width: 100%; margin-bottom: 0.75rem;"><tr>
<td style="color: #94A3B8; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Progression</td>
<td style="color: {progress_color}; font-weight: 700; text-align: right; font-size: 1.1rem; font-family: 'Segoe UI', Arial, sans-serif;">{progress:.1f}%</td>
</tr></table>
<div style="background: #0F172A; border: 1px solid #334155; border-radius: 8px; height: 14px; overflow: hidden;">
<div style="background: linear-gradient(90deg, {progress_color} 0%, {progress_color}dd 100%); height: 100%; width: {progress}%; border-radius: 8px; transition: width 0.3s ease;"></div>
</div>
<div style="color: #64748B; font-size: 0.75rem; margin-top: 0.75rem; text-align: center; font-weight: 500;">{status_text}</div>
</div>
'''
        st.markdown(html_gauge, unsafe_allow_html=True)
    
    # SECTION 3: Graphiques
    render_section_header("Analyse Détaillée", icon="", description="Exploration approfondie des données d'artificialisation")
    
    tab1, tab2, tab3 = st.tabs(["Évolution Annuelle", "Répartition par Destination", "Top Communes"])
    
    with tab1:
        render_evolution_chart(df_filtered)
    
    with tab2:
        render_repartition_chart(metrics)
    
    with tab3:
        render_top_communes_chart(df_filtered, n_top=10)
    
    # SECTION 4: Tableau
    render_section_header("Données par Commune", icon="", description="Tableau détaillé avec options de recherche, tri et export")
    render_data_table(df_filtered)
    
    # Footer avec métadonnées
    footer_text = get_footer_text()
    st.markdown(f'''
<div style="background: #1E293B; border-top: 2px solid #334155; padding: 1.5rem 2rem; margin-top: 3rem; text-align: center;">
<div style="color: #FFFFFF; font-size: 0.9rem; margin-bottom: 0.5rem; font-weight: 600; letter-spacing: 0.3px;">DASHBOARD DE PILOTAGE ZAN</div>
<div style="color: #94A3B8; font-size: 0.8rem; margin-bottom: 0.75rem;">Suivi de l'artificialisation des sols - Objectif Zéro Artificialisation Nette</div>
<div style="color: #64748B; font-size: 0.75rem; font-style: italic; border-top: 1px solid #334155; padding-top: 0.75rem; margin-top: 0.75rem;">{footer_text}</div>
</div>
''', unsafe_allow_html=True)

else:
    st.markdown('''
<div style="background: #1E293B; border: 1px solid #F56565; border-left: 4px solid #F56565; border-radius: 8px; padding: 2rem; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.3);">
<div style="color: #F56565; margin-bottom: 1rem; font-size: 1.5rem; font-weight: 700; letter-spacing: -0.3px;">ERREUR DE CHARGEMENT DES DONNÉES</div>
<div style="color: #94A3B8; font-size: 0.9rem; line-height: 1.6;">Vérifiez que les fichiers CSV sont présents dans le dossier parent et que les permissions d'accès sont correctes.</div>
</div>
''', unsafe_allow_html=True)
