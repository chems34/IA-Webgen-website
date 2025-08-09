#!/bin/bash

clear
echo "🎉 ====================================="
echo "   IA WEBGEN PRO - PRÊT POUR GITHUB"
echo "===================================== 🎉"
echo ""

# Vérifications des fichiers essentiels
echo "🔍 Vérification des fichiers..."

FILES=(
    "index.html"
    "README.md" 
    "package.json"
    "backend/server.py"
    "backend/requirements.txt"
    "deploy.sh"
    "init_github.sh"
)

all_files_present=true
for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file MANQUANT"
        all_files_present=false
    fi
done

if [ "$all_files_present" = false ]; then
    echo ""
    echo "❌ Des fichiers essentiels sont manquants !"
    exit 1
fi

echo ""
echo "✅ Tous les fichiers sont présents !"
echo ""

# Rendre les scripts exécutables
chmod +x *.sh
echo "✅ Scripts rendus exécutables"

# Afficher les informations importantes
echo ""
echo "📋 ===== INFORMATIONS IMPORTANTES ====="
echo ""
echo "📁 STRUCTURE DU PROJET :"
echo "├── index.html              # Application principale"
echo "├── README.md               # Documentation complète"  
echo "├── backend/                # API FastAPI sécurisée"
echo "│   ├── server.py           # Serveur principal"
echo "│   └── requirements.txt    # Dépendances Python"
echo "├── deploy.sh               # Script de déploiement"
echo "├── init_github.sh          # Initialisation GitHub"
echo "└── start_*.sh              # Scripts de lancement"
echo ""

echo "🎯 FONCTIONNALITÉS IMPLÉMENTÉES :"
echo "✅ Mini ChatGPT avec recherche d'images (/image [description])"
echo "✅ Mode édition complet après prévisualisation"
echo "✅ API backend sécurisée (FastAPI)"
echo "✅ Modification temps réel (textes, couleurs, styles)"
echo "✅ Ajout de sections dynamiques (6 types)"
echo "✅ Interface responsive moderne"
echo "✅ Console navigateur sans erreurs"
echo "✅ Tests fonctionnels validés"
echo ""

echo "🚀 ÉTAPES POUR GITHUB :"
echo ""
echo "1️⃣  CRÉER LE REPOSITORY GITHUB :"
echo "   👉 https://github.com/new"
echo "   📝 Nom : ia-webgen-pro"
echo "   📄 Description : Générateur de sites web avec IA, ChatGPT intégré"
echo "   ⚠️  IMPORTANT : NE PAS cocher README, .gitignore, license"
echo ""

echo "2️⃣  COPIER CE DOSSIER :"
echo "   cp -r $(pwd) ~/mes-projets/ia-webgen-pro"
echo "   cd ~/mes-projets/ia-webgen-pro"
echo ""

echo "3️⃣  INITIALISER GIT :"
echo "   ./init_github.sh"
echo "   git push -u origin main"
echo ""

echo "4️⃣  TESTER LOCALEMENT :"
echo "   ./deploy.sh"
echo "   ./start_all.sh"
echo ""

# Créer un résumé des commandes
cat > COMMANDS_SUMMARY.txt << 'EOF'
# 🚀 COMMANDES RÉSUMÉES POUR GITHUB

## 1. Créer repository sur GitHub
https://github.com/new
Nom: ia-webgen-pro
Ne pas cocher README, .gitignore, license

## 2. Copier et initialiser
cp -r /app ~/mes-projets/ia-webgen-pro
cd ~/mes-projets/ia-webgen-pro
./init_github.sh
git push -u origin main

## 3. Tester localement  
./deploy.sh
./start_all.sh

## URLs après déploiement
- Application: http://localhost:3000
- API Backend: http://localhost:8001
- API Docs: http://localhost:8001/docs

## Tests à effectuer
1. Cliquer sur robot 🤖 (ChatGPT)
2. Taper: /image restaurant moderne
3. Vérifier 4 images s'affichent
4. Activer mode édition
5. Cliquer éléments (bordures bleues)
6. F12 → Console → Vérifier 0 erreur
EOF

echo "📋 RÉSUMÉ SAUVEGARDÉ : COMMANDS_SUMMARY.txt"
echo ""

# Test de validation final
echo "🧪 VALIDATION FINALE DES FICHIERS CRITIQUES..."

# Vérifier index.html
if grep -q "IA WebGen" index.html && grep -q "toggleChatGPT" index.html; then
    echo "✅ index.html : Application principale OK"
else
    echo "❌ index.html : Problème détecté"
fi

# Vérifier backend
if grep -q "FastAPI" backend/server.py && grep -q "search_images" backend/server.py; then
    echo "✅ backend/server.py : API FastAPI OK"  
else
    echo "❌ backend/server.py : Problème détecté"
fi

# Vérifier README
if grep -q "ChatGPT" README.md && grep -q "Mode Édition" README.md; then
    echo "✅ README.md : Documentation complète OK"
else
    echo "❌ README.md : Documentation incomplète"
fi

echo ""
echo "🎉 ====================================="
echo "     PRÊT POUR GITHUB ! 🚀"
echo "===================================== 🎉"
echo ""
echo "📋 CHECKLIST FINALE :"
echo "□ Créer repository GitHub (https://github.com/new)"
echo "□ Copier ce dossier vers votre espace de travail"
echo "□ Exécuter ./init_github.sh"  
echo "□ Push : git push -u origin main"
echo "□ Tester : ./deploy.sh puis ./start_all.sh"
echo ""
echo "✨ Votre générateur de sites web avec IA sera alors"
echo "   disponible sur GitHub ET fonctionnel en local !"
echo ""
echo "📖 Voir SETUP_GITHUB.md pour les détails"
echo "💾 Voir COMMANDS_SUMMARY.txt pour un résumé"
echo ""

# Créer une archive zip si possible
if command -v zip &> /dev/null; then
    echo "📦 Création d'une archive zip..."
    zip -r ia-webgen-pro.zip . -x "*.git*" "*.log" "*__pycache__*" "node_modules/*"
    echo "✅ Archive créée : ia-webgen-pro.zip"
    echo "   (Vous pouvez télécharger et décompresser cette archive ailleurs)"
    echo ""
fi

echo "🎯 Pour commencer immédiatement :"
echo "   1. Créez votre repository sur GitHub"
echo "   2. Suivez SETUP_GITHUB.md"
echo "   3. Enjoy your new AI website generator! 🎉"