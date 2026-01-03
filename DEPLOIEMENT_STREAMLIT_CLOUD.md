# 🚀 Guide de Déploiement sur Streamlit Cloud

## ✅ Code poussé vers GitHub

Le code du Dashboard a été poussé avec succès vers :
**https://github.com/EP-portfolio/Dashboard_ZAN**

---

## 📋 Étapes de déploiement sur Streamlit Cloud

### 1. Accéder à Streamlit Cloud

1. Allez sur **https://share.streamlit.io**
2. Connectez-vous avec votre compte **GitHub**
3. Autorisez Streamlit Cloud à accéder à vos dépôts

### 2. Créer une nouvelle app

1. Cliquez sur **"New app"** ou **"Deploy an app"**
2. Sélectionnez :
   - **Repository** : `EP-portfolio/Dashboard_ZAN`
   - **Branch** : `main`
   - **Main file path** : `app.py`

### 3. Configuration automatique

Streamlit Cloud détectera automatiquement :
- ✅ `requirements.txt` pour les dépendances
- ✅ `app.py` comme point d'entrée
- ✅ Les fichiers dans `data/` pour les données

### 4. Déploiement

1. Cliquez sur **"Deploy"**
2. Attendez la fin du déploiement (2-5 minutes)
3. Votre Dashboard sera accessible via une URL publique :
   - Exemple : `https://dashboard-zan.streamlit.app`

---

## ⚙️ Configuration avancée (optionnel)

### Variables d'environnement

Si vous avez besoin de variables d'environnement :
1. Dans Streamlit Cloud, allez dans **Settings**
2. Section **Secrets**
3. Ajoutez vos variables au format TOML

### Fichier de secrets

Créez un fichier `.streamlit/secrets.toml` (ne sera pas versionné) :

```toml
# Exemple de secrets (si nécessaire)
# [secrets]
# api_key = "votre_cle_api"
```

---

## 🔍 Vérification du déploiement

### Checklist

- [ ] Le dépôt GitHub contient tous les fichiers nécessaires
- [ ] `requirements.txt` est présent et complet
- [ ] `app.py` est à la racine du dépôt
- [ ] Les fichiers CSV sont dans `data/`
- [ ] Le déploiement sur Streamlit Cloud est réussi
- [ ] L'application est accessible via l'URL publique

### Tests à effectuer

1. **Chargement des données**
   - Vérifiez que les données se chargent correctement
   - Les KPIs doivent s'afficher

2. **Graphiques**
   - Tous les graphiques doivent s'afficher
   - Les mentions de source doivent être visibles

3. **Filtres**
   - Testez les filtres par périmètre
   - Testez les filtres par commune

4. **Carte**
   - La carte doit s'afficher (nécessite internet)
   - Sinon, le tableau de fallback doit apparaître

---

## 🐛 Dépannage

### Erreur : "Module not found"

**Solution** : Vérifiez que toutes les dépendances sont dans `requirements.txt`

### Erreur : "File not found" pour les données

**Solution** : 
- Vérifiez que les fichiers CSV sont dans `data/`
- Vérifiez les chemins dans `utils/data_loader.py`

### Erreur : "Streamlit version incompatible"

**Solution** : Mettez à jour `requirements.txt` avec une version compatible :
```
streamlit>=1.28.0
```

### L'application ne se charge pas

**Solution** :
1. Vérifiez les logs dans Streamlit Cloud
2. Vérifiez que `app.py` est bien à la racine
3. Vérifiez la syntaxe Python

---

## 📊 Structure requise pour Streamlit Cloud

```
Dashboard_ZAN/
├── app.py                    # ✅ Point d'entrée principal
├── requirements.txt          # ✅ Dépendances Python
├── README.md                 # ✅ Documentation
├── .streamlit/
│   └── config.toml           # ✅ Configuration (optionnel)
├── components/               # ✅ Composants
├── utils/                    # ✅ Utilitaires
├── assets/                   # ✅ Ressources statiques
└── data/                     # ✅ Données CSV
    ├── data_scot_rives_du_rhone.csv
    └── data_cc_porte_dromeardeche.csv
```

---

## 🔄 Mise à jour de l'application

Pour mettre à jour l'application après des modifications :

1. **Modifier le code localement**
2. **Commit et push vers GitHub** :
   ```bash
   git add .
   git commit -m "Description des modifications"
   git push origin main
   ```
3. **Streamlit Cloud redéploiera automatiquement** (dans les 1-2 minutes)

---

## 🔗 Liens utiles

- **Streamlit Cloud** : https://share.streamlit.io
- **Documentation Streamlit Cloud** : https://docs.streamlit.io/streamlit-community-cloud
- **Dépôt GitHub** : https://github.com/EP-portfolio/Dashboard_ZAN

---

## ✅ Statut actuel

- ✅ Code poussé vers GitHub
- ✅ Structure prête pour Streamlit Cloud
- ✅ Fichiers de données inclus
- ✅ Requirements.txt complet
- ⏳ **En attente** : Déploiement sur Streamlit Cloud

**Prochaine étape** : Connecter le dépôt à Streamlit Cloud et déployer ! 🚀


