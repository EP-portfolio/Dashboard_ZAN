# -*- coding: utf-8 -*-
"""
Composant Header du Dashboard - Version Business Professional
"""

import streamlit as st
from datetime import datetime
from utils.metadata import get_data_last_update


def render_header():
    """Affiche l'en-tête professionnel du dashboard"""
    
    # Date de dernière récolte des données
    data_update = get_data_last_update()
    date_str = datetime.now().strftime('%d/%m/%Y')
    
    html = f'''
<div style="background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); border-bottom: 3px solid #2E86AB; padding: 2.5rem 2rem; margin-bottom: 2rem; box-shadow: 0 4px 12px rgba(0,0,0,0.5);">
<table style="width: 100%; border-collapse: collapse;">
<tr>
<td style="vertical-align: middle; padding-right: 2rem;">
<div style="border-left: 4px solid #2E86AB; padding-left: 1.5rem;">
<div style="color: #FFFFFF; font-size: 1.85rem; font-weight: 700; margin: 0; letter-spacing: -0.5px; font-family: 'Segoe UI', Arial, sans-serif;">DASHBOARD DE PILOTAGE ZAN</div>
<div style="color: #CBD5E0; font-size: 0.95rem; margin-top: 0.5rem; font-weight: 400; letter-spacing: 0.3px;">Suivi de l'artificialisation des sols - Objectif Zéro Artificialisation Nette</div>
</div>
</td>
<td style="width: 280px; vertical-align: middle; text-align: right;">
<div style="background: rgba(46, 134, 171, 0.15); border: 1px solid rgba(46, 134, 171, 0.3); border-radius: 8px; padding: 1rem 1.25rem; margin-bottom: 0.75rem;">
<div style="color: #94A3B8; font-size: 0.65rem; text-transform: uppercase; letter-spacing: 1.2px; font-weight: 600; margin-bottom: 0.25rem;">Dernière mise à jour</div>
<div style="color: #FFFFFF; font-size: 1rem; font-weight: 600; font-family: 'Courier New', monospace;">{data_update}</div>
</div>
<div style="background: rgba(46, 134, 171, 0.15); border: 1px solid rgba(46, 134, 171, 0.3); border-radius: 8px; padding: 1rem 1.25rem;">
<div style="color: #94A3B8; font-size: 0.65rem; text-transform: uppercase; letter-spacing: 1.2px; font-weight: 600; margin-bottom: 0.25rem;">Date de consultation</div>
<div style="color: #FFFFFF; font-size: 1rem; font-weight: 600; font-family: 'Courier New', monospace;">{date_str}</div>
</div>
</td>
</tr>
</table>
</div>
'''
    
    st.markdown(html, unsafe_allow_html=True)


def render_section_header(title: str, icon: str = "", description: str = None):
    """
    Affiche un en-tête de section professionnel
    """
    
    icon_html = f'<span style="font-size: 1.2rem; margin-right: 0.75rem; color: #2E86AB;">{icon}</span>' if icon else ''
    
    desc_html = ""
    if description:
        desc_html = f'<div style="color: #94A3B8; font-size: 0.875rem; margin-top: 0.5rem; font-weight: 400; line-height: 1.5;">{description}</div>'
    
    html = f'''
<div style="background: #1E293B; border-left: 4px solid #2E86AB; border-radius: 0 8px 8px 0; padding: 1.25rem 1.5rem; margin: 2rem 0 1.5rem 0; box-shadow: 0 2px 8px rgba(0,0,0,0.3);">
<div style="display: flex; align-items: center; margin-bottom: 0.25rem;">
{icon_html}
<span style="color: #FFFFFF; font-size: 1.25rem; font-weight: 700; letter-spacing: -0.3px; font-family: 'Segoe UI', Arial, sans-serif;">{title}</span>
</div>
{desc_html}
</div>
'''
    
    st.markdown(html, unsafe_allow_html=True)
