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
            text=df_evolution["Consommation"].apply(lambda x: f"<b>{x:.1f}</b>"),
            textposition="outside",
            textfont=dict(size=12, color="#FFFFFF", family="Segoe UI"),
            hovertemplate="<b>Annee %{x}</b><br>Consommation: %{y:.2f} ha<extra></extra>",
            name="Consommation annuelle",
            cliponaxis=False,
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
            text="ÉVOLUTION DE LA CONSOMMATION D'ESPACES NAF",
            font=dict(size=16, color="#FFFFFF", family="Segoe UI"),
            x=0.5,
        ),
        xaxis=dict(
            title="Année",
            tickfont=dict(size=12, color="#CBD5E0"),
            tickangle=0,
            showgrid=False,
        ),
        yaxis=dict(
            title="Hectares",
            tickfont=dict(size=12, color="#CBD5E0"),
            gridcolor="#334155",
            gridwidth=1,
            range=[0, df_evolution["Consommation"].max() * 1.35],
        ),
        template="plotly_dark",
        height=500,
        showlegend=False,
        margin=dict(t=100, b=60, l=80, r=40),
        plot_bgcolor="#0F172A",
        paper_bgcolor="#1E293B",
    )
    
    # Legende personnalisee
    fig.add_annotation(
        x=0.02, y=0.98,
        xref="paper", yref="paper",
        text="<b>Bleu</b>: Période référence (2010-2021) | <b>Rose</b>: Période ZAN (2022-2024)",
        showarrow=False,
        font=dict(size=11, color="#CBD5E0"),
        align="left",
        bgcolor="rgba(15, 23, 42, 0.9)",
        bordercolor="#334155",
        borderwidth=1,
    )
    
    # Ajout de la mention de source
    fig.add_annotation(
        x=0.98, y=0.02,
        xref="paper", yref="paper",
        text=get_data_source_text(),
        showarrow=False,
        font=dict(size=9, color="#64748B"),
        align="right",
        bgcolor="rgba(15, 23, 42, 0.9)",
        bordercolor="#334155",
        borderwidth=1,
        borderpad=4,
    )
    
    st.plotly_chart(fig, use_container_width=True)


# ============================================
# NOUVELLES INFOGRAPHIES BUSINESS
# ============================================

def render_efficience_chart(df: pd.DataFrame):
    """
    Infographie 1: Efficience de l'Urbanisation
    Scatter plot: croissance démographique vs artificialisation
    """
    
    df_plot = df.copy()
    
    # Filtrer les communes avec des données valides
    df_plot = df_plot[
        (df_plot["pop1521"].notna()) & 
        (df_plot["artif_total_ha"] > 0)
    ].copy()
    
    # Calculer l'efficience (m² par habitant ajouté)
    df_plot["efficience"] = np.where(
        df_plot["pop1521"] > 0,
        (df_plot["naf09art24"] / df_plot["pop1521"]),
        np.nan
    )
    
    # Typologie pour la couleur
    typo_labels = {
        "11": "Pôle principal",
        "12": "Couronne grande aire",
        "20": "Petite/moyenne aire",
        "30": "Hors attraction",
    }
    df_plot["typo_label"] = df_plot["aav2020_typo"].astype(str).map(typo_labels).fillna("Autre")
    
    # Couleurs par typologie
    color_map = {
        "Pôle principal": "#2E86AB",
        "Couronne grande aire": "#A23B72",
        "Petite/moyenne aire": "#48BB78",
        "Hors attraction": "#ED8936",
        "Autre": "#64748B",
    }
    
    fig = go.Figure()
    
    for typo in color_map.keys():
        df_typo = df_plot[df_plot["typo_label"] == typo]
        if len(df_typo) > 0:
            fig.add_trace(
                go.Scatter(
                    x=df_typo["pop1521"],
                    y=df_typo["artif_total_ha"],
                    mode="markers",
                    name=typo,
                    marker=dict(
                        size=np.sqrt(df_typo["pop21"]) / 5 + 8,
                        color=color_map[typo],
                        opacity=0.7,
                        line=dict(color="#FFFFFF", width=1),
                    ),
                    text=df_typo["idcomtxt"],
                    hovertemplate=(
                        "<b>%{text}</b><br>"
                        "Évolution pop.: %{x:+,}<br>"
                        "Artificialisation: %{y:.1f} ha<br>"
                        "<extra></extra>"
                    ),
                )
            )
    
    # Lignes de référence (seuils m²/hab)
    max_pop = max(df_plot["pop1521"].max(), 100)
    min_pop = min(df_plot["pop1521"].min(), 0)
    
    # Seuil 200 m²/hab (efficient)
    fig.add_trace(
        go.Scatter(
            x=[0, max_pop],
            y=[0, max_pop * 200 / 10000],
            mode="lines",
            line=dict(color="#48BB78", dash="dash", width=1.5),
            name="200 m²/hab (efficient)",
            showlegend=True,
        )
    )
    
    # Seuil 500 m²/hab (standard)
    fig.add_trace(
        go.Scatter(
            x=[0, max_pop],
            y=[0, max_pop * 500 / 10000],
            mode="lines",
            line=dict(color="#ED8936", dash="dash", width=1.5),
            name="500 m²/hab (standard)",
            showlegend=True,
        )
    )
    
    fig.update_layout(
        title=dict(
            text="EFFICIENCE DE L'URBANISATION",
            font=dict(size=18, color="#FFFFFF", family="Segoe UI"),
            x=0.5,
        ),
        xaxis=dict(
            title="Évolution de la population (2015-2021)",
            tickfont=dict(size=11, color="#94A3B8"),
            gridcolor="#334155",
            zerolinecolor="#475569",
            zerolinewidth=2,
        ),
        yaxis=dict(
            title="Artificialisation (ha)",
            tickfont=dict(size=11, color="#94A3B8"),
            gridcolor="#334155",
        ),
        template="plotly_dark",
        height=500,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5,
            font=dict(size=10, color="#CBD5E0"),
        ),
        margin=dict(t=80, b=100, l=80, r=40),
        paper_bgcolor="#1E293B",
        plot_bgcolor="#0F172A",
    )
    
    # Annotation explicative
    fig.add_annotation(
        x=0.02, y=0.98,
        xref="paper", yref="paper",
        text="Taille des bulles = Population 2021 | Sous la ligne verte = urbanisation efficiente",
        showarrow=False,
        font=dict(size=10, color="#94A3B8"),
        align="left",
        bgcolor="rgba(15, 23, 42, 0.8)",
        bordercolor="#334155",
        borderwidth=1,
    )
    
    # Source
    fig.add_annotation(
        x=0.98, y=0.02,
        xref="paper", yref="paper",
        text=get_data_source_text(),
        showarrow=False,
        font=dict(size=9, color="#64748B"),
        align="right",
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_typologie_chart(df: pd.DataFrame):
    """
    Infographie 2: Analyse par Typologie Territoriale
    Barres groupées + donut par typologie AAV - VERSION OPTIMISÉE
    """
    
    # Labels courts pour l'axe X
    typo_labels = {
        "11": "Pôles",
        "12": "Couronnes",
        "20": "P/M aires",
        "30": "Rural",
    }
    
    # Labels complets pour légende et tooltip
    typo_labels_full = {
        "Pôles": "Pôles principaux",
        "Couronnes": "Couronnes grandes aires",
        "P/M aires": "Petites/moyennes aires",
        "Rural": "Hors attraction (rural)",
    }
    
    typo_colors = {
        "Pôles": "#2E86AB",
        "Couronnes": "#A23B72",
        "P/M aires": "#48BB78",
        "Rural": "#ED8936",
    }
    
    # Agrégation par typologie
    df_copy = df.copy()
    df_copy["typo_label"] = df_copy["aav2020_typo"].astype(str).map(typo_labels).fillna("Autre")
    
    agg_data = df_copy.groupby("typo_label").agg({
        "naf09art24": "sum",
        "art09hab24": "sum",
        "art09act24": "sum",
        "art09mix24": "sum",
        "art09rou24": "sum",
        "pop1521": "sum",
        "pop21": "sum",
    }).reset_index()
    
    # Conversion en hectares
    for col in ["naf09art24", "art09hab24", "art09act24", "art09mix24", "art09rou24"]:
        agg_data[col] = agg_data[col] / 10000
    
    # Calcul efficience
    agg_data["efficience"] = np.where(
        agg_data["pop1521"] > 0,
        agg_data["naf09art24"] * 10000 / agg_data["pop1521"],
        0
    )
    
    # Ajouter labels complets pour affichage
    agg_data["typo_full"] = agg_data["typo_label"].map(typo_labels_full).fillna(agg_data["typo_label"])
    
    # ===== GRAPHIQUE BARRES GROUPÉES =====
    st.markdown("""
<div style="background: #1E293B; border: 1px solid #334155; border-radius: 8px; padding: 1rem; margin-bottom: 1rem;">
<div style="color: #FFFFFF; font-weight: 700; font-size: 1rem; text-transform: uppercase; letter-spacing: 0.5px;">ARTIFICIALISATION PAR TYPOLOGIE</div>
<div style="color: #94A3B8; font-size: 0.8rem; margin-top: 0.25rem;">Répartition par destination et type de territoire</div>
</div>
""", unsafe_allow_html=True)
    
    # ===== HISTOGRAMME GROUPÉ =====
    st.markdown("""
<div style="background: #1E293B; border: 1px solid #334155; border-radius: 8px; padding: 0.75rem; margin-bottom: 1rem;">
<div style="color: #94A3B8; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.5px;">Consommation par destination et type de territoire</div>
</div>
""", unsafe_allow_html=True)
    
    # Barres groupées par destination
    destinations = ["Habitat", "Activités", "Mixte", "Routes"]
    dest_cols = ["art09hab24", "art09act24", "art09mix24", "art09rou24"]
    dest_colors = ["#48BB78", "#ED8936", "#2E86AB", "#64748B"]
    
    fig = go.Figure()
    
    for dest, col_name, color in zip(destinations, dest_cols, dest_colors):
        fig.add_trace(
            go.Bar(
                name=dest,
                x=agg_data["typo_label"],
                y=agg_data[col_name],
                marker_color=color,
                text=agg_data[col_name].apply(lambda x: f"{x:.0f}" if x >= 1 else ""),
                textposition="outside",
                textfont=dict(size=10, color="#FFFFFF"),
                hovertemplate="<b>%{x}</b><br>" + dest + ": %{y:.1f} ha<extra></extra>",
            )
        )
    
    # Calculer le max pour ajuster l'axe Y
    max_val = max(agg_data[col].max() for col in dest_cols)
    
    fig.update_layout(
        xaxis=dict(
            title="",
            tickfont=dict(size=12, color="#FFFFFF"),
            tickangle=0,
        ),
        yaxis=dict(
            title="Hectares",
            tickfont=dict(size=11, color="#94A3B8"),
            gridcolor="#334155",
            range=[0, max_val * 1.2],  # Espace pour les labels
        ),
        barmode="group",
        template="plotly_dark",
        height=380,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=1.12,
            xanchor="center",
            x=0.5,
            font=dict(size=11, color="#CBD5E0"),
            bgcolor="rgba(0,0,0,0)",
        ),
        margin=dict(t=60, b=40, l=60, r=20),
        paper_bgcolor="#1E293B",
        plot_bgcolor="#0F172A",
        bargap=0.2,
        bargroupgap=0.1,
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # ===== DIAGRAMME CIRCULAIRE - PLEINE LARGEUR =====
    st.markdown("""
<div style="background: #1E293B; border: 1px solid #334155; border-radius: 8px; padding: 0.75rem; margin-top: 1rem; margin-bottom: 1rem;">
<div style="color: #94A3B8; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.5px;">Répartition globale par typologie territoriale</div>
</div>
""", unsafe_allow_html=True)
    
    # Donut répartition globale avec légende - pleine largeur
    labels = agg_data["typo_full"].tolist()
    labels_short = agg_data["typo_label"].tolist()
    values = agg_data["naf09art24"].tolist()
    colors = [typo_colors.get(l, "#64748B") for l in labels_short]
    
    fig2 = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.45,
        marker=dict(colors=colors, line=dict(color="#1E293B", width=2)),
        textinfo="percent+label",
        textposition="outside",
        textfont=dict(size=12, color="#FFFFFF"),
        hovertemplate="<b>%{label}</b><br>%{value:.1f} ha (%{percent})<extra></extra>",
        pull=[0.02] * len(labels),
    )])
    
    total = sum(values)
    fig2.update_layout(
        showlegend=False,  # Légende désactivée car labels affichés sur le graphique
        height=400,
        margin=dict(t=60, b=60, l=100, r=100),
        paper_bgcolor="#1E293B",
        annotations=[dict(
            text=f"<b>{total:.0f}</b><br><span style='font-size:14px'>ha total</span>",
            x=0.5, y=0.5,
            font=dict(size=24, color="#FFFFFF"),
            showarrow=False,
        )],
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # ===== TABLEAU RÉCAPITULATIF =====
    st.markdown("""
<div style="background: #1E293B; border: 1px solid #334155; border-radius: 8px; padding: 1.25rem; margin-top: 1rem;">
<div style="color: #FFFFFF; font-weight: 700; font-size: 0.9rem; margin-bottom: 1rem; text-transform: uppercase; letter-spacing: 0.5px;">SYNTHÈSE PAR TYPOLOGIE</div>
""", unsafe_allow_html=True)
    
    for _, row in agg_data.iterrows():
        typo = row["typo_label"]
        typo_full = row["typo_full"]
        artif = row["naf09art24"]
        eff = row["efficience"]
        
        # Couleur selon efficience
        if eff < 200:
            eff_color = "#48BB78"
        elif eff < 500:
            eff_color = "#ED8936"
        else:
            eff_color = "#F56565"
        
        st.markdown(f"""
<div style="display: flex; align-items: center; padding: 0.75rem; background: #0F172A; border-radius: 6px; margin-bottom: 0.5rem; border-left: 4px solid {typo_colors.get(typo, '#64748B')};">
<div style="flex: 1; color: #FFFFFF; font-weight: 600;">{typo_full}</div>
<div style="color: #94A3B8; font-size: 0.85rem; margin-right: 1rem;">{artif:.0f} ha</div>
<div style="background: {eff_color}; color: #0F172A; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.75rem; font-weight: 700;">{eff:.0f} m²/hab</div>
</div>
""", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)


def render_jauge_zan_communes(df: pd.DataFrame):
    """
    Infographie 3: Jauge ZAN par Commune
    Heatmap du taux de consommation de l'enveloppe individuelle
    """
    
    df_calc = df.copy()
    
    # Calcul de l'enveloppe individuelle par commune
    cols_ref = ["naf11art12", "naf12art13", "naf13art14", "naf14art15", "naf15art16",
                "naf16art17", "naf17art18", "naf18art19", "naf19art20", "naf20art21"]
    
    cols_recent = ["naf21art22", "naf22art23", "naf23art24"]
    
    df_calc["conso_ref"] = 0
    for col in cols_ref:
        if col in df_calc.columns:
            df_calc["conso_ref"] += df_calc[col] / 10000
    
    df_calc["enveloppe_commune"] = df_calc["conso_ref"] * 0.5
    
    df_calc["conso_2124"] = 0
    for col in cols_recent:
        if col in df_calc.columns:
            df_calc["conso_2124"] += df_calc[col] / 10000
    
    # Taux de consommation
    df_calc["taux_conso"] = np.where(
        df_calc["enveloppe_commune"] > 0,
        (df_calc["conso_2124"] / df_calc["enveloppe_commune"]) * 100,
        0
    )
    
    # Classification
    def get_statut(taux):
        if taux < 30:
            return "Conforme", "#48BB78"
        elif taux < 50:
            return "Vigilance", "#ED8936"
        else:
            return "Alerte", "#F56565"
    
    df_calc["statut"], df_calc["couleur"] = zip(*df_calc["taux_conso"].apply(get_statut))
    
    # Top 15 communes à risque
    df_risque = df_calc.nlargest(15, "taux_conso")[
        ["idcomtxt", "enveloppe_commune", "conso_2124", "taux_conso", "statut", "couleur"]
    ].reset_index(drop=True)
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        # Graphique barres horizontales
        df_plot = df_risque.sort_values("taux_conso", ascending=True)
        
        fig = go.Figure()
        
        fig.add_trace(
            go.Bar(
                y=df_plot["idcomtxt"],
                x=df_plot["taux_conso"],
                orientation="h",
                marker=dict(
                    color=df_plot["couleur"].tolist(),
                    line=dict(color="#1E293B", width=1),
                ),
                text=df_plot["taux_conso"].apply(lambda x: f"{x:.0f}%"),
                textposition="outside",
                textfont=dict(size=11, color="#FFFFFF"),
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Taux: %{x:.1f}%<br>"
                    "<extra></extra>"
                ),
            )
        )
        
        # Lignes de seuils
        fig.add_vline(x=30, line_dash="dash", line_color="#48BB78", line_width=2)
        fig.add_vline(x=50, line_dash="dash", line_color="#ED8936", line_width=2)
        fig.add_vline(x=100, line_dash="solid", line_color="#F56565", line_width=2)
        
        fig.update_layout(
            title=dict(
                text="COMMUNES À RISQUE DE DÉPASSEMENT ZAN",
                font=dict(size=16, color="#FFFFFF", family="Segoe UI"),
                x=0.5,
            ),
            xaxis=dict(
                title="% de l'enveloppe ZAN consommée",
                tickfont=dict(size=11, color="#94A3B8"),
                gridcolor="#334155",
                range=[0, max(df_risque["taux_conso"].max() * 1.2, 110)],
            ),
            yaxis=dict(
                title="",
                tickfont=dict(size=10, color="#FFFFFF"),
            ),
            template="plotly_dark",
            height=500,
            showlegend=False,
            margin=dict(t=60, b=60, l=160, r=60),
            paper_bgcolor="#1E293B",
            plot_bgcolor="#0F172A",
        )
        
        # Légende des seuils
        fig.add_annotation(
            x=0.98, y=0.98,
            xref="paper", yref="paper",
            text="<30% Conforme | 30-50% Vigilance | >50% Alerte",
            showarrow=False,
            font=dict(size=9, color="#94A3B8"),
            align="right",
            bgcolor="rgba(15, 23, 42, 0.8)",
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Résumé statistique
        nb_conforme = len(df_calc[df_calc["statut"] == "Conforme"])
        nb_vigilance = len(df_calc[df_calc["statut"] == "Vigilance"])
        nb_alerte = len(df_calc[df_calc["statut"] == "Alerte"])
        total = len(df_calc)
        
        st.markdown(f"""
<div style="background: #1E293B; border: 1px solid #334155; border-radius: 8px; padding: 1.5rem;">
<div style="color: #FFFFFF; font-weight: 700; font-size: 1rem; margin-bottom: 1.5rem; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 1px solid #334155; padding-bottom: 0.75rem;">SYNTHÈSE DU TERRITOIRE</div>

<div style="display: flex; align-items: center; padding: 1rem; background: rgba(72, 187, 120, 0.15); border-left: 4px solid #48BB78; border-radius: 0 6px 6px 0; margin-bottom: 0.75rem;">
<div style="flex: 1;">
<div style="color: #48BB78; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.25rem;">Conforme</div>
<div style="color: #FFFFFF; font-size: 1.5rem; font-weight: 700;">{nb_conforme}</div>
</div>
<div style="color: #94A3B8; font-size: 0.9rem;">{nb_conforme/total*100:.0f}%</div>
</div>

<div style="display: flex; align-items: center; padding: 1rem; background: rgba(237, 137, 54, 0.15); border-left: 4px solid #ED8936; border-radius: 0 6px 6px 0; margin-bottom: 0.75rem;">
<div style="flex: 1;">
<div style="color: #ED8936; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.25rem;">Vigilance</div>
<div style="color: #FFFFFF; font-size: 1.5rem; font-weight: 700;">{nb_vigilance}</div>
</div>
<div style="color: #94A3B8; font-size: 0.9rem;">{nb_vigilance/total*100:.0f}%</div>
</div>

<div style="display: flex; align-items: center; padding: 1rem; background: rgba(245, 101, 101, 0.15); border-left: 4px solid #F56565; border-radius: 0 6px 6px 0;">
<div style="flex: 1;">
<div style="color: #F56565; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.25rem;">Alerte</div>
<div style="color: #FFFFFF; font-size: 1.5rem; font-weight: 700;">{nb_alerte}</div>
</div>
<div style="color: #94A3B8; font-size: 0.9rem;">{nb_alerte/total*100:.0f}%</div>
</div>

<div style="margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid #334155;">
<div style="color: #94A3B8; font-size: 0.8rem; line-height: 1.5;">
<strong>Méthodologie</strong><br>
Enveloppe = Conso. 2011-2021 × 50%<br>
Taux = Conso. 2021-2024 / Enveloppe
</div>
</div>
</div>
""", unsafe_allow_html=True)


def render_densification_evolution(df: pd.DataFrame):
    """
    Infographie 4: Évolution de la Densification
    Comparaison du ratio m²/habitant par période
    """
    
    # Définition des périodes
    periodes = [
        {
            "nom": "2009-2015",
            "cols_artif": ["naf09art10", "naf10art11", "naf11art12", "naf12art13", "naf13art14", "naf14art15"],
            "pop_debut": "pop15",
            "pop_fin": "pop15",  # Approximation
        },
        {
            "nom": "2015-2021",
            "cols_artif": ["naf15art16", "naf16art17", "naf17art18", "naf18art19", "naf19art20", "naf20art21"],
            "pop_col": "pop1521",
        },
        {
            "nom": "2021-2024",
            "cols_artif": ["naf21art22", "naf22art23", "naf23art24"],
            "pop_col": None,  # Sera calculé proportionnellement
        },
    ]
    
    data_periodes = []
    
    # Période 2015-2021
    artif_1521 = 0
    for col in ["naf15art16", "naf16art17", "naf17art18", "naf18art19", "naf19art20", "naf20art21"]:
        if col in df.columns:
            artif_1521 += df[col].sum()
    pop_1521 = df["pop1521"].sum()
    
    if pop_1521 > 0:
        ratio_1521 = artif_1521 / pop_1521
    else:
        ratio_1521 = 0
    
    data_periodes.append({
        "Période": "2015-2021 (Réf.)",
        "Ratio": ratio_1521,
        "Artificialisation": artif_1521 / 10000,
        "Pop_evolution": pop_1521,
    })
    
    # Période 2021-2024 (estimation évolution pop proportionnelle)
    artif_2124 = 0
    for col in ["naf21art22", "naf22art23", "naf23art24"]:
        if col in df.columns:
            artif_2124 += df[col].sum()
    
    # Estimation évolution pop 2021-2024 (proportionnelle à 2015-2021)
    pop_2124_est = pop_1521 * (3/6)  # 3 ans vs 6 ans
    
    if pop_2124_est > 0:
        ratio_2124 = artif_2124 / pop_2124_est
    else:
        ratio_2124 = artif_2124 / 1 if artif_2124 > 0 else 0
    
    data_periodes.append({
        "Période": "2021-2024 (ZAN)",
        "Ratio": ratio_2124,
        "Artificialisation": artif_2124 / 10000,
        "Pop_evolution": pop_2124_est,
    })
    
    df_periodes = pd.DataFrame(data_periodes)
    
    col1, col2 = st.columns([1.2, 0.8])
    
    with col1:
        fig = go.Figure()
        
        colors = ["#2E86AB", "#A23B72"]
        
        fig.add_trace(
            go.Bar(
                x=df_periodes["Période"],
                y=df_periodes["Ratio"],
                marker=dict(
                    color=colors,
                    line=dict(color="#1E293B", width=2),
                ),
                text=df_periodes["Ratio"].apply(lambda x: f"{x:.0f} m²/hab"),
                textposition="outside",
                textfont=dict(size=14, color="#FFFFFF", family="Segoe UI"),
                hovertemplate=(
                    "<b>%{x}</b><br>"
                    "Ratio: %{y:.0f} m²/hab<br>"
                    "<extra></extra>"
                ),
            )
        )
        
        # Lignes de référence
        fig.add_hline(y=200, line_dash="dash", line_color="#48BB78", line_width=2,
                      annotation_text="Objectif efficient (200)", annotation_position="right",
                      annotation_font=dict(size=10, color="#48BB78"))
        
        fig.add_hline(y=500, line_dash="dash", line_color="#ED8936", line_width=2,
                      annotation_text="Seuil consommateur (500)", annotation_position="right",
                      annotation_font=dict(size=10, color="#ED8936"))
        
        fig.update_layout(
            title=dict(
                text="ÉVOLUTION DE L'EFFICIENCE D'URBANISATION",
                font=dict(size=16, color="#FFFFFF", family="Segoe UI"),
                x=0.5,
            ),
            xaxis=dict(
                title="",
                tickfont=dict(size=12, color="#FFFFFF"),
            ),
            yaxis=dict(
                title="m² artificialisés par habitant ajouté",
                tickfont=dict(size=11, color="#94A3B8"),
                gridcolor="#334155",
            ),
            template="plotly_dark",
            height=400,
            showlegend=False,
            margin=dict(t=60, b=40, l=80, r=120),
            paper_bgcolor="#1E293B",
            plot_bgcolor="#0F172A",
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Analyse de la tendance
        if len(df_periodes) >= 2:
            ratio_avant = df_periodes.iloc[0]["Ratio"]
            ratio_apres = df_periodes.iloc[1]["Ratio"]
            variation = ((ratio_apres - ratio_avant) / ratio_avant * 100) if ratio_avant > 0 else 0
            
            if variation < -10:
                tendance = "AMÉLIORATION"
                tendance_color = "#48BB78"
                tendance_icon = "↓"
            elif variation > 10:
                tendance = "DÉGRADATION"
                tendance_color = "#F56565"
                tendance_icon = "↑"
            else:
                tendance = "STABLE"
                tendance_color = "#ED8936"
                tendance_icon = "→"
            
            st.markdown(f"""
<div style="background: #1E293B; border: 1px solid #334155; border-radius: 8px; padding: 1.5rem;">
<div style="color: #FFFFFF; font-weight: 700; font-size: 1rem; margin-bottom: 1.5rem; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 1px solid #334155; padding-bottom: 0.75rem;">ANALYSE DE TENDANCE</div>

<div style="text-align: center; padding: 1.5rem; background: rgba(100, 100, 100, 0.15); border-radius: 8px; margin-bottom: 1.5rem;">
<div style="font-size: 3rem; margin-bottom: 0.5rem;">{tendance_icon}</div>
<div style="color: {tendance_color}; font-size: 1.25rem; font-weight: 700;">{tendance}</div>
<div style="color: #94A3B8; font-size: 0.85rem; margin-top: 0.25rem;">{variation:+.0f}% vs période précédente</div>
</div>

<div style="background: #0F172A; border-radius: 6px; padding: 1rem; margin-bottom: 0.75rem;">
<div style="color: #94A3B8; font-size: 0.75rem; text-transform: uppercase; margin-bottom: 0.25rem;">Période 2015-2021</div>
<div style="color: #FFFFFF; font-size: 1.25rem; font-weight: 700;">{ratio_avant:.0f} m²/hab</div>
</div>

<div style="background: #0F172A; border-radius: 6px; padding: 1rem;">
<div style="color: #94A3B8; font-size: 0.75rem; text-transform: uppercase; margin-bottom: 0.25rem;">Période 2021-2024 (ZAN)</div>
<div style="color: #FFFFFF; font-size: 1.25rem; font-weight: 700;">{ratio_apres:.0f} m²/hab</div>
</div>

<div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #334155; color: #64748B; font-size: 0.75rem; line-height: 1.4;">
<em>Note: L'évolution de population 2021-2024 est estimée proportionnellement à la période précédente.</em>
</div>
</div>
""", unsafe_allow_html=True)


def render_benchmark_radar(df_scot: pd.DataFrame, df_cc: pd.DataFrame):
    """
    Infographie 5: Benchmark SCoT vs CCPDA
    Radar chart multi-critères
    """
    
    def calc_metrics(df, name):
        total_pop = df["pop21"].sum()
        total_artif = df["naf09art24"].sum() / 10000
        evolution_pop = df["pop1521"].sum()
        surface = df["surfcom2024"].sum() / 10000
        
        # Calcul des métriques normalisées
        artif_par_1000hab = (total_artif / total_pop * 1000) if total_pop > 0 else 0
        efficience = (df["naf09art24"].sum() / evolution_pop) if evolution_pop > 0 else 0
        part_habitat = (df["art09hab24"].sum() / df["naf09art24"].sum() * 100) if df["naf09art24"].sum() > 0 else 0
        part_activites = (df["art09act24"].sum() / df["naf09art24"].sum() * 100) if df["naf09art24"].sum() > 0 else 0
        densite = (total_pop / surface) if surface > 0 else 0
        
        # Calcul enveloppe ZAN
        cols_ref = ["naf11art12", "naf12art13", "naf13art14", "naf14art15", "naf15art16",
                    "naf16art17", "naf17art18", "naf18art19", "naf19art20", "naf20art21"]
        conso_ref = sum(df[col].sum() / 10000 for col in cols_ref if col in df.columns)
        enveloppe = conso_ref * 0.5
        
        cols_recent = ["naf21art22", "naf22art23", "naf23art24"]
        conso_recent = sum(df[col].sum() / 10000 for col in cols_recent if col in df.columns)
        taux_zan = (conso_recent / enveloppe * 100) if enveloppe > 0 else 0
        
        return {
            "name": name,
            "Artif./1000 hab": artif_par_1000hab,
            "Efficience (m²/hab)": efficience,
            "Part Habitat (%)": part_habitat,
            "Part Activités (%)": part_activites,
            "Densité (hab/km²)": densite,
            "Conso. enveloppe ZAN (%)": taux_zan,
        }
    
    metrics_scot = calc_metrics(df_scot, "SCoT Rives du Rhône")
    metrics_cc = calc_metrics(df_cc, "CC Porte de DrômArdèche")
    
    categories = ["Artif./1000 hab", "Efficience (m²/hab)", "Part Habitat (%)", 
                  "Part Activités (%)", "Densité (hab/km²)", "Conso. enveloppe ZAN (%)"]
    
    # Normalisation pour le radar (0-100)
    def normalize(val, min_val, max_val):
        if max_val == min_val:
            return 50
        return (val - min_val) / (max_val - min_val) * 100
    
    values_scot = []
    values_cc = []
    
    for cat in categories:
        v_scot = metrics_scot[cat]
        v_cc = metrics_cc[cat]
        min_v = min(v_scot, v_cc) * 0.5
        max_v = max(v_scot, v_cc) * 1.5
        values_scot.append(normalize(v_scot, min_v, max_v))
        values_cc.append(normalize(v_cc, min_v, max_v))
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values_scot + [values_scot[0]],
        theta=categories + [categories[0]],
        fill="toself",
        fillcolor="rgba(46, 134, 171, 0.3)",
        line=dict(color="#2E86AB", width=3),
        name="SCoT Rives du Rhône",
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=values_cc + [values_cc[0]],
        theta=categories + [categories[0]],
        fill="toself",
        fillcolor="rgba(162, 59, 114, 0.3)",
        line=dict(color="#A23B72", width=3),
        name="CC Porte de DrômArdèche",
    ))
    
    fig.update_layout(
        title=dict(
            text="BENCHMARK TERRITORIAL COMPARATIF",
            font=dict(size=18, color="#FFFFFF", family="Segoe UI"),
            x=0.5,
        ),
        polar=dict(
            bgcolor="#0F172A",
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(color="#64748B", size=9),
                gridcolor="#334155",
            ),
            angularaxis=dict(
                tickfont=dict(color="#CBD5E0", size=10),
                gridcolor="#334155",
            ),
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(size=11, color="#CBD5E0"),
        ),
        template="plotly_dark",
        height=500,
        margin=dict(t=80, b=80, l=80, r=80),
        paper_bgcolor="#1E293B",
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Tableau comparatif détaillé
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
<div style="background: rgba(46, 134, 171, 0.1); border: 1px solid #2E86AB; border-radius: 8px; padding: 1.25rem;">
<div style="color: #2E86AB; font-weight: 700; font-size: 1rem; margin-bottom: 1rem; text-transform: uppercase;">SCoT RIVES DU RHÔNE</div>
<table style="width: 100%; border-collapse: collapse;">
<tr style="border-bottom: 1px solid #334155;">
<td style="color: #94A3B8; padding: 0.5rem 0; font-size: 0.85rem;">Artif./1000 hab</td>
<td style="color: #FFFFFF; font-weight: 600; text-align: right; padding: 0.5rem 0;">{metrics_scot['Artif./1000 hab']:.1f} ha</td>
</tr>
<tr style="border-bottom: 1px solid #334155;">
<td style="color: #94A3B8; padding: 0.5rem 0; font-size: 0.85rem;">Efficience</td>
<td style="color: #FFFFFF; font-weight: 600; text-align: right; padding: 0.5rem 0;">{metrics_scot['Efficience (m²/hab)']:.0f} m²/hab</td>
</tr>
<tr style="border-bottom: 1px solid #334155;">
<td style="color: #94A3B8; padding: 0.5rem 0; font-size: 0.85rem;">Part Habitat</td>
<td style="color: #FFFFFF; font-weight: 600; text-align: right; padding: 0.5rem 0;">{metrics_scot['Part Habitat (%)']:.0f}%</td>
</tr>
<tr style="border-bottom: 1px solid #334155;">
<td style="color: #94A3B8; padding: 0.5rem 0; font-size: 0.85rem;">Part Activités</td>
<td style="color: #FFFFFF; font-weight: 600; text-align: right; padding: 0.5rem 0;">{metrics_scot['Part Activités (%)']:.0f}%</td>
</tr>
<tr style="border-bottom: 1px solid #334155;">
<td style="color: #94A3B8; padding: 0.5rem 0; font-size: 0.85rem;">Densité</td>
<td style="color: #FFFFFF; font-weight: 600; text-align: right; padding: 0.5rem 0;">{metrics_scot['Densité (hab/km²)']:.0f} hab/km²</td>
</tr>
<tr>
<td style="color: #94A3B8; padding: 0.5rem 0; font-size: 0.85rem;">Conso. ZAN</td>
<td style="color: #FFFFFF; font-weight: 600; text-align: right; padding: 0.5rem 0;">{metrics_scot['Conso. enveloppe ZAN (%)']:.0f}%</td>
</tr>
</table>
</div>
""", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
<div style="background: rgba(162, 59, 114, 0.1); border: 1px solid #A23B72; border-radius: 8px; padding: 1.25rem;">
<div style="color: #A23B72; font-weight: 700; font-size: 1rem; margin-bottom: 1rem; text-transform: uppercase;">CC PORTE DE DRÔMARDÈCHE</div>
<table style="width: 100%; border-collapse: collapse;">
<tr style="border-bottom: 1px solid #334155;">
<td style="color: #94A3B8; padding: 0.5rem 0; font-size: 0.85rem;">Artif./1000 hab</td>
<td style="color: #FFFFFF; font-weight: 600; text-align: right; padding: 0.5rem 0;">{metrics_cc['Artif./1000 hab']:.1f} ha</td>
</tr>
<tr style="border-bottom: 1px solid #334155;">
<td style="color: #94A3B8; padding: 0.5rem 0; font-size: 0.85rem;">Efficience</td>
<td style="color: #FFFFFF; font-weight: 600; text-align: right; padding: 0.5rem 0;">{metrics_cc['Efficience (m²/hab)']:.0f} m²/hab</td>
</tr>
<tr style="border-bottom: 1px solid #334155;">
<td style="color: #94A3B8; padding: 0.5rem 0; font-size: 0.85rem;">Part Habitat</td>
<td style="color: #FFFFFF; font-weight: 600; text-align: right; padding: 0.5rem 0;">{metrics_cc['Part Habitat (%)']:.0f}%</td>
</tr>
<tr style="border-bottom: 1px solid #334155;">
<td style="color: #94A3B8; padding: 0.5rem 0; font-size: 0.85rem;">Part Activités</td>
<td style="color: #FFFFFF; font-weight: 600; text-align: right; padding: 0.5rem 0;">{metrics_cc['Part Activités (%)']:.0f}%</td>
</tr>
<tr style="border-bottom: 1px solid #334155;">
<td style="color: #94A3B8; padding: 0.5rem 0; font-size: 0.85rem;">Densité</td>
<td style="color: #FFFFFF; font-weight: 600; text-align: right; padding: 0.5rem 0;">{metrics_cc['Densité (hab/km²)']:.0f} hab/km²</td>
</tr>
<tr>
<td style="color: #94A3B8; padding: 0.5rem 0; font-size: 0.85rem;">Conso. ZAN</td>
<td style="color: #FFFFFF; font-weight: 600; text-align: right; padding: 0.5rem 0;">{metrics_cc['Conso. enveloppe ZAN (%)']:.0f}%</td>
</tr>
</table>
</div>
""", unsafe_allow_html=True)


def render_repartition_chart(metrics: dict):
    """
    Affiche le graphique de repartition par destination
    """
    
    categories = []
    valeurs = []
    couleurs = []
    
    data_rep = [
        ("Habitat", metrics.get("artif_habitat_ha", 0), "#48BB78"),
        ("Activites", metrics.get("artif_activites_ha", 0), "#ED8936"),
        ("Mixte", metrics.get("artif_mixte_ha", 0), "#2E86AB"),
        ("Routes", metrics.get("artif_routes_ha", 0), "#64748B"),
        ("Autres", metrics.get("artif_autres_ha", 0), "#DC3545"),
    ]
    
    for cat, val, col in data_rep:
        if val > 0.1:
            categories.append(cat)
            valeurs.append(val)
            couleurs.append(col)
    
    total = sum(valeurs)
    
    fig = go.Figure(data=[go.Pie(
        labels=categories,
        values=valeurs,
        hole=0.5,
        marker=dict(colors=couleurs, line=dict(color="#1E293B", width=2)),
        textinfo="percent",
        textposition="inside",
        textfont=dict(size=14, color="#FFFFFF", family="Segoe UI"),
        hovertemplate="<b>%{label}</b><br>%{value:.1f} ha (%{percent})<extra></extra>",
        pull=[0.02] * len(categories),
    )])
    
    fig.update_layout(
        title=dict(
            text="Repartition par destination",
            font=dict(size=16, color="#FFFFFF", family="Segoe UI"),
            x=0.5,
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(size=12, color="#CBD5E0"),
            bgcolor="rgba(0,0,0,0)",
        ),
        height=450,
        margin=dict(t=60, b=80, l=40, r=40),
        paper_bgcolor="#1E293B",
        annotations=[dict(
            text=f"<b>{total:.0f}</b><br><span style='font-size:12px'>ha total</span>",
            x=0.5, y=0.5,
            font=dict(size=20, color="#FFFFFF"),
            showarrow=False,
        )],
    )
    
    # Ajout de la mention de source
    fig.add_annotation(
        x=0.98, y=0.02,
        xref="paper", yref="paper",
        text=get_data_source_text(),
        showarrow=False,
        font=dict(size=9, color="#64748B"),
        align="right",
        bgcolor="rgba(15, 23, 42, 0.9)",
        bordercolor="#334155",
        borderwidth=1,
        borderpad=4,
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Tableau détaillé sous le graphique
    st.markdown("""
<div style="background: #1E293B; border: 1px solid #334155; border-radius: 8px; padding: 1rem; margin-top: 1rem;">
<div style="color: #FFFFFF; font-weight: 700; font-size: 0.9rem; margin-bottom: 0.75rem; text-transform: uppercase;">Detail par destination</div>
""", unsafe_allow_html=True)
    
    for cat, val, color in data_rep:
        if val > 0.1:
            pct = (val / total * 100) if total > 0 else 0
            st.markdown(f'<div style="display: flex; align-items: center; padding: 0.4rem 0; border-bottom: 1px solid #334155;"><div style="width: 12px; height: 12px; background: {color}; border-radius: 3px; margin-right: 0.75rem;"></div><div style="flex: 1; color: #CBD5E0; font-size: 0.9rem;">{cat}</div><div style="color: #FFFFFF; font-weight: 600; font-size: 0.9rem;">{val:.1f} ha</div><div style="color: #94A3B8; font-size: 0.85rem; margin-left: 0.5rem; width: 55px; text-align: right;">({pct:.1f}%)</div></div>', unsafe_allow_html=True)
    
    st.markdown(f'<div style="display: flex; align-items: center; padding: 0.6rem 0; margin-top: 0.5rem; background: #0F172A; border-radius: 6px; padding-left: 0.75rem; padding-right: 0.75rem;"><div style="flex: 1; color: #FFFFFF; font-weight: 700; font-size: 0.95rem;">TOTAL</div><div style="color: #48BB78; font-weight: 800; font-size: 1.1rem;">{total:.1f} ha</div></div></div>', unsafe_allow_html=True)


def render_top_communes_chart(df: pd.DataFrame, n_top: int = 10):
    """
    Affiche le top communes avec histogramme empilé horizontal par destination + carte
    """
    
    # Colonnes de destination disponibles
    dest_cols = ["art09hab24", "art09act24", "art09mix24", "art09rou24"]
    dest_names = ["Habitat", "Activités", "Mixte", "Routes"]
    dest_colors = ["#48BB78", "#ED8936", "#2E86AB", "#64748B"]
    
    # Sélectionner le top 10 et préparer les données par destination
    cols_needed = ["idcom", "idcomtxt", "artif_total_ha", "pop21", "iddeptxt"] + dest_cols
    cols_available = [c for c in cols_needed if c in df.columns]
    
    df_top = df.nlargest(n_top, "artif_total_ha")[cols_available].copy()
    df_top = df_top.reset_index(drop=True)
    
    # Convertir les colonnes destination en hectares si elles existent
    for col in dest_cols:
        if col in df_top.columns:
            # Si valeurs > 1000, probablement en m², convertir en ha
            if df_top[col].max() > 1000:
                df_top[col] = df_top[col] / 10000
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Trier par total décroissant pour l'affichage
        df_plot = df_top.sort_values("artif_total_ha", ascending=True)
        
        fig = go.Figure()
        
        # Vérifier si on a les colonnes de destination
        has_dest_data = all(col in df_plot.columns for col in dest_cols)
        
        if has_dest_data:
            # Histogramme empilé horizontal par destination
            for dest_name, dest_col, dest_color in zip(dest_names, dest_cols, dest_colors):
                fig.add_trace(
                    go.Bar(
                        y=df_plot["idcomtxt"],
                        x=df_plot[dest_col],
                        name=dest_name,
                        orientation="h",
                        marker=dict(
                            color=dest_color,
                            line=dict(color="#1E293B", width=1),
                        ),
                        hovertemplate=(
                            "<b>%{y}</b><br>"
                            f"{dest_name}: " + "%{x:.2f} ha<br>"
                            "<extra></extra>"
                        ),
                    )
                )
        else:
            # Fallback: barre simple si pas de données par destination
            fig.add_trace(
                go.Bar(
                    y=df_plot["idcomtxt"],
                    x=df_plot["artif_total_ha"],
                    orientation="h",
                    marker=dict(
                        color="#2E86AB",
                        line=dict(color="#1E293B", width=1),
                    ),
                    text=df_plot["artif_total_ha"].apply(lambda x: f"{x:.1f} ha"),
                    textposition="outside",
                    textfont=dict(size=11, color="#FFFFFF"),
                    hovertemplate=(
                        "<b>%{y}</b><br>"
                        "Total: %{x:.2f} ha<br>"
                        "<extra></extra>"
                    ),
                )
            )
        
        fig.update_layout(
            title=dict(
                text=f"TOP {n_top} COMMUNES - ARTIFICIALISATION PAR DESTINATION",
                font=dict(size=14, color="#FFFFFF", family="Segoe UI"),
                x=0.5,
            ),
            xaxis=dict(
                title="Hectares artificialisés (2009-2024)",
                tickfont=dict(size=11, color="#CBD5E0"),
                gridcolor="#334155",
                gridwidth=1,
                showgrid=True,
            ),
            yaxis=dict(
                title="",
                tickfont=dict(size=11, color="#FFFFFF"),
                showgrid=False,
            ),
            barmode="stack",
            template="plotly_dark",
            height=500,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.18,
                xanchor="center",
                x=0.5,
                font=dict(size=11, color="#CBD5E0"),
                bgcolor="rgba(0,0,0,0)",
            ),
            margin=dict(t=80, b=80, l=120, r=40),
            plot_bgcolor="#0F172A",
            paper_bgcolor="#1E293B",
        )
        
        # Ajout de la mention de source
        fig.add_annotation(
            x=0.98, y=0.02,
            xref="paper", yref="paper",
            text=get_data_source_text(),
            showarrow=False,
            font=dict(size=9, color="#64748B"),
            align="right",
            bgcolor="rgba(15, 23, 42, 0.9)",
            bordercolor="#334155",
            borderwidth=1,
            borderpad=4,
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
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
<div style="display: flex; align-items: center; padding: 0.6rem; background: {'#262730' if rang % 2 == 0 else '#1E2229'}; border-radius: 6px; margin-bottom: 0.25rem;">
<div style="width: 32px; height: 32px; background: linear-gradient(135deg, #2E86AB 0%, #1E3A5F 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: 700; font-size: 0.9rem; margin-right: 0.75rem;">{rang}</div>
<div style="flex: 1;">
<div style="color: #FAFAFA; font-weight: 600; font-size: 0.95rem;">{row['idcomtxt']}</div>
<div style="color: #A0AEC0; font-size: 0.8rem;">{row['iddeptxt']} - Pop: {pop_str}</div>
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
            tickfont=dict(size=11, color="#FAFAFA"),
            gridcolor="#E2E8F0",
        ),
        yaxis=dict(
            title="Consommation cumulee (ha)",
            tickfont=dict(size=11, color="#FAFAFA"),
            gridcolor="#E2E8F0",
        ),
        template="plotly_dark",
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
