#!/bin/bash

echo "🎯 Initialisation repository GitHub pour IA WebGen Pro"
echo "====================================================="

# Vérifier si git est installé
if ! command -v git &> /dev/null; then
    echo "❌ Git n'est pas installé. Installez-le d'abord."
    exit 1
fi

# Demander les informations GitHub
echo "📝 Configuration du repository..."
read -p "Nom d'utilisateur GitHub : " github_user
read -p "Nom du repository (ia-webgen-pro) : " repo_name

# Utiliser nom par défaut si vide
if [ -z "$repo_name" ]; then
    repo_name="ia-webgen-pro"
fi

echo ""
echo "🔧 Configuration Git..."

# Initialiser git si pas déjà fait
if [ ! -d ".git" ]; then
    git init
    echo "✅ Repository Git initialisé"
fi

# Configurer les informations de base
git config user.name "$github_user"
git config user.email "$github_user@users.noreply.github.com"

# Ajouter tous les fichiers
git add .

# Premier commit
git commit -m "🎉 Initial commit - IA WebGen Pro avec ChatGPT et mode édition complet

✅ Fonctionnalités implémentées:
- Mini ChatGPT intégré avec recherche d'images
- Mode édition complet après prévisualisation  
- API backend sécurisée (FastAPI)
- Interface responsive moderne
- Toutes les fonctionnalités critiques opérationnelles

🚀 Prêt pour la production!"

# Configurer la branche main
git branch -M main

# Ajouter le remote GitHub
git remote add origin "https://github.com/$github_user/$repo_name.git"

echo ""
echo "✅ Repository configuré !"
echo ""
echo "🚀 Étapes suivantes :"
echo "1. Créez le repository sur GitHub : https://github.com/new"
echo "2. Nom du repository : $repo_name"
echo "3. Laissez-le vide (pas de README, .gitignore, etc.)"
echo "4. Après création, exécutez : git push -u origin main"
echo ""
echo "📁 Structure du projet :"
echo "├── README.md              # Documentation complète"
echo "├── index.html             # Application principale"  
echo "├── backend/               # API FastAPI"
echo "├── package.json           # Configuration npm"
echo "├── docker-compose.yml     # Configuration Docker"
echo "└── scripts de déploiement # start_all.sh, etc."
echo ""
echo "🎯 URLs après déploiement :"
echo "- Repository: https://github.com/$github_user/$repo_name"
echo "- Application: http://localhost:3000"  
echo "- API Backend: http://localhost:8001"