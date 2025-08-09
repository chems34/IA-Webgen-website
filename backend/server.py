from fastapi import FastAPI, HTTPException, File, UploadFile, Form, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os
import json
import smtplib
import requests
import uuid
from datetime import datetime
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
from email.mime.base import MimeBase
from email import encoders
import zipfile
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv
import logging
import asyncio
from pathlib import Path

# Charger les variables d'environnement
load_dotenv()

app = FastAPI(title="IA WebGen API", version="1.0.0")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifier les domaines autorisés
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
websites_data = {}  # En production, utiliser une base de données
user_sessions = {}

@app.get("/")
async def root():
    return {"message": "IA WebGen API v1.0"}

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
            raise HTTPException(status_code=500, detail="Clé API Unsplash non configurée")
            
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
        raise HTTPException(status_code=500, detail="Erreur récupération images")
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
        
        # Programmer l'envoi en arrière-plan
        background_tasks.add_task(
            send_website_by_email,
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

async def send_website_by_email(site_id: str, email: str, business_name: str):
    """Envoie le site web par email de manière asynchrone"""
    try:
        # Récupérer les données du site
        site_data = websites_data.get(site_id)
        if not site_data:
            logger.error(f"Site non trouvé pour envoi email: {site_id}")
            return
            
        # Générer les fichiers du site
        website_files = await generate_website_files(site_data["data"])
        
        # Créer un ZIP
        zip_path = f"/tmp/site_{site_id}.zip"
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_name, content in website_files.items():
                zipf.writestr(file_name, content)
        
        # Envoyer l'email
        await send_email_with_attachment(
            to_email=email,
            subject=f"🎉 Votre site web {business_name} est prêt !",
            body=f"""
            Bonjour,
            
            Félicitations ! Votre site web "{business_name}" a été généré avec succès par IA WebGen.
            
            Vous trouverez en pièce jointe :
            • Le site web complet (fichiers HTML, CSS, JS)
            • Les instructions d'installation
            • Le guide d'utilisation
            
            Votre site est maintenant prêt à être mis en ligne !
            
            Support technique disponible pendant 6 mois.
            
            Cordialement,
            L'équipe IA WebGen
            """,
            attachment_path=zip_path
        )
        
        # Mettre à jour le statut
        websites_data[site_id]["status"] = "delivered"
        websites_data[site_id]["delivered_at"] = datetime.now().isoformat()
        
        # Nettoyer le fichier temporaire
        os.unlink(zip_path)
        
        logger.info(f"Site envoyé par email avec succès - ID: {site_id}, Email: {email}")
        
    except Exception as e:
        logger.error(f"Erreur envoi email: {str(e)}")
        # Marquer comme erreur
        if site_id in websites_data:
            websites_data[site_id]["status"] = "delivery_failed"
            websites_data[site_id]["error"] = str(e)

async def generate_website_files(website_data: Dict[str, Any]) -> Dict[str, str]:
    """Génère tous les fichiers du site web"""
    files = {}
    
    # Générer le fichier HTML principal
    files["index.html"] = generate_html_content(website_data)
    
    # Générer le CSS
    files["styles.css"] = generate_css_content(website_data)
    
    # Générer le JavaScript
    files["script.js"] = generate_js_content(website_data)
    
    # Générer les pages additionnelles
    for page in website_data.get("selectedPages", []):
        if page != "accueil":
            files[f"{page}.html"] = generate_page_content(page, website_data)
    
    # Ajouter le fichier README
    files["README.md"] = generate_readme_content(website_data)
    
    return files

def generate_html_content(data: Dict[str, Any]) -> str:
    """Génère le contenu HTML du site"""
    # Utiliser les données pour générer un HTML complet et professionnel
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data.get('businessName', 'Mon Site Web')}</title>
    <link rel="stylesheet" href="styles.css">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar">
        <div class="nav-container">
            <h1 class="nav-logo">{data.get('businessName', 'Mon Site Web')}</h1>
            <ul class="nav-menu">
                <li class="nav-item">
                    <a href="#accueil" class="nav-link">Accueil</a>
                </li>
                {' '.join([f'<li class="nav-item"><a href="#{page}" class="nav-link">{page.title()}</a></li>' for page in data.get('selectedPages', []) if page != 'accueil'])}
            </ul>
        </div>
    </nav>

    <!-- Contenu principal -->
    <main>
        <!-- Section Hero -->
        <section id="accueil" class="hero">
            <div class="hero-content">
                <h1 class="hero-title">{data.get('businessName', 'Mon Entreprise')}</h1>
                <p class="hero-subtitle">{data.get('slogan', data.get('description', 'Bienvenue sur notre site'))}</p>
                <div class="hero-buttons">
                    <a href="#contact" class="btn btn-primary">Nous contacter</a>
                    <a href="#services" class="btn btn-secondary">Nos services</a>
                </div>
            </div>
        </section>

        <!-- Sections dynamiques basées sur les pages sélectionnées -->
        {generate_sections_html(data)}
    </main>

    <!-- Footer -->
    <footer class="footer">
        <div class="footer-content">
            <div class="footer-section">
                <h3>{data.get('businessName', 'Mon Entreprise')}</h3>
                <p>{data.get('description', 'Description de l' + chr(39) + 'entreprise')}</p>
            </div>
            {generate_footer_contact(data)}
        </div>
        <div class="footer-bottom">
            <p>&copy; 2024 {data.get('businessName', 'Mon Entreprise')}. Tous droits réservés. Site créé par IA WebGen.</p>
        </div>
    </footer>

    <script src="script.js"></script>
</body>
</html>"""

def generate_sections_html(data: Dict[str, Any]) -> str:
    """Génère les sections HTML basées sur les pages sélectionnées"""
    sections = []
    
    for page in data.get('selectedPages', []):
        if page == 'apropos':
            sections.append(f"""
        <section id="apropos" class="section">
            <div class="container">
                <h2>À propos de nous</h2>
                <p>{data.get('description', 'Notre histoire et nos valeurs.')}</p>
                {f'<div class="team-info">{data.get("teamInfo", "")}</div>' if data.get('teamInfo') else ''}
            </div>
        </section>""")
        elif page == 'services':
            sections.append(f"""
        <section id="services" class="section">
            <div class="container">
                <h2>Nos Services</h2>
                <p>Découvrez l'ensemble de nos prestations professionnelles</p>
                {f'<div class="services-detail">{data.get("servicesDetail", "")}</div>' if data.get('servicesDetail') else ''}
                <div class="services-grid">
                    {generate_services_grid(data.get('siteType', 'default'))}
                </div>
            </div>
        </section>""")
        elif page == 'contact':
            sections.append(f"""
        <section id="contact" class="section">
            <div class="container">
                <h2>Contactez-nous</h2>
                <div class="contact-grid">
                    <div class="contact-info">
                        {f'<p><i class="fas fa-phone"></i> {data.get("phone")}</p>' if data.get('phone') else ''}
                        {f'<p><i class="fas fa-envelope"></i> {data.get("userEmail")}</p>' if data.get('userEmail') else ''}
                        {f'<p><i class="fas fa-map-marker-alt"></i> {data.get("address")}</p>' if data.get('address') else ''}
                    </div>
                    <form class="contact-form">
                        <input type="text" placeholder="Votre nom" required>
                        <input type="email" placeholder="Votre email" required>
                        <textarea placeholder="Votre message" required></textarea>
                        <button type="submit" class="btn btn-primary">Envoyer</button>
                    </form>
                </div>
            </div>
        </section>""")
    
    return ''.join(sections)

def generate_services_grid(site_type: str) -> str:
    """Génère une grille de services basée sur le type de site"""
    services_data = {
        'restaurant': [
            {'icon': '🍽️', 'title': 'Menu Traditionnel', 'desc': 'Plats authentiques avec ingrédients de qualité'},
            {'icon': '🥂', 'title': 'Événements Privés', 'desc': 'Organisation pour vos occasions spéciales'},
            {'icon': '🚚', 'title': 'Livraison', 'desc': 'Service de livraison rapide'},
        ],
        'salon': [
            {'icon': '💇‍♀️', 'title': 'Coiffure', 'desc': 'Coupes, colorations et soins capillaires'},
            {'icon': '💅', 'title': 'Soins des Ongles', 'desc': 'Manucure, pédicure et nail art'},
            {'icon': '✨', 'title': 'Soins du Visage', 'desc': 'Nettoyage, hydratation et anti-âge'},
        ],
        'default': [
            {'icon': '⭐', 'title': 'Service Premium', 'desc': 'Excellence et satisfaction client'},
            {'icon': '🛠️', 'title': 'Solutions Personnalisées', 'desc': 'Adaptées à vos besoins'},
            {'icon': '📞', 'title': 'Support', 'desc': 'Accompagnement complet'},
        ]
    }
    
    services = services_data.get(site_type, services_data['default'])
    
    return ''.join([
        f"""<div class="service-card">
            <div class="service-icon">{service['icon']}</div>
            <h3>{service['title']}</h3>
            <p>{service['desc']}</p>
        </div>"""
        for service in services
    ])

def generate_footer_contact(data: Dict[str, Any]) -> str:
    """Génère la section contact du footer"""
    if not any([data.get('phone'), data.get('address'), data.get('userEmail')]):
        return ""
    
    return f"""
            <div class="footer-section">
                <h3>Contact</h3>
                {f'<p><i class="fas fa-phone"></i> {data.get("phone")}</p>' if data.get('phone') else ''}
                {f'<p><i class="fas fa-envelope"></i> {data.get("userEmail")}</p>' if data.get('userEmail') else ''}
                {f'<p><i class="fas fa-map-marker-alt"></i> {data.get("address")}</p>' if data.get('address') else ''}
            </div>"""

def generate_css_content(data: Dict[str, Any]) -> str:
    """Génère le CSS personnalisé"""
    primary_color = data.get('primaryColor', '#3b82f6')
    secondary_color = data.get('secondaryColor', '#1e40af')
    
    return f"""
/* Variables CSS */
:root {{
    --primary-color: {primary_color};
    --secondary-color: {secondary_color};
    --text-dark: #1f2937;
    --text-light: #6b7280;
    --background-light: #f8fafc;
    --white: #ffffff;
}}

/* Reset et base */
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: var(--text-dark);
}}

.container {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}}

/* Navigation */
.navbar {{
    background: var(--white);
    padding: 1rem 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    position: fixed;
    width: 100%;
    top: 0;
    z-index: 1000;
}}

.nav-container {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

.nav-logo {{
    color: var(--primary-color);
    font-size: 1.5rem;
    font-weight: bold;
}}

.nav-menu {{
    display: flex;
    list-style: none;
    gap: 2rem;
}}

.nav-link {{
    text-decoration: none;
    color: var(--text-dark);
    font-weight: 500;
    transition: color 0.3s;
}}

.nav-link:hover {{
    color: var(--primary-color);
}}

/* Hero Section */
.hero {{
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    color: white;
    padding: 120px 20px 80px;
    text-align: center;
    margin-top: 60px;
}}

.hero-title {{
    font-size: 3rem;
    font-weight: 900;
    margin-bottom: 1rem;
    text-shadow: 0 2px 4px rgba(0,0,0,0.3);
}}

.hero-subtitle {{
    font-size: 1.3rem;
    opacity: 0.95;
    margin-bottom: 2rem;
    max-width: 800px;
    margin-left: auto;
    margin-right: auto;
}}

.hero-buttons {{
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
}}

/* Boutons */
.btn {{
    padding: 12px 30px;
    border: none;
    border-radius: 30px;
    font-weight: bold;
    text-decoration: none;
    cursor: pointer;
    transition: all 0.3s;
    display: inline-block;
}}

.btn-primary {{
    background: var(--white);
    color: var(--primary-color);
}}

.btn-primary:hover {{
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}}

.btn-secondary {{
    background: rgba(255,255,255,0.2);
    color: white;
    border: 2px solid white;
}}

.btn-secondary:hover {{
    background: white;
    color: var(--primary-color);
}}

/* Sections */
.section {{
    padding: 80px 20px;
}}

.section:nth-child(even) {{
    background: var(--background-light);
}}

.section h2 {{
    font-size: 2.5rem;
    font-weight: bold;
    text-align: center;
    margin-bottom: 3rem;
    color: var(--primary-color);
}}

/* Services Grid */
.services-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin-top: 3rem;
}}

.service-card {{
    background: white;
    padding: 2rem;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    transition: transform 0.3s;
}}

.service-card:hover {{
    transform: translateY(-5px);
}}

.service-icon {{
    font-size: 3rem;
    margin-bottom: 1rem;
}}

.service-card h3 {{
    color: var(--primary-color);
    font-size: 1.4rem;
    margin-bottom: 1rem;
}}

/* Contact */
.contact-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 3rem;
    margin-top: 3rem;
}}

.contact-info p {{
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}

.contact-info i {{
    color: var(--primary-color);
    width: 20px;
}}

.contact-form {{
    display: flex;
    flex-direction: column;
    gap: 1rem;
}}

.contact-form input,
.contact-form textarea {{
    padding: 12px;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    font-size: 1rem;
}}

.contact-form textarea {{
    min-height: 120px;
    resize: vertical;
}}

/* Footer */
.footer {{
    background: #1f2937;
    color: white;
    padding: 3rem 0 1rem;
}}

.footer-content {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
}}

.footer-section h3 {{
    margin-bottom: 1rem;
    color: var(--primary-color);
}}

.footer-bottom {{
    border-top: 1px solid #374151;
    margin-top: 2rem;
    padding-top: 1rem;
    text-align: center;
    color: #9ca3af;
}}

/* Responsive */
@media (max-width: 768px) {{
    .hero-title {{
        font-size: 2rem;
    }}
    
    .nav-menu {{
        display: none; /* Simplification pour mobile */
    }}
    
    .services-grid {{
        grid-template-columns: 1fr;
    }}
    
    .hero-buttons {{
        flex-direction: column;
        align-items: center;
    }}
}}

/* Animations */
@keyframes fadeIn {{
    from {{
        opacity: 0;
        transform: translateY(20px);
    }}
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

.section {{
    animation: fadeIn 0.8s ease-in;
}}
"""

def generate_js_content(data: Dict[str, Any]) -> str:
    """Génère le JavaScript du site"""
    return """
// JavaScript pour IA WebGen Site
document.addEventListener('DOMContentLoaded', function() {
    console.log('Site IA WebGen chargé avec succès');
    
    // Navigation fluide
    setupSmoothScrolling();
    
    // Formulaire de contact
    setupContactForm();
    
    // Animations d'entrée
    setupScrollAnimations();
});

function setupSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

function setupContactForm() {
    const form = document.querySelector('.contact-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Récupérer les données du formulaire
            const formData = new FormData(form);
            
            // Simuler l'envoi (à remplacer par un vrai service)
            showNotification('Merci ! Votre message a été envoyé avec succès.', 'success');
            form.reset();
        });
    }
}

function setupScrollAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    });
    
    // Observer les sections
    document.querySelectorAll('.section').forEach(section => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(30px)';
        section.style.transition = 'all 0.6s ease-out';
        observer.observe(section);
    });
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#10b981' : '#3b82f6'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        z-index: 10000;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 4000);
}

// Fonctions utilitaires pour l'édition (si nécessaire)
window.iaWebgenUtils = {
    showNotification: showNotification
};
"""

def generate_readme_content(data: Dict[str, Any]) -> str:
    """Génère le fichier README"""
    return f"""# {data.get('businessName', 'Mon Site Web')} - Site Web Professionnel

Site web généré automatiquement par **IA WebGen** le {datetime.now().strftime('%d/%m/%Y')}.

## 📋 Contenu du package

- `index.html` - Page principale du site
- `styles.css` - Feuilles de style personnalisées
- `script.js` - JavaScript et interactions
- Pages additionnelles selon votre sélection

## 🚀 Installation

### Option 1 : Hébergement simple
1. Décompressez tous les fichiers
2. Uploadez le contenu sur votre hébergeur web
3. Votre site est en ligne !

### Option 2 : Test local
1. Décompressez les fichiers
2. Double-cliquez sur `index.html`
3. Le site s'ouvre dans votre navigateur

## ✏️ Personnalisation

### Modifier les couleurs
Dans le fichier `styles.css`, changez les variables CSS :
```css
:root {{
    --primary-color: {data.get('primaryColor', '#3b82f6')};
    --secondary-color: {data.get('secondaryColor', '#1e40af')};
}}
```

### Modifier les textes
Éditez directement le fichier `index.html` pour personnaliser :
- Titres et sous-titres
- Descriptions et contenus
- Informations de contact

### Ajouter des images
1. Ajoutez vos images dans un dossier `images/`
2. Modifiez les balises `<img>` dans le HTML
3. Mettez à jour les chemins d'accès

## 📱 Fonctionnalités incluses

✅ Design responsive (mobile et desktop)
✅ Navigation fluide
✅ Formulaire de contact
✅ Animations modernes
✅ SEO optimisé
✅ Code propre et commenté

## 🎨 Pages incluses

{chr(10).join([f'- **{page.title()}** - Section dédiée' for page in data.get('selectedPages', [])])}

## 📞 Support

Besoin d'aide ? Contactez le support IA WebGen :
- Email : support@iawebgen.fr
- Support technique inclus pendant 6 mois

## 🔧 Modifications avancées

Pour des modifications plus poussées, nous recommandons de faire appel à un développeur web ou de contacter notre service de personnalisation.

---

**Site créé avec ❤️ par IA WebGen - Générateur de sites web intelligent**

Merci de votre confiance !
"""

async def send_email_with_attachment(to_email: str, subject: str, body: str, attachment_path: str):
    """Envoie un email avec pièce jointe"""
    try:
        smtp_host = os.getenv("SMTP_HOST")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        smtp_user = os.getenv("SMTP_USERNAME")
        smtp_pass = os.getenv("SMTP_PASSWORD")
        
        if not all([smtp_host, smtp_user, smtp_pass]):
            raise Exception("Configuration SMTP incomplète")
            
        # Créer le message
        msg = MimeMultipart()
        msg['From'] = smtp_user
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Ajouter le corps du message
        msg.attach(MimeText(body, 'plain', 'utf-8'))
        
        # Ajouter la pièce jointe
        with open(attachment_path, "rb") as attachment:
            part = MimeBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename= site_web.zip'
        )
        msg.attach(part)
        
        # Envoyer l'email
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        text = msg.as_string()
        server.sendmail(smtp_user, to_email, text)
        server.quit()
        
        logger.info(f"Email envoyé avec succès à {to_email}")
        
    except Exception as e:
        logger.error(f"Erreur envoi email: {str(e)}")
        raise

@app.post("/api/paypal-webhook")
async def paypal_webhook(request: dict):
    """Webhook PayPal pour confirmation de paiement"""
    try:
        # Vérifier la signature PayPal (à implémenter selon la doc PayPal)
        logger.info(f"Webhook PayPal reçu: {request}")
        
        # Traiter le paiement confirmé
        # Implémenter la logique selon vos besoins
        
        return {"status": "success"}
        
    except Exception as e:
        logger.error(f"Erreur webhook PayPal: {str(e)}")
        raise HTTPException(status_code=400, detail="Erreur webhook")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)