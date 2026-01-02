# -*- coding: utf-8 -*-
"""
Composants Graphiques du Dashboard - Version corrigee et amelioree
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from utils.metadata import get_data_source_text, get_data_source_html


COLORS = {
    "primary": "#2E86AB",
    "secondary": "#A23B72",
    "habitat": "#28A745",
    "activites": "#FFC107",
    "mixte": "#17A2B8",
    "routes": "#6C757D",
    "autres": "#DC3545",
    "reference": "#E74C3C",
    "objectif": "#27AE60",
}


def render_evolution_chart(df: pd.DataFrame):
    """
    Affiche le graphique d'evolution annuelle - VERSION CORRIGEE
    """
    
    cols_annuelles = [
        ("naf09art10", "2010"),
        ("naf10art11", "2011"),
        ("naf11art12", "2012"),
        ("naf12art13", "2013"),
        ("naf13art14", "2014"),
        ("naf14art15", "2015"),
        ("naf15art16", "2016"),
        ("naf16art17", "2017"),
        ("naf17art18", "2018"),
        ("naf18art19", "2019"),
        ("naf19art20", "2020"),
        ("naf20art21", "2021"),
        ("naf21art22", "2022"),
        ("naf22art23", "2023"),
        ("naf23art24", "2024"),
    ]
    
    data = []
    for col, annee in cols_annuelles:
        if col in df.columns:
            total = df[col].sum() / 10000
            data.append({"Annee": annee, "Consommation": total})
    
    df_evolution = pd.DataFrame(data)
    moyenne = df_evolution["Consommation"].mean()
    
    # Creation du graphique avec barres simples (pas empilees)
    fig = go.Figure()
    
    # Couleurs par periode
    colors_list = []
    for annee in df_evolution["Annee"]:
        if int(annee) <= 2021:
            colors_list.append("#2E86AB")  # Periode reference
        else:
            colors_list.append("#A23B72")  # Periode ZAN
    
    # Une seule trace de barres (pas empilees)
    fig.add_trace(
        go.Bar(
            x=df_evolution["Annee"],
            y=df_evolution["Consommation"],
            marker=dict(color=colors_list),
            text=df_evolution["Consommation"].apply(lambda x: f"{x:.1f}"),
            textposition="outside",
            textfont=dict(size=11, color="#1A202C", family="Arial"),
            hovertemplate="<b>Annee %{x}</b><br>Consommation: %{y:.2f} ha<extra></extra>",
            name="Consommation annuelle",
        )
    )
    
    # Ligne moyenne
    fig.add_hline(
        y=moyenne,
        line_dash="dash",
        line_color="#E74C3C",
        line_width=2,
        annotation_text=f"Moyenne: {moyenne:.1f} ha/an",
        annotation_position="top right",
        annotation_font=dict(size=12, color="#E74C3C"),
    )
    
    # Mise en forme
    fig.update_layout(
        title=dict(
            text="Evolution de la consommation d'espaces NAF (ha/an)",
            font=dict(size=18, color="#1E3A5F"),
            x=0.5,
        ),
        xaxis=dict(
            title="Annee",
            tickfont=dict(size=12, color="#1A202C"),
            tickangle=0,
            showgrid=False,
        ),
        yaxis=dict(
            title="Hectares",
            tickfont=dict(size=12, color="#1A202C"),
            gridcolor="#E2E8F0",
            gridwidth=1,
            range=[0, max(df_evolution["Consommation"].max() * 1.3, moyenne * 1.1)],
        ),
        template="plotly_white",
        height=500,
        showlegend=False,
        margin=dict(t=80, b=60, l=80, r=40),
        plot_bgcolor="white",
        paper_bgcolor="white",
    )
    
    # Legende personnalisee
    fig.add_annotation(
        x=0.02, y=0.98,
        xref="paper", yref="paper",
        text="<b>Bleu</b>: Periode reference (2010-2021) | <b>Rose</b>: Periode ZAN (2022-2024)",
        showarrow=False,
        font=dict(size=11, color="#718096"),
        align="left",
        bgcolor="rgba(255,255,255,0.8)",
        bordercolor="#E2E8F0",
        borderwidth=1,
    )
    
    # Ajout de la mention de source
    fig.add_annotation(
        x=0.98, y=0.02,
        xref="paper", yref="paper",
        text=get_data_source_text(),
        showarrow=False,
        font=dict(size=9, color="#718096"),
        align="right",
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor="#E2E8F0",
        borderwidth=1,
        borderpad=4,
    )
    
    # Ajout de la mention de source
    fig.add_annotation(
        x=0.98, y=0.02,
        xref="paper", yref="paper",
        text=get_data_source_text(),
        showarrow=False,
        font=dict(size=9, color="#718096"),
        align="right",
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor="#E2E8F0",
        borderwidth=1,
        borderpad=4,
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_repartition_chart(metrics: dict):
    """
    Affiche le graphique de repartition par destination
    """
    
    categories = []
    valeurs = []
    couleurs = []
    
    data_rep = [
        ("Habitat", metrics.get("artif_habitat_ha", 0), "#28A745"),
        ("Activites", metrics.get("artif_activites_ha", 0), "#FFC107"),
        ("Mixte", metrics.get("artif_mixte_ha", 0), "#17A2B8"),
        ("Routes", metrics.get("artif_routes_ha", 0), "#6C757D"),
        ("Autres", metrics.get("artif_autres_ha", 0), "#DC3545"),
    ]
    
    for cat, val, col in data_rep:
        if val > 0.1:
            categories.append(cat)
            valeurs.append(val)
            couleurs.append(col)
    
    total = sum(valeurs)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        fig = go.Figure(data=[go.Pie(
            labels=categories,
            values=valeurs,
            hole=0.5,
            marker=dict(colors=couleurs),
            textinfo="percent",
            textposition="outside",
            textfont=dict(size=13, color="#1A202C", family="Arial"),
            hovertemplate="<b>%{label}</b><br>%{value:.1f} ha (%{percent})<extra></extra>",
            pull=[0.02] * len(categories),
        )])
        
        fig.update_layout(
            title=dict(
                text="Repartition par destination",
                font=dict(size=16, color="#1E3A5F"),
                x=0.5,
            ),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.15,
                xanchor="center",
                x=0.5,
                font=dict(size=11),
            ),
            height=400,
            margin=dict(t=60, b=60, l=20, r=20),
            annotations=[dict(
                text=f"<b>{total:.0f}</b><br>ha total",
                x=0.5, y=0.5,
                font=dict(size=16, color="#1E3A5F"),
                showarrow=False,
            )],
        )
        
        # Ajout de la mention de source
    fig.add_annotation(
        x=0.98, y=0.02,
        xref="paper", yref="paper",
        text=get_data_source_text(),
        showarrow=False,
        font=dict(size=9, color="#718096"),
        align="right",
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor="#E2E8F0",
        borderwidth=1,
        borderpad=4,
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("""
<div style="background: white; border: 1px solid #E2E8F0; border-radius: 10px; padding: 1rem; margin-top: 2rem;">
<div style="color: #1E3A5F; font-weight: 700; font-size: 0.95rem; margin-bottom: 1rem;">Detail par destination</div>
""", unsafe_allow_html=True)
        
        for cat, val, col in data_rep:
            if val > 0.1:
                pct = (val / total * 100) if total > 0 else 0
                st.markdown(f"""
<div style="display: flex; align-items: center; padding: 0.5rem 0; border-bottom: 1px solid #E2E8F0;">
<div style="width: 12px; height: 12px; background: {col}; border-radius: 3px; margin-right: 0.75rem;"></div>
<div style="flex: 1; color: #4A5568; font-size: 0.9rem;">{cat}</div>
<div style="color: #1A202C; font-weight: 600; font-size: 0.9rem;">{val:.1f} ha</div>
<div style="color: #718096; font-size: 0.85rem; margin-left: 0.5rem; width: 50px; text-align: right;">({pct:.1f}%)</div>
</div>
""", unsafe_allow_html=True)
        
        st.markdown(f"""
<div style="display: flex; align-items: center; padding: 0.75rem 0; margin-top: 0.5rem; background: #F7FAFC; border-radius: 6px; padding-left: 0.75rem;">
<div style="flex: 1; color: #1E3A5F; font-weight: 700; font-size: 0.95rem;">TOTAL</div>
<div style="color: #1E3A5F; font-weight: 800; font-size: 1.1rem;">{total:.1f} ha</div>
<div style="width: 60px;"></div>
</div>
</div>
""", unsafe_allow_html=True)


def render_top_communes_chart(df: pd.DataFrame, n_top: int = 10):
    """
    Affiche le top communes avec carte interactive - VERSION AMELIOREE
    """
    
    df_top = df.nlargest(n_top, "artif_total_ha")[
        ["idcom", "idcomtxt", "artif_total_ha", "pop21", "iddeptxt"]
    ].copy()
    df_top = df_top.reset_index(drop=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Graphique barres horizontales - AMELIORE
        df_plot = df_top.sort_values("artif_total_ha", ascending=True)
        
        fig = go.Figure()
        
        # Gradient de couleurs pour meilleure lisibilite
        n = len(df_plot)
        colors = [f"rgba(46, 134, 171, {0.5 + 0.5 * i / n})" for i in range(n)]
        
        fig.add_trace(
            go.Bar(
                y=df_plot["idcomtxt"],
                x=df_plot["artif_total_ha"],
                orientation="h",
                marker=dict(
                    color=colors,
                    line=dict(color="#1E3A5F", width=1.5),
                ),
                text=df_plot["artif_total_ha"].apply(lambda x: f"{x:.1f} ha"),
                textposition="outside",
                textfont=dict(size=12, color="#1A202C"),
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Artificialisation: %{x:.2f} ha<br>"
                    "<extra></extra>"
                ),
            )
        )
        
        fig.update_layout(
            title=dict(
                text=f"Top {n_top} communes les plus artificialisees",
                font=dict(size=18, color="#1E3A5F"),
                x=0.5,
            ),
            xaxis=dict(
                title="Hectares artificialises (2009-2024)",
                tickfont=dict(size=12, color="#1A202C"),
                gridcolor="#E2E8F0",
                gridwidth=1,
                showgrid=True,
            ),
            yaxis=dict(
                title="",
                tickfont=dict(size=12, color="#1A202C"),
                showgrid=False,
            ),
            template="plotly_white",
            height=500,
            showlegend=False,
            margin=dict(t=80, b=40, l=180, r=100),
            plot_bgcolor="white",
            paper_bgcolor="white",
        )
        
        # Ajout de la mention de source
    fig.add_annotation(
        x=0.98, y=0.02,
        xref="paper", yref="paper",
        text=get_data_source_text(),
        showarrow=False,
        font=dict(size=9, color="#718096"),
        align="right",
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor="#E2E8F0",
        borderwidth=1,
        borderpad=4,
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Mention de source
    st.markdown(f'<div style="text-align: center; margin-top: -10px; font-size: 0.75rem; color: #718096;">{get_data_source_html()}</div>', unsafe_allow_html=True)
    
    with col2:
        # Carte interactive
        st.markdown("""
<div style="background: white; border: 1px solid #E2E8F0; border-radius: 10px; padding: 1rem;">
<div style="color: #1E3A5F; font-weight: 700; font-size: 0.95rem; margin-bottom: 1rem;">🗺️ Localisation des communes</div>
""", unsafe_allow_html=True)
        
        try:
            render_communes_map(df_top)
        except Exception as e:
            # Fallback: tableau detaille
            st.markdown(f"""
<div style="color: #718096; font-size: 0.85rem; margin-bottom: 1rem; font-style: italic;">
Carte non disponible ({str(e)[:50]}) - Affichage en tableau
</div>
""", unsafe_allow_html=True)
            
            for i, row in df_top.iterrows():
                rang = i + 1
                pop_str = f"{int(row['pop21']):,}".replace(",", " ")
                st.markdown(f"""
<div style="display: flex; align-items: center; padding: 0.6rem; background: {'#F7FAFC' if rang % 2 == 0 else 'white'}; border-radius: 6px; margin-bottom: 0.25rem;">
<div style="width: 32px; height: 32px; background: linear-gradient(135deg, #2E86AB 0%, #1E3A5F 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: 700; font-size: 0.9rem; margin-right: 0.75rem;">{rang}</div>
<div style="flex: 1;">
<div style="color: #1A202C; font-weight: 600; font-size: 0.95rem;">{row['idcomtxt']}</div>
<div style="color: #718096; font-size: 0.8rem;">{row['iddeptxt']} - Pop: {pop_str}</div>
</div>
<div style="color: #2E86AB; font-weight: 700; font-size: 1rem;">{row['artif_total_ha']:.1f} ha</div>
</div>
""", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)


def render_communes_map(df_top: pd.DataFrame):
    """
    Affiche une carte des communes - VERSION CORRIGEE avec Folium
    """
    try:
        import folium
        import requests
    except ImportError:
        raise Exception("Folium non installe - pip install folium")
    
    # Recuperer les coordonnees via API
    coords_data = []
    for _, row in df_top.iterrows():
        code_insee = str(row["idcom"]).zfill(5)
        try:
            resp = requests.get(
                f"https://geo.api.gouv.fr/communes/{code_insee}?fields=centre",
                timeout=3
            )
            if resp.status_code == 200:
                data = resp.json()
                if "centre" in data and data["centre"]:
                    coords = data["centre"]["coordinates"]
                    coords_data.append({
                        "code": code_insee,
                        "lon": coords[0],
                        "lat": coords[1],
                        "nom": row["idcomtxt"],
                        "artif": row["artif_total_ha"],
                    })
        except:
            continue
    
    if len(coords_data) < 2:
        raise Exception("Impossible de recuperer les coordonnees geographiques")
    
    # Calculer le centre de la carte
    lats = [c["lat"] for c in coords_data]
    lons = [c["lon"] for c in coords_data]
    center_lat = sum(lats) / len(lats)
    center_lon = sum(lons) / len(lons)
    
    # Creer la carte Folium
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=9,
        tiles="CartoDB positron",
    )
    
    # Ajouter les marqueurs
    max_artif = max(c["artif"] for c in coords_data)
    
    for coord in coords_data:
        # Taille du marqueur proportionnelle
        radius = max(8, min(25, coord["artif"] / max_artif * 20))
        
        folium.CircleMarker(
            location=[coord["lat"], coord["lon"]],
            radius=radius,
            popup=f"<b>{coord['nom']}</b><br>{coord['artif']:.1f} ha",
            tooltip=f"{coord['nom']}: {coord['artif']:.1f} ha",
            color="#1E3A5F",
            fillColor="#2E86AB",
            fillOpacity=0.7,
            weight=2,
        ).add_to(m)
        
        # Label avec nom
        folium.Marker(
            location=[coord["lat"], coord["lon"]],
            icon=folium.DivIcon(
                html=f'<div style="font-size: 10px; font-weight: bold; color: #1E3A5F; text-align: center; background: rgba(255,255,255,0.8); padding: 2px 4px; border-radius: 3px;">{coord["nom"][:15]}</div>',
                icon_size=(100, 20),
                icon_anchor=(50, 10),
            ),
        ).add_to(m)
    
    # Afficher la carte avec st.components.v1.html
    import streamlit.components.v1 as components
    html_str = m._repr_html_()
    components.html(html_str, height=400, scrolling=False)


def render_trajectory_chart(df: pd.DataFrame, metrics: dict):
    """
    Affiche le graphique de trajectoire ZAN
    """
    
    annees = list(range(2021, 2032))
    
    conso_reelle = [0]
    cumul = 0
    
    cols_recentes = [
        ("naf21art22", 2022),
        ("naf22art23", 2023),
        ("naf23art24", 2024),
    ]
    
    for col, annee in cols_recentes:
        if col in df.columns:
            cumul += df[col].sum() / 10000
            conso_reelle.append(cumul)
    
    enveloppe = metrics["enveloppe_zan"]
    trajectoire_lineaire = [enveloppe * i / 10 for i in range(11)]
    
    fig = go.Figure()
    
    fig.add_trace(
        go.Scatter(
            x=annees,
            y=trajectoire_lineaire,
            fill="tozeroy",
            fillcolor="rgba(39, 174, 96, 0.15)",
            line=dict(color="#27AE60", dash="dash", width=2),
            name="Enveloppe theorique (-50%)",
            hovertemplate="<b>%{x}</b><br>Enveloppe: %{y:.1f} ha<extra></extra>",
        )
    )
    
    x_reel = annees[:len(conso_reelle)]
    fig.add_trace(
        go.Scatter(
            x=x_reel,
            y=conso_reelle,
            mode="lines+markers",
            line=dict(color="#2E86AB", width=4),
            marker=dict(size=12, color="#2E86AB", line=dict(color="white", width=2)),
            name="Consommation reelle",
            hovertemplate="<b>%{x}</b><br>Cumule: %{y:.1f} ha<extra></extra>",
        )
    )
    
    fig.add_hline(
        y=enveloppe,
        line_dash="dot",
        line_color="#E74C3C",
        line_width=2,
        annotation_text=f"Limite 2031: {enveloppe:.0f} ha",
        annotation_position="top right",
        annotation_font=dict(size=12, color="#E74C3C"),
    )
    
    fig.update_layout(
        title=dict(
            text="Trajectoire de consommation vs Objectif ZAN",
            font=dict(size=16, color="#1E3A5F"),
            x=0.5,
        ),
        xaxis=dict(
            title="",
            tickmode="linear",
            dtick=1,
            tickfont=dict(size=11, color="#1A202C"),
            gridcolor="#E2E8F0",
        ),
        yaxis=dict(
            title="Consommation cumulee (ha)",
            tickfont=dict(size=11, color="#1A202C"),
            gridcolor="#E2E8F0",
        ),
        template="plotly_white",
        height=400,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(size=11),
        ),
        margin=dict(t=60, b=80, l=60, r=40),
    )
    
    # Ajout de la mention de source
    fig.add_annotation(
        x=0.98, y=0.02,
        xref="paper", yref="paper",
        text=get_data_source_text(),
        showarrow=False,
        font=dict(size=9, color="#718096"),
        align="right",
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor="#E2E8F0",
        borderwidth=1,
        borderpad=4,
    )
    
    st.plotly_chart(fig, use_container_width=True)
