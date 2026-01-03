#!/bin/bash
# Script de lancement du Dashboard avec accès réseau
# ===================================================

echo "========================================"
echo "  DASHBOARD ZAN - Lancement Réseau"
echo "========================================"
echo ""

# Changer vers le répertoire du Dashboard
cd "$(dirname "$0")"

# Afficher l'adresse IP locale
echo "Récupération de l'adresse IP locale..."
IP=$(hostname -I | awk '{print $1}')
echo ""
echo "Votre adresse IP locale: $IP"
echo ""

# Lancer Streamlit avec accès réseau
echo "Lancement du Dashboard..."
echo ""
echo "Le Dashboard sera accessible sur:"
echo "  - Local: http://localhost:8501"
echo "  - Réseau: http://$IP:8501"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter le serveur"
echo ""

streamlit run app.py --server.address 0.0.0.0 --server.port 8501


