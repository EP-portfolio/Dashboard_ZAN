# 🏗️ Dashboard de Pilotage ZAN

## Description

Tableau de bord interactif pour le suivi de l'artificialisation des sols et le pilotage des objectifs **ZAN** (Zéro Artificialisation Nette).

**Territoire couvert** : SCoT des Rives du Rhône & CC Porte de DrômArdèche

**Source des données** : Observatoire de l'artificialisation des sols (2009-2024)

---

## 🚀 Déploiement sur Streamlit Cloud

Ce Dashboard est configuré pour être déployé sur [Streamlit Cloud](https://streamlit.io/cloud).

### Étapes de déploiement

1. **Connecter le dépôt GitHub à Streamlit Cloud**
   - Allez sur https://share.streamlit.io
   - Connectez votre compte GitHub
   - Sélectionnez le dépôt `EP-portfolio/Dashboard_ZAN`
   - Choisissez le fichier principal : `app.py`

2. **Configuration automatique**
   - Streamlit Cloud détectera automatiquement `requirements.txt`
   - Les données doivent être dans le dossier `data/`

3. **Accès**
   - Votre Dashboard sera accessible via une URL publique
   - Exemple : `https://dashboard-zan.streamlit.app`

---

## 📁 Structure du Projet

```
DASHBOARD/
├── app.py                 # Application principale Streamlit
├── requirements.txt       # Dépendances Python
├── README.md             # Documentation
├── components/           # Composants de l'interface
│   ├── __init__.py
│   ├── header.py         # En-tête du dashboard
│   ├── kpis.py          # Indicateurs clés (KPIs)
│   ├── charts.py        # Graphiques Plotly
│   ├── filters.py       # Filtres sidebar
│   └── tables.py        # Tableaux de données
├── utils/               # Utilitaires
│   ├── __init__.py
│   ├── data_loader.py   # Chargement des données
│   ├── calculations.py  # Calculs des métriques ZAN
│   └── metadata.py      # Métadonnées des données
├── assets/              # Ressources statiques
│   └── styles.css       # Styles CSS personnalisés
├── data/                # Données CSV
│   ├── data_scot_rives_du_rhone.csv
│   └── data_cc_porte_dromeardeche.csv
└── .streamlit/          # Configuration Streamlit
    └── config.toml
```

---

## 🖥️ Installation locale

### Prérequis
- Python 3.9+
- pip

### Installation des dépendances

```bash
cd DASHBOARD
pip install -r requirements.txt
```

### Lancement

```bash
streamlit run app.py
```

Le dashboard sera accessible à l'adresse : `http://localhost:8501`

### Lancement avec accès réseau

```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

Ou utilisez les scripts :
- **Windows** : `lancement_reseau.bat`
- **Linux/Mac** : `./lancement_reseau.sh`

---

## 📊 Fonctionnalités

### Indicateurs Clés (KPIs)
- Artificialisation totale 2009-2024
- Population et évolution
- Consommation par habitant ajouté
- Enveloppe ZAN 2031
- Statut de trajectoire

### Graphiques
- **Trajectoire ZAN** : Suivi de la consommation vs objectif -50%
- **Évolution annuelle** : Historique de consommation par période
- **Répartition** : Camembert par destination (habitat, activités...)
- **Top 10 communes** : Classement avec carte interactive

### Filtres
- Par périmètre (SCoT ou CC)
- Par commune(s)
- Par département(s)

### Tableaux
- Données détaillées par commune
- Recherche et tri
- Export possible

---

## 📝 Données

### Source
- **Observatoire de l'artificialisation des sols**
- **Période** : 2009-2024
- **Format** : CSV avec séparateur point-virgule

### Fichiers requis
- `data/data_scot_rives_du_rhone.csv`
- `data/data_cc_porte_dromeardeche.csv`

---

## 🔧 Configuration

### Fichier `.streamlit/config.toml`
Contient la configuration par défaut pour :
- Adresse d'écoute
- Port
- Thème
- CORS

### Variables d'environnement
Aucune variable d'environnement requise pour le moment.

---

## 📚 Documentation

- `GUIDE_ACCES_RESEAU.md` : Guide d'accès réseau
- `MODIFICATIONS_METADONNEES.md` : Détails des métadonnées
- `CORRECTIONS_APPLIQUEES.md` : Historique des corrections

---

## 🐛 Dépannage

### Erreur de chargement des données
- Vérifiez que les fichiers CSV sont dans le dossier `data/`
- Vérifiez les chemins dans `utils/data_loader.py`

### Problème d'affichage
- Videz le cache Streamlit : `streamlit cache clear`
- Vérifiez la console pour les erreurs

### Problème de carte
- La carte nécessite une connexion internet pour récupérer les coordonnées
- Si l'API geo.api.gouv.fr ne répond pas, un tableau de fallback s'affiche

---

## 📄 Licence

Ce projet est développé pour le suivi de l'artificialisation des sols dans le cadre de la mise en œuvre de la loi Climat et Résilience (objectif ZAN).

---

## 👥 Auteur

Développé pour le suivi ZAN des territoires SCoT Rives du Rhône et CC Porte de DrômArdèche.

---

## 🔗 Liens utiles

- [Streamlit Cloud](https://streamlit.io/cloud)
- [Observatoire de l'artificialisation des sols](https://artificialisation.biodiversite.gouv.fr)
- [Documentation Streamlit](https://docs.streamlit.io)
