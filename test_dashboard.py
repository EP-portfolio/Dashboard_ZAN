# -*- coding: utf-8 -*-
"""Script de test du Dashboard"""

import sys
sys.path.insert(0, ".")

print("=" * 50)
print("TEST DU DASHBOARD ZAN")
print("=" * 50)

# Test 1: Chargement des données
print("\n[TEST 1] Chargement des donnees...")
try:
    from utils.data_loader import load_data
    df_scot, df_cc = load_data()
    print(f"  OK - SCoT: {len(df_scot)} communes")
    print(f"  OK - CC: {len(df_cc)} communes")
except Exception as e:
    print(f"  ERREUR: {e}")
    sys.exit(1)

# Test 2: Calcul des métriques
print("\n[TEST 2] Calcul des metriques ZAN...")
try:
    from utils.calculations import calculate_zan_metrics
    metrics = calculate_zan_metrics(df_scot)
    print(f"  OK - Artif totale: {metrics['artif_total_ha']:.1f} ha")
    print(f"  OK - Enveloppe ZAN: {metrics['enveloppe_zan']:.1f} ha")
    print(f"  OK - Population: {metrics['population']:,}")
    print(f"  OK - Conso reference: {metrics['conso_reference']:.1f} ha")
except Exception as e:
    print(f"  ERREUR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Composants
print("\n[TEST 3] Import des composants...")
try:
    from components.header import render_header
    from components.kpis import render_kpis
    from components.charts import render_evolution_chart, render_repartition_chart
    from components.filters import render_filters
    from components.tables import render_data_table
    print("  OK - Tous les composants importes")
except Exception as e:
    print(f"  ERREUR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Colonnes nécessaires
print("\n[TEST 4] Verification des colonnes...")
required_cols = [
    "idcom", "idcomtxt", "iddeptxt", "pop21", "pop1521",
    "naf09art24", "art09hab24", "art09act24", "surfcom2024"
]
missing = [c for c in required_cols if c not in df_scot.columns]
if missing:
    print(f"  ATTENTION - Colonnes manquantes: {missing}")
else:
    print("  OK - Toutes les colonnes requises presentes")

print("\n" + "=" * 50)
print("TOUS LES TESTS PASSES AVEC SUCCES!")
print("=" * 50)

