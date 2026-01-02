# -*- coding: utf-8 -*-
"""
Module de chargement des données
"""

import pandas as pd
from pathlib import Path
from typing import Tuple


def load_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Charge les données des deux périmètres d'étude
    
    Returns:
        Tuple contenant (df_scot, df_cc)
    """
    
    # Chemins vers les fichiers de données
    # Essayer d'abord dans le dossier data/ (pour Streamlit Cloud)
    # Sinon dans le dossier parent (pour développement local)
    base_path = Path(__file__).parent.parent
    data_dir = base_path / "data"
    parent_dir = base_path.parent
    
    # Chercher les fichiers dans data/ d'abord, puis dans le parent
    scot_path = data_dir / "data_scot_rives_du_rhone.csv"
    cc_path = data_dir / "data_cc_porte_dromeardeche.csv"
    
    if not scot_path.exists():
        scot_path = parent_dir / "data_scot_rives_du_rhone.csv"
    if not cc_path.exists():
        cc_path = parent_dir / "data_cc_porte_dromeardeche.csv"
    
    # Charger les données
    df_scot = pd.read_csv(scot_path, sep=";", encoding="utf-8-sig", low_memory=False)
    df_cc = pd.read_csv(cc_path, sep=";", encoding="utf-8-sig", low_memory=False)
    
    # Préparer les données
    df_scot = prepare_data(df_scot)
    df_cc = prepare_data(df_cc)
    
    return df_scot, df_cc


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prépare et nettoie les données
    
    Args:
        df: DataFrame brut
    
    Returns:
        DataFrame nettoyé
    """
    
    # Liste des colonnes numériques à convertir
    numeric_cols = [
        # Colonnes d'artificialisation cumulée
        "naf09art24", "art09act24", "art09hab24", "art09mix24",
        "art09rou24", "art09fer24", "art09inc24",
        # Colonnes démographiques
        "pop15", "pop21", "pop1521",
        "men15", "men21", "men1521",
        "emp15", "emp21", "emp1521",
        # Surface
        "surfcom2024",
        # Colonnes calculées
        "artif_total_ha", "artif_habitat_ha", "artif_activites_ha",
        "taux_artif", "artif_par_habitant", "part_habitat",
    ]
    
    # Colonnes annuelles
    for year_start in range(9, 24):
        for year_end in range(10, 25):
            if year_end == year_start + 1:
                col = f"naf{year_start:02d}art{year_end:02d}"
                if col not in numeric_cols:
                    numeric_cols.append(col)
    
    # Conversion en numérique
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    
    # S'assurer que les colonnes calculées existent
    if "artif_total_ha" not in df.columns:
        df["artif_total_ha"] = df.get("naf09art24", 0) / 10000
    
    if "artif_habitat_ha" not in df.columns:
        df["artif_habitat_ha"] = df.get("art09hab24", 0) / 10000
    
    if "artif_activites_ha" not in df.columns:
        df["artif_activites_ha"] = df.get("art09act24", 0) / 10000
    
    return df

