# -*- coding: utf-8 -*-
"""
Composant Filtres du Dashboard - Version corrigée
"""

import streamlit as st
import pandas as pd


def render_filters(df_scot: pd.DataFrame, df_cc: pd.DataFrame) -> dict:
    """
    Affiche les filtres dans la sidebar
    """
    
    filters = {}
    
    # Périmètre
    st.markdown('''
<div style="background: linear-gradient(135deg, #1E3A5F 0%, #2E5A8F 100%); border-radius: 10px; padding: 0.75rem 1rem; margin-bottom: 1rem;">
<span style="color: white; font-weight: 600; font-size: 0.9rem;">🗺️ Perimetre d etude</span>
</div>
''', unsafe_allow_html=True)
    
    filters["perimetre"] = st.radio(
        "Territoire",
        options=["SCoT Rives du Rhône", "CC Porte de DrômArdèche"],
        index=0,
        label_visibility="collapsed",
    )
    
    # DataFrame selon périmètre
    df = df_scot if filters["perimetre"] == "SCoT Rives du Rhône" else df_cc
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Département
    st.markdown('''
<div style="background: #F7FAFC; border-radius: 8px; padding: 0.6rem 0.9rem; margin-bottom: 0.5rem; border-left: 3px solid #2E86AB;">
<span style="color: #1E3A5F; font-weight: 600; font-size: 0.85rem;">🏛️ Departement</span>
</div>
''', unsafe_allow_html=True)
    
    departements = sorted(df["iddeptxt"].unique().tolist())
    filters["departements"] = st.multiselect(
        "Departements",
        options=departements,
        default=[],
        placeholder="Tous les departements",
        label_visibility="collapsed",
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Communes
    st.markdown('''
<div style="background: #F7FAFC; border-radius: 8px; padding: 0.6rem 0.9rem; margin-bottom: 0.5rem; border-left: 3px solid #A23B72;">
<span style="color: #1E3A5F; font-weight: 600; font-size: 0.85rem;">🏘️ Communes</span>
</div>
''', unsafe_allow_html=True)
    
    if filters["departements"]:
        communes_disponibles = df[df["iddeptxt"].isin(filters["departements"])]["idcomtxt"].unique()
    else:
        communes_disponibles = df["idcomtxt"].unique()
    
    communes_disponibles = sorted(communes_disponibles)
    
    filters["communes"] = st.multiselect(
        "Communes",
        options=communes_disponibles,
        default=[],
        placeholder="Toutes les communes",
        label_visibility="collapsed",
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Typologie AAV
    st.markdown('''
<div style="background: #F7FAFC; border-radius: 8px; padding: 0.6rem 0.9rem; margin-bottom: 0.5rem; border-left: 3px solid #1D7A4B;">
<span style="color: #1E3A5F; font-weight: 600; font-size: 0.85rem;">🌆 Typologie Urbaine</span>
</div>
''', unsafe_allow_html=True)
    
    typo_labels = {
        "11": "Pole principal",
        "12": "Couronne grande aire",
        "20": "Petite/moyenne aire",
        "30": "Hors attraction",
    }
    
    typologies = df["aav2020_typo"].astype(str).unique()
    typo_options = [typo_labels.get(t, f"Type {t}") for t in typologies if t in typo_labels]
    
    filters["typologies"] = st.multiselect(
        "Typologies",
        options=typo_options,
        default=[],
        placeholder="Toutes les typologies",
        label_visibility="collapsed",
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Résumé de la sélection
    df_filtered = df.copy()
    if filters["departements"]:
        df_filtered = df_filtered[df_filtered["iddeptxt"].isin(filters["departements"])]
    if filters["communes"]:
        df_filtered = df_filtered[df_filtered["idcomtxt"].isin(filters["communes"])]
    
    nb_communes = len(df_filtered)
    pop = int(df_filtered['pop21'].sum())
    artif = df_filtered['artif_total_ha'].sum()
    
    html = f'''
<div style="background: linear-gradient(135deg, #EBF4FF 0%, #E6FFFA 100%); border: 1px solid #90CDF4; border-radius: 10px; padding: 1rem; margin-top: 0.5rem;">
<div style="color: #1E3A5F; font-weight: 700; font-size: 0.85rem; margin-bottom: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px;">ℹ️ Selection actuelle</div>
<table style="width: 100%; border-collapse: separate; border-spacing: 0 0.4rem;">
<tr>
<td style="background: white; border-radius: 6px; padding: 0.5rem 0.75rem;">
<table style="width: 100%;"><tr>
<td style="color: #718096; font-size: 0.8rem;">Communes</td>
<td style="color: #1A202C; font-weight: 700; font-size: 1rem; text-align: right;">{nb_communes}</td>
</tr></table>
</td>
</tr>
<tr>
<td style="background: white; border-radius: 6px; padding: 0.5rem 0.75rem;">
<table style="width: 100%;"><tr>
<td style="color: #718096; font-size: 0.8rem;">Habitants</td>
<td style="color: #1A202C; font-weight: 700; font-size: 1rem; text-align: right;">{pop:,}</td>
</tr></table>
</td>
</tr>
<tr>
<td style="background: white; border-radius: 6px; padding: 0.5rem 0.75rem;">
<table style="width: 100%;"><tr>
<td style="color: #718096; font-size: 0.8rem;">Artificialise</td>
<td style="color: #1A202C; font-weight: 700; font-size: 1rem; text-align: right;">{artif:,.1f} ha</td>
</tr></table>
</td>
</tr>
</table>
</div>
'''.replace(",", " ")
    
    st.markdown(html, unsafe_allow_html=True)
    
    return filters
