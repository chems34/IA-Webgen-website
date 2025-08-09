# 🚀 **SETUP GITHUB AUTOMATIQUE**

## ⚡ **MÉTHODE ULTRA RAPIDE** (3 commandes)

### 1. **Créer le repository sur GitHub**
- Aller sur https://github.com/new  
- Nom : `ia-webgen-pro`
- Description : `Générateur de sites web avec IA, ChatGPT intégré et mode édition complet`
- **Public** ou **Private** (au choix)
- ⚠️ **NE PAS** cocher : README, .gitignore, license (tout est déjà fourni)
- Cliquer **"Create repository"**

### 2. **Copier ce dossier et exécuter les scripts**
```bash
# Copier le dossier /app vers votre dossier de projets
cp -r /app ~/mes-projets/ia-webgen-pro
cd ~/mes-projets/ia-webgen-pro

# Initialiser GitHub (remplacez YOUR_USERNAME par votre nom d'utilisateur GitHub)
./init_github.sh

# Pousser vers GitHub
git push -u origin main
```

### 3. **Tester localement**
```bash
# Déploiement automatique
./deploy.sh

# Lancer l'application
./start_all.sh
```

**C'est tout ! 🎉**

---

## 📋 **CHECKLIST FINALE**

Après avoir suivi les étapes ci-dessus, vérifiez :

### ✅ **Repository GitHub**
- [ ] Repository créé sur GitHub
- [ ] Code poussé avec succès  
- [ ] README.md visible sur la page principale
- [ ] Tous les fichiers présents (index.html, backend/, etc.)

### ✅ **Application Locale** 
- [ ] `./deploy.sh` exécuté sans erreur
- [ ] Backend démarré sur http://localhost:8001
- [ ] Frontend accessible sur http://localhost:3000
- [ ] API Health check : http://localhost:8001/api/health

### ✅ **Tests Fonctionnels**
- [ ] ChatGPT s'ouvre (icône robot en bas à gauche)
- [ ] Recherche d'images : `/image restaurant` affiche 4 images
- [ ] Mode édition activable avec éléments éditables (bordures bleues)
- [ ] Ajout de section fonctionne
- [ ] Console du navigateur sans erreurs (F12)

---

## 🎯 **URLS IMPORTANTES**

Une fois configuré, vous aurez :

- 🌐 **Application :** http://localhost:3000
- 🔧 **API Backend :** http://localhost:8001  
- 📖 **Documentation API :** http://localhost:8001/docs
- 📱 **Repository GitHub :** https://github.com/VOTRE_USERNAME/ia-webgen-pro
- 📋 **Issues/Support :** https://github.com/VOTRE_USERNAME/ia-webgen-pro/issues

---

## 🆘 **DÉPANNAGE RAPIDE**

### Erreur : "Permission denied"
```bash
chmod +x *.sh
```

### Backend ne démarre pas
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn server:app --host 0.0.0.0 --port 8001
```

### Port 3000 occupé
```bash
# Utiliser un autre port
python -m http.server 3001
```

### Git non configuré
```bash
git config --global user.name "Votre Nom"
git config --global user.email "votre.email@example.com"
```

---

## 🎉 **FÉLICITATIONS !**

Votre application **IA WebGen Pro** est maintenant :
- ✅ **Sur GitHub** avec documentation complète
- ✅ **Fonctionnelle** avec toutes les features critiques  
- ✅ **Prête** pour le développement et la collaboration
- ✅ **Sécurisée** avec backend séparé et clés API protégées

**Profitez de votre nouveau générateur de sites web avec IA ! 🚀**