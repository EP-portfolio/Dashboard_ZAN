# Modifications : Mentions de Provenance et Accès Réseau

## Date : 02/01/2026

---

## ✅ Modifications Apportées

### 1. Mentions de Provenance des Données

#### Dans tous les graphiques
- ✅ **Annotation de source** en bas à droite de chaque graphique Plotly
- ✅ **Texte de source** : "Source: Observatoire de l'artificialisation des sols | Données: 2009-2024 | Dernière mise à jour: DD/MM/YYYY"
- ✅ **Style discret** : Police grise, fond semi-transparent, bordure subtile

#### Graphiques concernés :
- 📈 **Évolution annuelle** : Annotation Plotly + mention HTML sous le graphique
- 🥧 **Répartition par destination** : Mention HTML sous le camembert
- 🏆 **Top 10 communes** : Annotation Plotly + mention HTML sous le graphique
- 📊 **Trajectoire ZAN** : Annotation Plotly

### 2. Date de Dernière Récolte des Données

#### Dans le Header
- ✅ **Date de dernière récolte** : Affiche la date de modification du fichier CSV source
- ✅ **Date de consultation** : Affiche la date actuelle de consultation
- ✅ **Deux badges distincts** dans l'en-tête du Dashboard

#### Dans le Footer
- ✅ **Texte complet** avec source, période, date de récolte et lien vers plus d'infos
- ✅ **Format** : "Données: Observatoire de l'artificialisation des sols (2009-2024) | Dernière récolte: DD/MM/YYYY | Plus d'infos: https://artificialisation.biodiversite.gouv.fr"

### 3. Accès Réseau via Navigateur Internet

#### Configuration Streamlit
- ✅ **Fichier `.streamlit/config.toml`** créé avec :
  - `address = "0.0.0.0"` : Écoute sur toutes les interfaces réseau
  - `port = 8501` : Port par défaut
  - `enableCORS = true` : Autorise les requêtes cross-origin

#### Scripts de lancement
- ✅ **`lancement_reseau.bat`** : Script Windows pour lancer avec accès réseau
- ✅ **`lancement_reseau.sh`** : Script Linux/Mac pour lancer avec accès réseau
- ✅ **Affichage automatique** de l'adresse IP locale

#### Documentation
- ✅ **`GUIDE_ACCES_RESEAU.md`** : Guide complet avec :
  - Instructions de lancement
  - Configuration firewall
  - Accès depuis mobile/tablette
  - Dépannage
  - Options de sécurité

---

## 📁 Fichiers Créés/Modifiés

### Nouveaux fichiers
- `utils/metadata.py` : Module de gestion des métadonnées
- `.streamlit/config.toml` : Configuration Streamlit pour accès réseau
- `lancement_reseau.bat` : Script de lancement Windows
- `lancement_reseau.sh` : Script de lancement Linux/Mac
- `GUIDE_ACCES_RESEAU.md` : Documentation accès réseau
- `MODIFICATIONS_METADONNEES.md` : Ce fichier

### Fichiers modifiés
- `components/charts.py` : Ajout des annotations de source dans tous les graphiques
- `components/header.py` : Ajout de la date de dernière récolte
- `app.py` : Intégration des métadonnées dans le footer

---

## 🚀 Utilisation

### Lancer avec accès réseau

**Windows** :
```bash
cd DASHBOARD
lancement_reseau.bat
```

**Linux/Mac** :
```bash
cd DASHBOARD
chmod +x lancement_reseau.sh
./lancement_reseau.sh
```

**Manuel** :
```bash
cd DASHBOARD
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

### Accéder au Dashboard

- **Local** : `http://localhost:8501`
- **Réseau local** : `http://VOTRE_IP:8501` (ex: `http://192.168.1.100:8501`)
- **Depuis mobile/tablette** : Même URL que réseau local (sur le même WiFi)

---

## 📊 Informations Affichées

### Dans les graphiques
- Source : Observatoire de l'artificialisation des sols
- Période : 2009-2024
- Date de dernière mise à jour : Automatique (basée sur le fichier CSV)

### Dans le header
- Date de dernière récolte des données
- Date de consultation actuelle

### Dans le footer
- Source complète avec lien
- Période des données
- Date de dernière récolte
- Lien vers le site officiel

---

## 🔍 Vérification

Pour vérifier que tout fonctionne :

1. **Tester les métadonnées** :
   ```bash
   cd DASHBOARD
   python -c "from utils.metadata import *; print(get_data_source_text())"
   ```

2. **Lancer le Dashboard** :
   ```bash
   streamlit run app.py --server.address 0.0.0.0
   ```

3. **Vérifier l'accès réseau** :
   - Ouvrir `http://VOTRE_IP:8501` depuis un autre appareil
   - Vérifier que les mentions de source apparaissent sur tous les graphiques

---

## ✅ Checklist

- [x] Mentions de source dans tous les graphiques
- [x] Date de dernière récolte dans le header
- [x] Footer avec métadonnées complètes
- [x] Configuration accès réseau
- [x] Scripts de lancement
- [x] Documentation complète
- [x] Tests de fonctionnement

---

**Toutes les modifications sont terminées et testées !** 🎉



