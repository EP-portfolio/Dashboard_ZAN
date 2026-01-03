# 🌐 Guide d'Accès Réseau au Dashboard ZAN

## Configuration pour l'accès via navigateur internet

Le Dashboard est configuré pour être accessible depuis n'importe quel appareil sur le réseau local ou internet.

---

## 🚀 Lancement avec accès réseau

### Option 1 : Accès local uniquement (même réseau)
```bash
cd DASHBOARD
streamlit run app.py
```

Le Dashboard sera accessible sur :
- **Local** : `http://localhost:8501`
- **Réseau local** : `http://VOTRE_IP:8501` (ex: `http://192.168.1.100:8501`)

### Option 2 : Accès depuis internet (toutes les adresses)
```bash
cd DASHBOARD
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

Le Dashboard sera accessible sur :
- **Local** : `http://localhost:8501`
- **Réseau local** : `http://VOTRE_IP_LOCALE:8501`
- **Internet** : `http://VOTRE_IP_PUBLIQUE:8501` (si port ouvert)

---

## 📋 Trouver votre adresse IP

### Windows
```powershell
# Adresse IP locale
ipconfig

# Cherchez "Adresse IPv4" dans la section de votre carte réseau
```

### Linux/Mac
```bash
# Adresse IP locale
ifconfig
# ou
ip addr show
```

---

## 🔒 Sécurité et Firewall

### Ouvrir le port dans le Firewall Windows

1. Ouvrir **Pare-feu Windows Defender**
2. Cliquer sur **Paramètres avancés**
3. **Règles de trafic entrant** → **Nouvelle règle**
4. Choisir **Port** → **TCP** → Port spécifique : **8501**
5. Autoriser la connexion
6. Appliquer à tous les profils
7. Nommer la règle : "Dashboard ZAN Streamlit"

### Via PowerShell (Administrateur)
```powershell
New-NetFirewallRule -DisplayName "Dashboard ZAN Streamlit" -Direction Inbound -LocalPort 8501 -Protocol TCP -Action Allow
```

---

## 🌍 Accès depuis Internet (Optionnel)

Pour rendre le Dashboard accessible depuis internet :

1. **Ouvrir le port sur votre routeur** (port forwarding)
   - Port externe : 8501 (ou autre)
   - Port interne : 8501
   - IP interne : Votre adresse IP locale

2. **Utiliser un service de tunnel** (plus simple et sécurisé)
   ```bash
   # Installer ngrok
   ngrok http 8501
   
   # Vous obtiendrez une URL publique comme :
   # https://abc123.ngrok.io
   ```

3. **Utiliser Streamlit Cloud** (recommandé pour production)
   - Déployer sur https://streamlit.io/cloud
   - Accès gratuit avec authentification

---

## 📱 Accès depuis mobile/tablette

Une fois le Dashboard lancé avec `--server.address 0.0.0.0`, vous pouvez y accéder depuis n'importe quel appareil sur le même réseau :

1. Trouvez l'adresse IP de votre ordinateur
2. Sur votre mobile/tablette, ouvrez le navigateur
3. Entrez : `http://VOTRE_IP:8501`

**Exemple** : Si votre IP est `192.168.1.100`, entrez `http://192.168.1.100:8501`

---

## ⚙️ Configuration avancée

Le fichier `.streamlit/config.toml` contient la configuration par défaut :

```toml
[server]
address = "0.0.0.0"  # Écoute sur toutes les interfaces
port = 8501          # Port par défaut
enableCORS = true    # Autorise les requêtes cross-origin
```

Pour changer le port :
```bash
streamlit run app.py --server.port 8080
```

---

## 🔍 Dépannage

### Le Dashboard ne s'ouvre pas depuis un autre appareil

1. **Vérifier que le serveur écoute sur 0.0.0.0**
   ```bash
   netstat -ano | findstr :8501
   # Doit afficher 0.0.0.0:8501 (pas seulement 127.0.0.1:8501)
   ```

2. **Vérifier le firewall**
   - Le port 8501 doit être ouvert

3. **Vérifier que vous êtes sur le même réseau**
   - Les deux appareils doivent être sur le même WiFi/réseau

4. **Tester avec l'IP locale**
   - Utilisez l'IP locale, pas `localhost`

### Erreur "Connection refused"

- Vérifiez que le serveur Streamlit est bien démarré
- Vérifiez que le port n'est pas déjà utilisé
- Essayez un autre port : `--server.port 8502`

---

## 📝 Notes importantes

- ⚠️ **Sécurité** : En mode `0.0.0.0`, le Dashboard est accessible à tous sur le réseau. Pour un usage en production, ajoutez une authentification.

- 🔐 **Recommandation** : Pour un usage professionnel, utilisez :
  - Un reverse proxy (nginx, Apache)
  - HTTPS avec certificat SSL
  - Authentification (Streamlit Authenticator)

- 📊 **Performance** : Le Dashboard peut être lent si plusieurs utilisateurs accèdent simultanément. Pour un usage intensif, considérez un déploiement sur serveur dédié.

---

## ✅ Vérification rapide

1. Lancer le Dashboard :
   ```bash
   streamlit run app.py --server.address 0.0.0.0
   ```

2. Vérifier l'écoute :
   ```bash
   netstat -ano | findstr :8501
   ```

3. Tester depuis un autre appareil :
   - Ouvrir `http://VOTRE_IP:8501` dans un navigateur

Si tout fonctionne, vous verrez le Dashboard ! 🎉


