# -*- coding: utf-8 -*-
"""
Composant Header du Dashboard - Version corrigée
"""

import streamlit as st
from datetime import datetime
from utils.metadata import get_data_last_update


def render_header():
    """Affiche l'en-tête du dashboard"""
    
    # Date de dernière récolte des données
    data_update = get_data_last_update()
    date_str = datetime.now().strftime('%d/%m/%Y')
    
    html = f'''
<div style="background: linear-gradient(135deg, #1E3A5F 0%, #2E5A8F 100%); border-radius: 16px; padding: 2rem; margin-bottom: 1.5rem; box-shadow: 0 10px 25px rgba(30, 58, 95, 0.3);">
<table style="width: 100%; border-collapse: collapse;">
<tr>
<td style="width: 60px; vertical-align: middle;">
<div style="background: rgba(255,255,255,0.15); border-radius: 12px; padding: 0.75rem; text-align: center;">
<span style="font-size: 2.5rem;">🏗️</span>
</div>
</td>
<td style="vertical-align: middle; padding-left: 1rem;">
<div style="color: white; font-size: 1.75rem; font-weight: 800; margin: 0; letter-spacing: -0.5px;">Dashboard de Pilotage ZAN</div>
<div style="color: rgba(255,255,255,0.8); font-size: 0.95rem; margin-top: 0.25rem; font-weight: 500;">Suivi de l'artificialisation des sols - Objectif Zéro Artificialisation Nette</div>
</td>
<td style="width: 180px; vertical-align: middle; text-align: right;">
<div style="background: rgba(255,255,255,0.1); border-radius: 8px; padding: 0.75rem 1rem; margin-bottom: 0.5rem;">
<div style="color: rgba(255,255,255,0.7); font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1px;">Dernière récolte</div>
<div style="color: white; font-size: 1rem; font-weight: 600;">{data_update}</div>
</div>
<div style="background: rgba(255,255,255,0.1); border-radius: 8px; padding: 0.75rem 1rem;">
<div style="color: rgba(255,255,255,0.7); font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1px;">Consultation</div>
<div style="color: white; font-size: 1rem; font-weight: 600;">{date_str}</div>
</div>
</td>
</tr>
</table>
</div>
'''
    
    st.markdown(html, unsafe_allow_html=True)


def render_section_header(title: str, icon: str = "📊", description: str = None):
    """
    Affiche un en-tête de section stylisé
    """
    
    desc_html = ""
    if description:
        desc_html = f'<div style="color: #718096; font-size: 0.9rem; margin-top: 0.5rem;">{description}</div>'
    
    html = f'''
<div style="background: linear-gradient(135deg, #F7FAFC 0%, #EDF2F7 100%); border-radius: 10px; padding: 1rem 1.25rem; margin: 1.5rem 0 1rem 0; border-left: 4px solid #2E86AB;">
<table style="border-collapse: collapse;">
<tr>
<td style="vertical-align: middle; padding-right: 0.75rem;"><span style="font-size: 1.5rem;">{icon}</span></td>
<td style="vertical-align: middle;"><span style="color: #1E3A5F; font-size: 1.15rem; font-weight: 700;">{title}</span></td>
</tr>
</table>
{desc_html}
</div>
'''
    
    st.markdown(html, unsafe_allow_html=True)
