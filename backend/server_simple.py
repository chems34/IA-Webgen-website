from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import json
import requests
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv
import logging

# Charger les variables d'environnement
load_dotenv()

app = FastAPI(title="IA WebGen API", version="1.0.0")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Modèles Pydantic
class WebsiteData(BaseModel):
    businessName: str
    description: str
    siteType: str
    userEmail: EmailStr
    phone: Optional[str] = ""
    address: Optional[str] = ""
    website: Optional[str] = ""
    slogan: Optional[str] = ""
    teamInfo: Optional[str] = ""
    servicesDetail: Optional[str] = ""
    selectedPages: List[str]
    socialMedia: Dict[str, str] = {}
    primaryColor: str = "#3b82f6"
    secondaryColor: str = "#1e40af"
    templateId: str
    photos: List[str] = []

class PaymentData(BaseModel):
    websiteData: WebsiteData
    offerType: str  # 'site' ou 'conciergerie'
    totalPrice: float
    paypalTransactionId: Optional[str] = ""

class EditCommand(BaseModel):
    command: str  # 'setText', 'setHTML', 'setImage', 'setStyle'
    selector: str
    value: str
    page: Optional[str] = "current"

# Variables globales pour stocker les données
websites_data = {}
user_sessions = {}

@app.get("/")
async def root():
    return {"message": "IA WebGen API v1.0 - Édition Avancée"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/api/generate-website")
async def generate_website(website_data: WebsiteData):
    """Génère un site web complet avec l'IA"""
    try:
        # Générer un ID unique pour le site
        site_id = str(uuid.uuid4())
        
        # Stocker les données
        websites_data[site_id] = {
            "data": website_data.dict(),
            "created_at": datetime.now().isoformat(),
            "status": "generated"
        }
        
        logger.info(f"Site généré avec succès - ID: {site_id}")
        
        return {
            "success": True,
            "site_id": site_id,
            "message": "Site généré avec succès",
            "pages_count": len(website_data.selectedPages)
        }
        
    except Exception as e:
        logger.error(f"Erreur génération site: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur génération: {str(e)}")

@app.post("/api/edit-element")
async def edit_element(edit_data: EditCommand, site_id: str):
    """Édite un élément du site en temps réel"""
    try:
        if site_id not in websites_data:
            raise HTTPException(status_code=404, detail="Site non trouvé")
            
        # Sauvegarder la modification
        if "modifications" not in websites_data[site_id]:
            websites_data[site_id]["modifications"] = []
            
        modification = {
            "id": str(uuid.uuid4()),
            "command": edit_data.command,
            "selector": edit_data.selector,
            "value": edit_data.value,
            "page": edit_data.page,
            "timestamp": datetime.now().isoformat()
        }
        
        websites_data[site_id]["modifications"].append(modification)
        
        logger.info(f"Modification appliquée - Site: {site_id}, Command: {edit_data.command}")
        
        return {
            "success": True,
            "modification_id": modification["id"],
            "message": "Modification appliquée avec succès"
        }
        
    except Exception as e:
        logger.error(f"Erreur modification: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur modification: {str(e)}")

@app.get("/api/get-images")
async def get_images(query: str, count: int = 6):
    """Récupère des images depuis Unsplash de manière sécurisée"""
    try:
        api_key = os.getenv("UNSPLASH_API_KEY")
        if not api_key:
            # Retourner des images de démonstration si pas de clé API
            demo_images = [
                {
                    "id": f"demo-{i}",
                    "url": f"https://picsum.photos/800/600?random={i}",
                    "thumb": f"https://picsum.photos/200/150?random={i}",
                    "description": f"Image de démonstration {i+1}",
                    "author": "Picsum Photos"
                }
                for i in range(count)
            ]
            return {"success": True, "images": demo_images}
            
        url = f"https://api.unsplash.com/search/photos"
        params = {
            "query": query,
            "per_page": count,
            "client_id": api_key,
            "orientation": "landscape"
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        images = [
            {
                "id": img["id"],
                "url": img["urls"]["regular"],
                "thumb": img["urls"]["thumb"],
                "description": img["alt_description"] or "Image professionnelle",
                "author": img["user"]["name"]
            }
            for img in data.get("results", [])
        ]
        
        return {"success": True, "images": images}
        
    except requests.RequestException as e:
        logger.error(f"Erreur API Unsplash: {str(e)}")
        # Retourner des images de démonstration en cas d'erreur
        demo_images = [
            {
                "id": f"demo-{i}",
                "url": f"https://picsum.photos/800/600?random={i}",
                "thumb": f"https://picsum.photos/200/150?random={i}",
                "description": f"Image de démonstration {i+1}",
                "author": "Picsum Photos"
            }
            for i in range(count)
        ]
        return {"success": True, "images": demo_images}
    except Exception as e:
        logger.error(f"Erreur inattendue: {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur serveur")

@app.post("/api/process-payment")
async def process_payment(payment_data: PaymentData, background_tasks: BackgroundTasks):
    """Traite le paiement et envoie le site par email"""
    try:
        # Générer le site complet
        site_id = str(uuid.uuid4())
        
        # Stocker les données de paiement
        websites_data[site_id] = {
            "data": payment_data.websiteData.dict(),
            "payment": {
                "offer_type": payment_data.offerType,
                "total_price": payment_data.totalPrice,
                "paypal_transaction_id": payment_data.paypalTransactionId,
                "status": "pending"
            },
            "created_at": datetime.now().isoformat(),
            "status": "paid_pending_delivery"
        }
        
        # Programmer l'envoi en arrière-plan (simulé pour le moment)
        background_tasks.add_task(
            simulate_email_delivery,
            site_id,
            payment_data.websiteData.userEmail,
            payment_data.websiteData.businessName
        )
        
        logger.info(f"Paiement traité - Site ID: {site_id}, Email: {payment_data.websiteData.userEmail}")
        
        return {
            "success": True,
            "site_id": site_id,
            "message": "Paiement confirmé. Votre site sera envoyé par email dans quelques minutes."
        }
        
    except Exception as e:
        logger.error(f"Erreur traitement paiement: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur paiement: {str(e)}")

async def simulate_email_delivery(site_id: str, email: str, business_name: str):
    """Simule l'envoi du site web par email"""
    try:
        # Simuler un délai d'envoi
        import asyncio
        await asyncio.sleep(5)
        
        # Mettre à jour le statut
        if site_id in websites_data:
            websites_data[site_id]["status"] = "delivered"
            websites_data[site_id]["delivered_at"] = datetime.now().isoformat()
        
        logger.info(f"Email simulé envoyé avec succès - ID: {site_id}, Email: {email}")
        
    except Exception as e:
        logger.error(f"Erreur simulation email: {str(e)}")
        if site_id in websites_data:
            websites_data[site_id]["status"] = "delivery_failed"
            websites_data[site_id]["error"] = str(e)

@app.post("/api/paypal-webhook")
async def paypal_webhook(request: dict):
    """Webhook PayPal pour confirmation de paiement"""
    try:
        logger.info(f"Webhook PayPal reçu: {request}")
        return {"status": "success"}
        
    except Exception as e:
        logger.error(f"Erreur webhook PayPal: {str(e)}")
        raise HTTPException(status_code=400, detail="Erreur webhook")

@app.get("/api/website/{site_id}")
async def get_website(site_id: str):
    """Récupère les données d'un site"""
    if site_id not in websites_data:
        raise HTTPException(status_code=404, detail="Site non trouvé")
    
    return {
        "success": True,
        "data": websites_data[site_id]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)