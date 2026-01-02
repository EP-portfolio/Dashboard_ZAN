# -*- coding: utf-8 -*-
"""Script de verification des donnees"""

import sys
sys.path.insert(0, ".")

from utils.data_loader import load_data
from utils.calculations import calculate_zan_metrics

df_scot, df_cc = load_data()
metrics = calculate_zan_metrics(df_scot)

print("=== VERIFICATION REPARTITION ===")
print(f"Artif total: {metrics['artif_total_ha']:.1f} ha")
print(f"Habitat: {metrics['artif_habitat_ha']:.1f} ha")
print(f"Activites: {metrics['artif_activites_ha']:.1f} ha")
print(f"Mixte: {metrics['artif_mixte_ha']:.1f} ha")
print(f"Routes: {metrics['artif_routes_ha']:.1f} ha")
print(f"Autres (fer+inconnu): {metrics['artif_autres_ha']:.1f} ha")

total_calc = metrics['artif_habitat_ha'] + metrics['artif_activites_ha'] + metrics['artif_mixte_ha'] + metrics['artif_routes_ha'] + metrics['artif_autres_ha']
print(f"Total calcule: {total_calc:.1f} ha")
print(f"Ecart: {metrics['artif_total_ha'] - total_calc:.1f} ha")

print("")
print("=== COLONNES BRUTES ===")
print(f"naf09art24: {df_scot['naf09art24'].sum() / 10000:.1f} ha")
print(f"art09hab24: {df_scot['art09hab24'].sum() / 10000:.1f} ha")
print(f"art09act24: {df_scot['art09act24'].sum() / 10000:.1f} ha")
print(f"art09mix24: {df_scot['art09mix24'].sum() / 10000:.1f} ha")
print(f"art09rou24: {df_scot['art09rou24'].sum() / 10000:.1f} ha")
print(f"art09fer24: {df_scot['art09fer24'].sum() / 10000:.1f} ha")
print(f"art09inc24: {df_scot['art09inc24'].sum() / 10000:.1f} ha")

print("")
print("=== COLONNES ANNUELLES ===")
cols = ['naf09art10', 'naf10art11', 'naf11art12', 'naf20art21', 'naf21art22', 'naf22art23', 'naf23art24']
for col in cols:
    if col in df_scot.columns:
        val = df_scot[col].sum() / 10000
        print(f"{col}: {val:.1f} ha")

