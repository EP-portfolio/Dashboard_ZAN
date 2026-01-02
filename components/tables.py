# -*- coding: utf-8 -*-
"""
Composant Tableaux du Dashboard
"""

import streamlit as st
import pandas as pd


def render_data_table(df: pd.DataFrame):
    """
    Affiche le tableau de données interactif
    
    Args:
        df: DataFrame à afficher
    """
    
    # Colonnes à afficher
    colonnes_affichage = {
        "idcomtxt": "Commune",
        "iddeptxt": "Département",
        "epci24txt": "EPCI",
        "artif_total_ha": "Artif. Totale (ha)",
        "artif_habitat_ha": "Habitat (ha)",
        "artif_activites_ha": "Activités (ha)",
        "pop21": "Population 2021",
        "pop1521": "Évol. Pop.",
        "taux_artif": "Taux Artif. (%)",
        "artif_par_habitant": "m²/hab ajouté",
    }
    
    # Filtrer les colonnes existantes
    cols_existantes = [c for c in colonnes_affichage.keys() if c in df.columns]
    
    # Préparer le DataFrame pour l'affichage
    df_display = df[cols_existantes].copy()
    df_display = df_display.rename(columns={c: colonnes_affichage[c] for c in cols_existantes})
    
    # Formater les nombres
    for col in df_display.columns:
        if "ha" in col or "%" in col:
            df_display[col] = df_display[col].apply(lambda x: f"{x:.2f}" if pd.notna(x) else "-")
        elif "m²" in col:
            df_display[col] = df_display[col].apply(lambda x: f"{x:,.0f}" if pd.notna(x) and x > 0 else "-")
        elif col in ["Population 2021", "Évol. Pop."]:
            df_display[col] = df_display[col].apply(lambda x: f"{int(x):,}" if pd.notna(x) else "-")
    
    # Options d'affichage
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search = st.text_input("🔍 Rechercher une commune", placeholder="Tapez un nom...")
    
    with col2:
        sort_col = st.selectbox(
            "Trier par",
            options=["Artif. Totale (ha)", "Population 2021", "Commune"],
            index=0,
        )
    
    with col3:
        sort_order = st.radio("Ordre", ["Décroissant", "Croissant"], horizontal=True)
    
    # Appliquer la recherche
    if search:
        df_display = df_display[
            df_display["Commune"].str.lower().str.contains(search.lower(), na=False)
        ]
    
    # Appliquer le tri
    ascending = sort_order == "Croissant"
    if sort_col in df_display.columns:
        # Reconvertir en numérique pour le tri si nécessaire
        if sort_col not in ["Commune", "Département", "EPCI"]:
            df_display["_sort"] = pd.to_numeric(
                df_display[sort_col].str.replace(",", "").str.replace("-", "0"),
                errors="coerce"
            )
            df_display = df_display.sort_values("_sort", ascending=ascending)
            df_display = df_display.drop(columns=["_sort"])
        else:
            df_display = df_display.sort_values(sort_col, ascending=ascending)
    
    # Afficher le tableau
    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True,
        height=400,
    )
    
    # Bouton export
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        csv = df[cols_existantes].to_csv(index=False, sep=";", encoding="utf-8-sig")
        st.download_button(
            label="📥 Exporter CSV",
            data=csv,
            file_name="donnees_zan.csv",
            mime="text/csv",
        )
    
    with col2:
        # Pour Excel, on utilise un buffer
        import io
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df[cols_existantes].to_excel(writer, index=False, sheet_name="Données ZAN")
        
        st.download_button(
            label="📥 Exporter Excel",
            data=buffer.getvalue(),
            file_name="donnees_zan.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

