# -*- coding: utf-8 -*-
"""
Composant KPIs du Dashboard - Version Business Professional
"""

import streamlit as st


def render_kpis(metrics: dict):
    """
    Affiche les indicateurs clés de performance avec un design professionnel
    """
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        _render_kpi_card(
            label="ARTIFICIALISATION TOTALE",
            value=f"{metrics['artif_total_ha']:,.0f}",
            unit="hectares",
            sublabel="Consommation 2009-2024",
            color="#2E86AB"
        )
    
    with col2:
        delta_pop = metrics['evolution_pop']
        delta_str = f"+{delta_pop:,}".replace(",", " ") if delta_pop > 0 else f"{delta_pop:,}".replace(",", " ")
        _render_kpi_card(
            label="POPULATION 2021",
            value=f"{metrics['population']:,}".replace(",", " "),
            unit="habitants",
            sublabel=f"Évolution: {delta_str}",
            color="#48BB78"
        )
    
    with col3:
        _render_kpi_card(
            label="CONSOMMATION PAR HABITANT",
            value=f"{metrics['conso_par_hab']:,.0f}",
            unit="m²",
            sublabel="Par habitant ajouté",
            color="#A23B72"
        )
    
    with col4:
        _render_kpi_card(
            label="ENVELOPPE ZAN 2031",
            value=f"{metrics['enveloppe_zan']:,.0f}",
            unit="hectares",
            sublabel=f"Reste disponible: {metrics['reste_disponible']:,.0f} ha".replace(",", " "),
            color="#ED8936"
        )
    
    with col5:
        taux = (metrics['conso_2021_2024'] / metrics['enveloppe_zan'] * 100) if metrics['enveloppe_zan'] > 0 else 0
        
        if taux < 30:
            status = "CONFORME"
            color = "#48BB78"
        elif taux < 50:
            status = "VIGILANCE"
            color = "#ED8936"
        else:
            status = "ALERTE"
            color = "#F56565"
        
        _render_kpi_card(
            label="STATUT TRAJECTOIRE",
            value=status,
            unit="",
            sublabel=f"{taux:.0f}% de l'enveloppe consommée",
            color=color
        )


def _render_kpi_card(label: str, value: str, unit: str, sublabel: str, color: str):
    """Affiche une carte KPI professionnelle"""
    
    unit_html = f'<span style="color: #94A3B8; font-size: 0.85rem; font-weight: 500; margin-left: 0.25rem;">{unit}</span>' if unit else ''
    
    html = f'''
<div style="background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%); border: 1px solid #334155; border-left: 4px solid {color}; border-radius: 8px; padding: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.3); min-height: 140px; transition: all 0.3s ease;">
<div style="margin-bottom: 1rem;">
<div style="color: #94A3B8; font-size: 0.7rem; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 0.5rem;">{label}</div>
<div style="color: #FFFFFF; font-size: 1.75rem; font-weight: 700; line-height: 1.2; font-family: 'Segoe UI', Arial, sans-serif; display: flex; align-items: baseline;">
{value}{unit_html}
</div>
</div>
<div style="border-top: 1px solid #334155; padding-top: 0.75rem;">
<div style="color: #64748B; font-size: 0.8rem; font-weight: 400; line-height: 1.4;">{sublabel}</div>
</div>
</div>
'''
    
    st.markdown(html, unsafe_allow_html=True)


def render_summary_capsule(metrics: dict, perimetre: str):
    """Affiche une capsule de résumé professionnelle"""
    
    html = f'''
<div style="background: #1E293B; border: 1px solid #334155; border-radius: 8px; padding: 1.75rem; margin: 1.5rem 0; box-shadow: 0 2px 8px rgba(0,0,0,0.3);">
<div style="color: #FFFFFF; margin-bottom: 1.25rem; font-size: 1.1rem; font-weight: 700; letter-spacing: -0.3px; border-bottom: 1px solid #334155; padding-bottom: 0.75rem;">SYNTHÈSE - {perimetre.upper()}</div>
<table style="width: 100%; border-collapse: collapse;">
<tr>
<td style="background: #0F172A; border: 1px solid #334155; border-radius: 6px; padding: 1rem 1.25rem; border-left: 3px solid #2E86AB; width: 33%;">
<div style="color: #94A3B8; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.5rem; font-weight: 600;">Communes</div>
<div style="color: #FFFFFF; font-size: 1.5rem; font-weight: 700; font-family: 'Segoe UI', Arial, sans-serif;">{metrics['nb_communes']}</div>
</td>
<td style="width: 1rem;"></td>
<td style="background: #0F172A; border: 1px solid #334155; border-radius: 6px; padding: 1rem 1.25rem; border-left: 3px solid #48BB78; width: 33%;">
<div style="color: #94A3B8; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.5rem; font-weight: 600;">Surface Totale</div>
<div style="color: #FFFFFF; font-size: 1.5rem; font-weight: 700; font-family: 'Segoe UI', Arial, sans-serif;">{metrics['surface_totale_ha']:,.0f} ha</div>
</td>
<td style="width: 1rem;"></td>
<td style="background: #0F172A; border: 1px solid #334155; border-radius: 6px; padding: 1rem 1.25rem; border-left: 3px solid #A23B72; width: 33%;">
<div style="color: #94A3B8; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.5rem; font-weight: 600;">Taux d'Artificialisation</div>
<div style="color: #FFFFFF; font-size: 1.5rem; font-weight: 700; font-family: 'Segoe UI', Arial, sans-serif;">{metrics['taux_artif_global']:.2f}%</div>
</td>
</tr>
</table>
</div>
'''
    
    st.markdown(html, unsafe_allow_html=True)
