# -*- coding: utf-8 -*-
"""
Composant Filtres du Dashboard - Version Business Professional
"""

import streamlit as st
import pandas as pd


def render_filters(df_scot: pd.DataFrame, df_cc: pd.DataFrame) -> dict:
    """
    Affiche les filtres dans la sidebar avec un design professionnel
    """
    
    filters = {}
    
    # Header sidebar
    st.markdown('''
<div style="background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); border-bottom: 2px solid #2E86AB; border-radius: 8px 8px 0 0; padding: 1.25rem 1rem; margin-bottom: 1.5rem;">
<div style="color: #FFFFFF; font-size: 1.1rem; font-weight: 700; letter-spacing: -0.3px; margin-bottom: 0.25rem;">DASHBOARD ZAN</div>
<div style="color: #94A3B8; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px;">Pilotage Artificialisation</div>
</div>
''', unsafe_allow_html=True)
    
    # Périmètre
    st.markdown('''
<div style="background: #1E293B; border-left: 3px solid #2E86AB; border-radius: 0 6px 6px 0; padding: 0.75rem 1rem; margin-bottom: 1rem;">
<span style="color: #FFFFFF; font-weight: 600; font-size: 0.85rem; letter-spacing: 0.3px;">PÉRIMÈTRE D'ÉTUDE</span>
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
<div style="background: #1E293B; border-left: 3px solid #2E86AB; border-radius: 0 6px 6px 0; padding: 0.6rem 0.9rem; margin-bottom: 0.5rem;">
<span style="color: #FFFFFF; font-weight: 600; font-size: 0.8rem; letter-spacing: 0.3px;">DÉPARTEMENT</span>
</div>
''', unsafe_allow_html=True)
    
    departements = sorted(df["iddeptxt"].unique().tolist())
    filters["departements"] = st.multiselect(
        "Departements",
        options=departements,
        default=[],
        placeholder="Tous les départements",
        label_visibility="collapsed",
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Communes
    st.markdown('''
<div style="background: #1E293B; border-left: 3px solid #A23B72; border-radius: 0 6px 6px 0; padding: 0.6rem 0.9rem; margin-bottom: 0.5rem;">
<span style="color: #FFFFFF; font-weight: 600; font-size: 0.8rem; letter-spacing: 0.3px;">COMMUNES</span>
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
<div style="background: #1E293B; border-left: 3px solid #48BB78; border-radius: 0 6px 6px 0; padding: 0.6rem 0.9rem; margin-bottom: 0.5rem;">
<span style="color: #FFFFFF; font-weight: 600; font-size: 0.8rem; letter-spacing: 0.3px;">TYPOLOGIE URBAINE</span>
</div>
''', unsafe_allow_html=True)
    
    typo_labels = {
        "11": "Pôle principal",
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
<div style="background: #1E293B; border: 1px solid #334155; border-radius: 8px; padding: 1.25rem; margin-top: 1rem;">
<div style="color: #FFFFFF; font-weight: 700; font-size: 0.85rem; margin-bottom: 1rem; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 1px solid #334155; padding-bottom: 0.75rem;">SÉLECTION ACTUELLE</div>
<table style="width: 100%; border-collapse: separate; border-spacing: 0 0.5rem;">
<tr>
<td style="background: #0F172A; border: 1px solid #334155; border-radius: 6px; padding: 0.75rem 1rem;">
<table style="width: 100%;"><tr>
<td style="color: #94A3B8; font-size: 0.8rem; font-weight: 500;">Communes</td>
<td style="color: #FFFFFF; font-weight: 700; font-size: 1rem; text-align: right; font-family: 'Segoe UI', Arial, sans-serif;">{nb_communes}</td>
</tr></table>
</td>
</tr>
<tr>
<td style="background: #0F172A; border: 1px solid #334155; border-radius: 6px; padding: 0.75rem 1rem;">
<table style="width: 100%;"><tr>
<td style="color: #94A3B8; font-size: 0.8rem; font-weight: 500;">Habitants</td>
<td style="color: #FFFFFF; font-weight: 700; font-size: 1rem; text-align: right; font-family: 'Segoe UI', Arial, sans-serif;">{pop:,}</td>
</tr></table>
</td>
</tr>
<tr>
<td style="background: #0F172A; border: 1px solid #334155; border-radius: 6px; padding: 0.75rem 1rem;">
<table style="width: 100%;"><tr>
<td style="color: #94A3B8; font-size: 0.8rem; font-weight: 500;">Artificialisé</td>
<td style="color: #FFFFFF; font-weight: 700; font-size: 1rem; text-align: right; font-family: 'Segoe UI', Arial, sans-serif;">{artif:,.1f} ha</td>
</tr></table>
</td>
</tr>
</table>
</div>
'''.replace(",", " ")
    
    st.markdown(html, unsafe_allow_html=True)
    
    return filters
