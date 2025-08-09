#!/usr/bin/env python3
"""
Backend API pour IA WebGen Pro
Gère les recherches d'images et autres APIs sécurisées
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import httpx
import os
from typing import List, Dict, Any
import json

app = FastAPI(title="IA WebGen Pro API")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir les fichiers statiques
app.mount("/static", StaticFiles(directory="../"), name="static")

@app.get("/")
async def serve_index():
    """Servir l'index.html"""
    return FileResponse("../index.html")

@app.get("/api/health")
async def health_check():
    """Vérification de santé de l'API"""
    return {"status": "healthy", "message": "IA WebGen Pro API is running"}

@app.post("/api/images/search")
async def search_images(request: Dict[Any, Any]):
    """
    Recherche d'images via API Unsplash
    """
    try:
        query = request.get("query", "")
        if not query:
            raise HTTPException(status_code=400, detail="Query is required")
        
        # URLs d'images de démonstration - dans un vrai projet, utiliser l'API Unsplash
        demo_images = [
            {
                "id": f"demo_{i}",
                "url": f"https://images.unsplash.com/photo-{1571197857330 + i * 1000}?w=400&h=300&fit=crop&q=80",
                "small_url": f"https://images.unsplash.com/photo-{1571197857330 + i * 1000}?w=200&h=150&fit=crop&q=80",
                "description": f"{query} image {i + 1}",
                "alt_description": f"Image de {query}"
            }
            for i in range(6)
        ]
        
        # Images spécifiques selon la requête
        if "restaurant" in query.lower():
            demo_images = [
                {
                    "id": "rest_1",
                    "url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=400&h=300&fit=crop&q=80",
                    "small_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=200&h=150&fit=crop&q=80",
                    "description": "Restaurant moderne élégant",
                    "alt_description": "Restaurant moderne"
                },
                {
                    "id": "rest_2", 
                    "url": "https://images.unsplash.com/photo-1571197857330-8894d3da2c3b?w=400&h=300&fit=crop&q=80",
                    "small_url": "https://images.unsplash.com/photo-1571197857330-8894d3da2c3b?w=200&h=150&fit=crop&q=80",
                    "description": "Plats gastronomiques",
                    "alt_description": "Cuisine gastronomique"
                },
                {
                    "id": "rest_3",
                    "url": "https://images.unsplash.com/photo-1559329007-40df8d946775?w=400&h=300&fit=crop&q=80",
                    "small_url": "https://images.unsplash.com/photo-1559329007-40df8d946775?w=200&h=150&fit=crop&q=80",
                    "description": "Ambiance restaurant chaleureuse",
                    "alt_description": "Ambiance restaurant"
                },
                {
                    "id": "rest_4",
                    "url": "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=400&h=300&fit=crop&q=80",
                    "small_url": "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=200&h=150&fit=crop&q=80",
                    "description": "Chef en cuisine",
                    "alt_description": "Chef cuisinier"
                }
            ]
        
        return {
            "success": True,
            "query": query,
            "images": demo_images,
            "total": len(demo_images)
        }
        
    except Exception as e:
        print(f"Erreur recherche d'images: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
async def chat_response(request: Dict[Any, Any]):
    """
    Réponses du ChatGPT
    """
    try:
        message = request.get("message", "").lower()
        
        # Réponses contextuelles
        if "aide" in message or "help" in message:
            response = {
                "message": """Je peux t'aider avec :
• <b>/image [description]</b> - Chercher des images
• Questions sur l'édition du site
• Suggestions d'amélioration
• Conseils de design

Que veux-tu faire ?""",
                "type": "help"
            }
        elif message.startswith("/image"):
            query = message.replace("/image", "").strip()
            response = {
                "message": f"🔍 Recherche d'images pour: \"{query}\"...",
                "type": "image_search",
                "query": query
            }
        elif "édition" in message or "modifier" in message:
            response = {
                "message": """Pour modifier ton site :
1. Active le <b>Mode Édition</b> dans le panneau de droite
2. Clique sur n'importe quel élément pour le modifier
3. Utilise les boutons d'édition qui apparaissent
4. Tu peux changer les textes, couleurs, styles

Veux-tu que j'active le mode édition pour toi ?""",
                "type": "edit_help"
            }
        else:
            responses = [
                "C'est une excellente question ! Peux-tu me donner plus de détails ?",
                "Je vois que tu travailles sur ton site. Comment puis-je t'aider à l'améliorer ?",
                "Bonne idée ! Pour cela, je recommande d'utiliser le mode édition.",
                "Intéressant ! N'hésite pas à expérimenter avec les couleurs et les styles.",
                "Super ! Si tu veux ajouter du contenu visuel, utilise la commande <b>/image [description]</b>."
            ]
            import random
            response = {
                "message": random.choice(responses),
                "type": "general"
            }
        
        return response
        
    except Exception as e:
        print(f"Erreur chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)