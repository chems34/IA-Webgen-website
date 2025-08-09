# 🤝 Guide de Contribution - IA WebGen Pro

Merci de votre intérêt pour contribuer à IA WebGen Pro ! Ce guide vous aidera à démarrer.

## 🚀 Démarrage Rapide

### 1. Fork et Clone
```bash
# Fork le projet sur GitHub, puis :
git clone https://github.com/votre-username/ia-webgen-pro.git
cd ia-webgen-pro
```

### 2. Installation
```bash
# Déploiement automatique
chmod +x deploy.sh
./deploy.sh

# Ou manuellement :
cd backend && pip install -r requirements.txt
```

### 3. Développement
```bash
# Démarrer tous les services
./start_all.sh

# Ou séparément :
./start_backend.sh    # Port 8001
./start_frontend.sh   # Port 3000
```

## 📋 Types de Contributions

### 🐛 Correction de Bugs
1. Vérifiez qu'un issue n'existe pas déjà
2. Créez un issue décrivant le bug
3. Référencez l'issue dans votre PR

### ✨ Nouvelles Fonctionnalités
1. Discutez d'abord dans les issues
2. Créez une branche : `feature/ma-fonctionnalite`
3. Développez en suivant les standards
4. Ajoutez des tests si nécessaire

### 📚 Documentation
- Améliorations du README
- Commentaires de code
- Guides d'utilisation
- Exemples

## 🔧 Standards de Développement

### Structure du Code

#### Frontend (JavaScript)
```javascript
// ✅ Bon
function searchImages(query) {
    console.log('Recherche:', query);
    // Code avec gestion d'erreurs
    try {
        // Logique principale
    } catch (error) {
        console.error('Erreur:', error);
        showNotification('❌ Erreur');
    }
}

// ❌ Éviter
function search(q) {
    // Code sans gestion d'erreurs
}
```

#### Backend (Python)
```python
# ✅ Bon
@app.post("/api/images/search")
async def search_images(request: Dict[Any, Any]):
    """Documentation de l'endpoint"""
    try:
        query = request.get("query", "")
        if not query:
            raise HTTPException(status_code=400, detail="Query required")
        # Logique
        return {"success": True, "data": result}
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

### CSS/Styles
- Utiliser **Tailwind CSS** pour la cohérence
- Classes utilitaires plutôt que CSS personnalisé
- Responsive design obligatoire

### Conventions de Nommage
- **Variables JavaScript :** `camelCase`
- **Fonctions :** `verbeAction()` ex: `searchImages()`
- **Classes CSS :** `kebab-case`
- **Fichiers :** `snake_case.py` ou `camelCase.js`

## 🧪 Tests

### Tests Fonctionnels Obligatoires
Avant toute PR, vérifiez que ces tests passent :

1. **ChatGPT et Images**
   ```bash
   # Ouvrir http://localhost:3000
   # Cliquer sur robot, taper "/image restaurant"
   # Vérifier 4 images s'affichent
   ```

2. **Mode Édition**
   ```bash
   # Activer mode édition
   # Cliquer sur un élément
   # Vérifier barre d'outils apparaît
   ```

3. **API Backend**
   ```bash
   curl http://localhost:8001/api/health
   # Doit retourner: {"status":"healthy"}
   ```

4. **Console Propre**
   - F12 → Console
   - Vérifier aucune erreur rouge

### Tests de Régression
- Toutes les fonctionnalités existantes doivent continuer à fonctionner
- Pas d'erreurs JavaScript introduites
- Performance maintenue

## 📝 Format des Commits

```
<type>(<portée>): <description>

<corps explicatif>

<footer>
```

### Types
- `feat`: Nouvelle fonctionnalité
- `fix`: Correction de bug
- `docs`: Documentation
- `style`: Formatage, CSS
- `refactor`: Refactoring de code
- `test`: Ajout de tests
- `chore`: Maintenance

### Exemples
```bash
feat(chatgpt): ajouter recherche vidéos YouTube

- Nouvelle commande /video [query]
- Intégration API YouTube
- Interface de sélection vidéos

Closes #123
```

```bash
fix(editor): corriger sauvegarde des modifications

- Problème de persistence des changements
- Event listeners dupliqués résolus
- Amélioration gestion erreurs

Fixes #456
```

## 🔄 Processus de Pull Request

### 1. Préparation
- [ ] Branch à jour avec `main`
- [ ] Tests fonctionnels passent
- [ ] Console sans erreurs
- [ ] Documentation mise à jour si nécessaire

### 2. Création de la PR
- **Titre clair** décrivant le changement
- **Description détaillée** avec :
  - Problème résolu
  - Solution implémentée  
  - Tests effectués
  - Captures d'écran si UI

### 3. Template de PR
```markdown
## 📋 Description
Brief description du changement.

## 🔧 Type de changement
- [ ] Bug fix (non-breaking change)
- [ ] New feature (non-breaking change)
- [ ] Breaking change
- [ ] Documentation update

## 🧪 Tests Effectués
- [ ] ChatGPT et recherche d'images
- [ ] Mode édition complet
- [ ] API backend health check
- [ ] Interface responsive
- [ ] Console sans erreurs

## 📱 Captures d'écran
Si applicable, ajoutez des captures.

## ✅ Checklist
- [ ] Code testé localement
- [ ] Documentation mise à jour
- [ ] Pas d'erreurs console
- [ ] Compatible mobile/desktop
```

## 🎯 Priorités de Contribution

### 🔥 Haute Priorité
- Corrections de bugs critiques
- Amélioration performance
- Sécurité

### 📈 Moyenne Priorité  
- Nouvelles fonctionnalités ChatGPT
- Amélioration UX/UI
- Tests automatisés

### 🌟 Basse Priorité
- Optimisations mineures
- Documentation
- Refactoring

## 💬 Communication

- **Issues** : Discussion des bugs et features
- **Discussions** : Questions générales
- **Wiki** : Documentation technique détaillée

## 🏆 Reconnaissance

Tous les contributeurs sont listés dans le README et les releases notes.

**Merci de contribuer à IA WebGen Pro ! 🚀**