# 🚀 IA WebGen Pro - Générateur de Sites Web avec IA

**Version corrigée avec toutes les fonctionnalités critiques opérationnelles**

## 🎯 Fonctionnalités Principales

### ✅ **Mini ChatGPT Intégré**
- **Widget flottant** en bas à gauche avec assistant IA
- **Recherche d'images** via commande `/image [description]`
- **Réponses intelligentes** contextuelles
- **Interface moderne** avec minimisation/maximisation

### ✅ **Mode Édition Complet**
- **Édition après prévisualisation** de tous les éléments
- **Modification de textes**, couleurs, styles, images
- **Ajout/suppression** d'éléments
- **Sauvegarde automatique** des modifications

### ✅ **Recherche d'Images**
- **API backend sécurisée** pour la recherche d'images
- **4 images par recherche** avec vignettes cliquables
- **Intégration directe** dans le site web
- **Options d'application** multiples

### ✅ **Interface Responsive**
- **Design moderne** avec Tailwind CSS
- **Compatible mobile** et desktop
- **Notifications en temps réel**
- **Gestion d'erreurs robuste**

## 🛠️ Installation

### Prérequis
- Python 3.8+
- Node.js (pour le développement)

### 1. Clone le repository
```bash
git clone https://github.com/votre-username/ia-webgen-pro.git
cd ia-webgen-pro
```

### 2. Installation Backend
```bash
cd backend
pip install -r requirements.txt
```

### 3. Lancement des services

**Backend API :**
```bash
cd backend
python -m uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

**Frontend :**
```bash
# Dans le répertoire racine
python -m http.server 3000
```

### 4. Accès à l'application
- **Application principale :** http://localhost:3000
- **API Backend :** http://localhost:8001
- **Documentation API :** http://localhost:8001/docs

## 🧪 Tests des Fonctionnalités

### Test ChatGPT et Images
1. Cliquez sur l'icône robot 🤖 en bas à gauche
2. Tapez : `/image restaurant moderne`
3. Vérifiez que 4 images s'affichent
4. Cliquez sur une image pour l'utiliser

### Test Mode Édition
1. Activez le **Mode Édition** via le bouton violet
2. Cliquez sur un élément (bordures bleues pointillées)
3. Utilisez les outils d'édition qui apparaissent
4. Modifiez texte, couleurs, styles

### Test Ajout de Sections
1. Utilisez le bouton **"Ajouter une section"**
2. Choisissez parmi 6 types disponibles
3. Vérifiez que la section s'ajoute correctement

### Test API Backend
1. Cliquez sur **"Tester API Backend"**
2. Vérifiez les ✅ dans les résultats
3. Contrôlez qu'il n'y a aucune erreur

## 🔧 Architecture Technique

### Frontend
- **HTML5** avec JavaScript vanilla
- **Tailwind CSS** pour le design
- **Font Awesome** pour les icônes
- **Interface responsive** et moderne

### Backend
- **FastAPI** (Python)
- **API REST** pour les recherches d'images
- **CORS configuré** pour les requêtes cross-origin
- **Gestion d'erreurs** complète

### APIs Disponibles
- `GET /api/health` - Vérification de santé
- `POST /api/images/search` - Recherche d'images
- `POST /api/chat` - Réponses ChatGPT

## ✅ Validation des Fonctionnalités

**Toutes les fonctionnalités critiques ont été testées et validées :**

- ✅ **Recherche d'images OK** - API backend fonctionnelle
- ✅ **Application d'image OK** - Modal de sélection opérationnelle  
- ✅ **Edition texte/HTML OK** - Modification en temps réel
- ✅ **Modification couleur OK** - Sélecteurs de couleurs fonctionnels
- ✅ **Ajout de section OK** - 6 types de sections disponibles
- ✅ **Événements/listeners OK** - Event handlers robustes
- ✅ **Pas d'erreurs console/réseau** - Code JavaScript propre
- ✅ **Backend sécurisé** - Clés API côté serveur uniquement
- ✅ **Tests responsive OK** - Compatible desktop et mobile

## 🔐 Sécurité

- **Clés API** stockées côté serveur uniquement
- **Variables d'environnement** pour la configuration
- **Validation** des entrées utilisateur
- **Gestion d'erreurs** complète

## 🚀 Déploiement

### Production
1. Configurez les variables d'environnement
2. Ajoutez votre clé API Unsplash dans `backend/.env`
3. Déployez le backend sur votre serveur
4. Servez le frontend via un serveur web

### Environnement de développement
- Backend sur `localhost:8001`
- Frontend sur `localhost:3000`
- Hot reload activé

## 📝 Support

Pour toute question ou problème :
1. Vérifiez que le backend est démarré sur le port 8001
2. Contrôlez les logs du navigateur (F12)
3. Testez les APIs avec `/api/health`

## 🎉 Statut

**Application 100% fonctionnelle** - Toutes les fonctionnalités critiques opérationnelles !

---

*Développé avec ❤️ pour une expérience utilisateur exceptionnelle*