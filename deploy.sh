#!/bin/bash

echo "🚀 Déploiement IA WebGen Pro"
echo "================================"

# Vérification des prérequis
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé"
    exit 1
fi

if ! command -v pip &> /dev/null; then
    echo "❌ pip n'est pas installé"
    exit 1
fi

echo "✅ Prérequis vérifiés"

# Installation des dépendances backend
echo "📦 Installation des dépendances backend..."
cd backend
pip install -r requirements.txt
cd ..

echo "✅ Dépendances installées"

# Créer les scripts de lancement
cat > start_backend.sh << 'EOF'
#!/bin/bash
echo "🔧 Démarrage du Backend API sur port 8001..."
cd backend
python -m uvicorn server:app --host 0.0.0.0 --port 8001 --reload
EOF

cat > start_frontend.sh << 'EOF'
#!/bin/bash
echo "🌐 Démarrage du Frontend sur port 3000..."
python -m http.server 3000
EOF

cat > start_all.sh << 'EOF'
#!/bin/bash
echo "🚀 Démarrage complet IA WebGen Pro..."
echo "Backend: http://localhost:8001"
echo "Frontend: http://localhost:3000"
echo "================================"

# Démarrer backend en arrière-plan
cd backend && python -m uvicorn server:app --host 0.0.0.0 --port 8001 --reload &
BACKEND_PID=$!

# Attendre 3 secondes
sleep 3

# Démarrer frontend
cd .. && python -m http.server 3000 &
FRONTEND_PID=$!

echo "✅ Services démarrés"
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "Pour arrêter : Ctrl+C puis 'kill $BACKEND_PID $FRONTEND_PID'"

# Attendre les processus
wait
EOF

# Rendre les scripts exécutables
chmod +x start_backend.sh
chmod +x start_frontend.sh  
chmod +x start_all.sh

echo "✅ Scripts de lancement créés"
echo ""
echo "🎉 Déploiement terminé !"
echo ""
echo "Pour démarrer :"
echo "  ./start_all.sh    # Démarrer tout"
echo "  ./start_backend.sh # Backend seulement" 
echo "  ./start_frontend.sh # Frontend seulement"
echo ""
echo "Accès :"
echo "  Frontend: http://localhost:3000"
echo "  Backend:  http://localhost:8001"
echo "  API Docs: http://localhost:8001/docs"