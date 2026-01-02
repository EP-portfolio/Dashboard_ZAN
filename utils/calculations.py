# -*- coding: utf-8 -*-
"""
Module de calculs des métriques ZAN
"""

import pandas as pd
import numpy as np
from typing import Dict


def calculate_zan_metrics(df: pd.DataFrame) -> Dict:
    """
    Calcule l'ensemble des métriques ZAN pour un périmètre donné
    
    Args:
        df: DataFrame contenant les données du territoire
    
    Returns:
        Dictionnaire contenant toutes les métriques
    """
    
    metrics = {}
    
    # ========================================
    # 1. ARTIFICIALISATION TOTALE 2009-2024
    # ========================================
    metrics["artif_total_ha"] = df["naf09art24"].sum() / 10000
    
    # Par destination
    metrics["artif_habitat_ha"] = df["art09hab24"].sum() / 10000
    metrics["artif_activites_ha"] = df["art09act24"].sum() / 10000
    metrics["artif_mixte_ha"] = df["art09mix24"].sum() / 10000
    metrics["artif_routes_ha"] = df["art09rou24"].sum() / 10000
    metrics["artif_fer_ha"] = df.get("art09fer24", pd.Series([0])).sum() / 10000
    metrics["artif_inconnu_ha"] = df.get("art09inc24", pd.Series([0])).sum() / 10000
    metrics["artif_autres_ha"] = metrics["artif_fer_ha"] + metrics["artif_inconnu_ha"]
    
    # ========================================
    # 2. DÉMOGRAPHIE
    # ========================================
    metrics["population"] = int(df["pop21"].sum())
    metrics["population_2015"] = int(df["pop15"].sum())
    metrics["evolution_pop"] = int(df["pop1521"].sum())
    metrics["menages"] = int(df["men21"].sum())
    metrics["emplois"] = int(df["emp21"].sum())
    
    # ========================================
    # 3. RATIOS D'EFFICACITÉ
    # ========================================
    if metrics["evolution_pop"] > 0:
        metrics["conso_par_hab"] = (df["naf09art24"].sum() / metrics["evolution_pop"])
    else:
        metrics["conso_par_hab"] = 0
    
    # Taux d'artificialisation global
    surface_totale = df["surfcom2024"].sum()
    if surface_totale > 0:
        metrics["taux_artif_global"] = (df["naf09art24"].sum() / surface_totale * 100)
    else:
        metrics["taux_artif_global"] = 0
    
    # ========================================
    # 4. CALCULS ZAN
    # ========================================
    
    # Période de référence 2011-2021 (10 ans)
    cols_ref = [
        "naf11art12", "naf12art13", "naf13art14", "naf14art15", "naf15art16",
        "naf16art17", "naf17art18", "naf18art19", "naf19art20", "naf20art21"
    ]
    
    conso_ref = 0
    for col in cols_ref:
        if col in df.columns:
            conso_ref += df[col].sum() / 10000
    
    metrics["conso_reference"] = conso_ref
    
    # Enveloppe ZAN 2021-2031 (-50%)
    metrics["enveloppe_zan"] = conso_ref * 0.5
    
    # Consommation 2021-2024 (3 ans)
    cols_recent = ["naf21art22", "naf22art23", "naf23art24"]
    
    conso_recent = 0
    for col in cols_recent:
        if col in df.columns:
            conso_recent += df[col].sum() / 10000
    
    metrics["conso_2021_2024"] = conso_recent
    
    # Reste disponible
    metrics["reste_disponible"] = max(0, metrics["enveloppe_zan"] - conso_recent)
    
    # Consommation annuelle moyenne période récente
    metrics["conso_annuelle_moyenne"] = conso_recent / 3 if conso_recent > 0 else 0
    
    # Projection linéaire
    annees_restantes = 7  # 2025-2031
    metrics["projection_2031"] = conso_recent + (metrics["conso_annuelle_moyenne"] * annees_restantes)
    
    # Écart à l'objectif
    metrics["ecart_objectif"] = metrics["projection_2031"] - metrics["enveloppe_zan"]
    
    # ========================================
    # 5. STATISTIQUES TERRITORIALES
    # ========================================
    metrics["nb_communes"] = len(df)
    metrics["surface_totale_ha"] = surface_totale / 10000
    
    # Moyenne par commune
    metrics["artif_moyenne_commune"] = metrics["artif_total_ha"] / metrics["nb_communes"]
    
    # Médiane
    if "artif_total_ha" in df.columns:
        metrics["artif_mediane_commune"] = df["artif_total_ha"].median()
    else:
        metrics["artif_mediane_commune"] = (df["naf09art24"] / 10000).median()
    
    return metrics


def calculate_commune_ranking(df: pd.DataFrame, metric: str = "artif_total_ha") -> pd.DataFrame:
    """
    Calcule le classement des communes selon une métrique
    
    Args:
        df: DataFrame des communes
        metric: Colonne sur laquelle calculer le classement
    
    Returns:
        DataFrame avec le classement
    """
    
    df_ranked = df.copy()
    df_ranked["rang"] = df_ranked[metric].rank(ascending=False, method="min").astype(int)
    df_ranked = df_ranked.sort_values("rang")
    
    return df_ranked


def calculate_annual_trajectory(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcule la trajectoire annuelle de consommation
    
    Args:
        df: DataFrame des communes
    
    Returns:
        DataFrame avec les données annuelles
    """
    
    cols_annuelles = [
        ("naf09art10", 2010),
        ("naf10art11", 2011),
        ("naf11art12", 2012),
        ("naf12art13", 2013),
        ("naf13art14", 2014),
        ("naf14art15", 2015),
        ("naf15art16", 2016),
        ("naf16art17", 2017),
        ("naf17art18", 2018),
        ("naf18art19", 2019),
        ("naf19art20", 2020),
        ("naf20art21", 2021),
        ("naf21art22", 2022),
        ("naf22art23", 2023),
        ("naf23art24", 2024),
    ]
    
    data = []
    cumul = 0
    
    for col, annee in cols_annuelles:
        if col in df.columns:
            conso = df[col].sum() / 10000
            cumul += conso
            data.append({
                "annee": annee,
                "consommation_annuelle": conso,
                "consommation_cumulee": cumul,
            })
    
    return pd.DataFrame(data)

