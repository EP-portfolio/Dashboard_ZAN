# -*- coding: utf-8 -*-
"""
Composant KPIs du Dashboard - Version corrigée
"""

import streamlit as st


def render_kpis(metrics: dict):
    """
    Affiche les indicateurs clés de performance
    """
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        _render_kpi_card(
            icon="🏗️",
            label="ARTIFICIALISATION TOTALE",
            value=f"{metrics['artif_total_ha']:,.0f} ha".replace(",", " "),
            sublabel="Consommation 2009-2024",
            color="#2E86AB"
        )
    
    with col2:
        delta_pop = metrics['evolution_pop']
        delta_str = f"+{delta_pop:,}".replace(",", " ") if delta_pop > 0 else f"{delta_pop:,}".replace(",", " ")
        _render_kpi_card(
            icon="👥",
            label="POPULATION 2021",
            value=f"{metrics['population']:,}".replace(",", " "),
            sublabel=f"Evolution: {delta_str}",
            color="#1D7A4B"
        )
    
    with col3:
        _render_kpi_card(
            icon="📐",
            label="CONSO/HABITANT",
            value=f"{metrics['conso_par_hab']:,.0f} m2".replace(",", " "),
            sublabel="Par habitant ajoute",
            color="#A23B72"
        )
    
    with col4:
        _render_kpi_card(
            icon="🎯",
            label="ENVELOPPE ZAN 2031",
            value=f"{metrics['enveloppe_zan']:,.0f} ha".replace(",", " "),
            sublabel=f"Reste: {metrics['reste_disponible']:,.0f} ha".replace(",", " "),
            color="#D4820A"
        )
    
    with col5:
        taux = (metrics['conso_2021_2024'] / metrics['enveloppe_zan'] * 100) if metrics['enveloppe_zan'] > 0 else 0
        
        if taux < 30:
            status = "CONFORME"
            icon_s = "🟢"
            color = "#1D7A4B"
        elif taux < 50:
            status = "VIGILANCE"
            icon_s = "🟡"
            color = "#D4820A"
        else:
            status = "ALERTE"
            icon_s = "🔴"
            color = "#C53030"
        
        _render_kpi_card(
            icon=icon_s,
            label="STATUT TRAJECTOIRE",
            value=status,
            sublabel=f"{taux:.0f}% de l'enveloppe",
            color=color
        )


def _render_kpi_card(icon: str, label: str, value: str, sublabel: str, color: str):
    """Affiche une carte KPI"""
    
    html = f'''
<div style="background: linear-gradient(135deg, #1E2229 0%, #262730 100%); border: 1px solid #2D3748; border-left: 4px solid {color}; border-radius: 12px; padding: 1.25rem; box-shadow: 0 4px 6px rgba(0,0,0,0.4); min-height: 120px;">
<div style="margin-bottom: 0.5rem;">
<span style="font-size: 1.5rem; margin-right: 0.5rem;">{icon}</span>
<span style="color: #CBD5E0; font-size: 0.7rem; font-weight: 600; letter-spacing: 0.5px;">{label}</span>
</div>
<div style="color: #FAFAFA; font-size: 1.5rem; font-weight: 800; line-height: 1.2; margin-bottom: 0.35rem;">{value}</div>
<div style="color: #A0AEC0; font-size: 0.8rem; font-weight: 500;">{sublabel}</div>
</div>
'''
    
    st.markdown(html, unsafe_allow_html=True)


def render_summary_capsule(metrics: dict, perimetre: str):
    """Affiche une capsule de résumé"""
    
    html = f'''
<div style="background: linear-gradient(135deg, rgba(46, 134, 171, 0.15) 0%, rgba(72, 187, 120, 0.15) 100%); border: 1px solid #2D3748; border-radius: 12px; padding: 1.5rem; margin: 1rem 0; box-shadow: 0 2px 4px rgba(0,0,0,0.3);">
<div style="color: #FAFAFA; margin-bottom: 1rem; font-size: 1.1rem; font-weight: 700;">📊 Synthese - {perimetre}</div>
<table style="width: 100%; border-collapse: collapse;">
<tr>
<td style="background: #1E2229; border-radius: 8px; padding: 0.75rem 1rem; border-left: 3px solid #2E86AB; width: 33%;">
<div style="color: #A0AEC0; font-size: 0.75rem; text-transform: uppercase;">Communes</div>
<div style="color: #FAFAFA; font-size: 1.25rem; font-weight: 700;">{metrics['nb_communes']}</div>
</td>
<td style="width: 1rem;"></td>
<td style="background: #1E2229; border-radius: 8px; padding: 0.75rem 1rem; border-left: 3px solid #48BB78; width: 33%;">
<div style="color: #A0AEC0; font-size: 0.75rem; text-transform: uppercase;">Surface Totale</div>
<div style="color: #FAFAFA; font-size: 1.25rem; font-weight: 700;">{metrics['surface_totale_ha']:,.0f} ha</div>
</td>
<td style="width: 1rem;"></td>
<td style="background: #1E2229; border-radius: 8px; padding: 0.75rem 1rem; border-left: 3px solid #A23B72; width: 33%;">
<div style="color: #A0AEC0; font-size: 0.75rem; text-transform: uppercase;">Taux Artif.</div>
<div style="color: #FAFAFA; font-size: 1.25rem; font-weight: 700;">{metrics['taux_artif_global']:.2f}%</div>
</td>
</tr>
</table>
</div>
'''
    
    st.markdown(html, unsafe_allow_html=True)
