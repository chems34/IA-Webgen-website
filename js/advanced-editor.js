// ========== SYSTÈME D'ÉDITION AVANCÉ IA WEBGEN ==========

// Templates professionnels (conservés)
const TEMPLATES = [
    // 7 THÈMES GRATUITS
    {
        id: 'modern-clean',
        name: 'Modern Clean',
        description: 'Design épuré et moderne',
        isPremium: false,
        colors: { primary: '#3b82f6', secondary: '#1e40af' },
        gradient: 'from-blue-400 to-blue-600'
    },
    {
        id: 'business-pro',
        name: 'Business Pro',
        description: 'Professionnel et élégant',
        isPremium: false,
        colors: { primary: '#374151', secondary: '#111827' },
        gradient: 'from-gray-600 to-gray-800'
    },
    {
        id: 'creative-studio',
        name: 'Creative Studio',
        description: 'Créatif et artistique',
        isPremium: false,
        colors: { primary: '#f59e0b', secondary: '#dc2626' },
        gradient: 'from-orange-400 to-red-500'
    },
    {
        id: 'fresh-green',
        name: 'Fresh Green',
        description: 'Nature et éco-responsable',
        isPremium: false,
        colors: { primary: '#10b981', secondary: '#047857' },
        gradient: 'from-green-400 to-emerald-600'
    },
    {
        id: 'tech-innovation',
        name: 'Tech Innovation',
        description: 'High-tech et futuriste',
        isPremium: false,
        colors: { primary: '#8b5cf6', secondary: '#7c3aed' },
        gradient: 'from-purple-500 to-cyan-500'
    },
    {
        id: 'warm-elegance',
        name: 'Warm Elegance',
        description: 'Chaleureux et accueillant',
        isPremium: false,
        colors: { primary: '#f97316', secondary: '#ea580c' },
        gradient: 'from-orange-500 to-amber-600'
    },
    {
        id: 'classic-minimal',
        name: 'Classic Minimal',
        description: 'Classique et minimaliste',
        isPremium: false,
        colors: { primary: '#6b7280', secondary: '#374151' },
        gradient: 'from-slate-400 to-slate-600'
    },
    // 3 THÈMES PREMIUM (+5€)
    {
        id: 'luxury-gold',
        name: 'Luxury Gold',
        description: 'Premium avec animations dorées',
        isPremium: true,
        colors: { primary: '#f59e0b', secondary: '#d97706' },
        gradient: 'from-yellow-400 to-amber-600'
    },
    {
        id: 'royal-purple',
        name: 'Royal Purple',
        description: 'Design royal avec effets premium',
        isPremium: true,
        colors: { primary: '#a855f7', secondary: '#7c3aed' },
        gradient: 'from-purple-500 to-indigo-600'
    },
    {
        id: 'diamond-elite',
        name: 'Diamond Elite',
        description: 'Ultra-premium avec cristaux',
        isPremium: true,
        colors: { primary: '#6b7280', secondary: '#374151' },
        gradient: 'from-slate-400 to-slate-700'
    }
];

// ========== FONCTIONS D'ÉDITION AVANCÉE ==========

// Initialisation de l'éditeur
function initializeAdvancedEditor() {
    console.log('🎨 Initialisation de l\'éditeur avancé...');
    
    // Activer les éléments éditables
    enableEditableElements();
    
    // Initialiser les listeners
    setupEditorEventListeners();
    
    // Configurer l'historique
    initEditHistory();
    
    console.log('✅ Éditeur avancé initialisé avec succès');
}

// Activer/désactiver l'éditeur
function toggleEditor() {
    editorOpen = !editorOpen;
    const panel = document.getElementById('editorPanel');
    const toggle = document.getElementById('editorToggle');
    
    if (editorOpen) {
        panel.classList.add('open');
        toggle.classList.add('active');
        toggle.innerHTML = '<i class="fas fa-times"></i>';
        showNotification('🎨 Éditeur ouvert - Commencez à personnaliser !', 'info');
    } else {
        panel.classList.remove('open');
        toggle.classList.remove('active');
        toggle.innerHTML = '<i class="fas fa-edit"></i>';
        hideElementSelection();
    }
}

// Changer le mode d'édition
function changeEditMode() {
    const mode = document.getElementById('editMode').value;
    editMode = mode;
    
    // Masquer/afficher les sections appropriées
    document.getElementById('commandMode').classList.toggle('hidden', mode !== 'command');
    document.getElementById('sectionMode').classList.toggle('hidden', mode !== 'sections');
    
    if (mode === 'sections') {
        showSectionBuilder();
    } else {
        hideSectionBuilder();
    }
    
    showNotification(`Mode d'édition changé : ${mode}`, 'info');
}

// ========== FONCTIONS DE COMMANDES AVANCÉES ==========

// Exécuter une commande (Enter dans l'input)
function executeCommand(event) {
    if (event.key === 'Enter') {
        executeCommandManual();
    }
}

// Exécuter une commande manuellement
function executeCommandManual() {
    const command = document.getElementById('commandInput').value.trim();
    if (!command) return;
    
    console.log('⚡ Exécution de la commande:', command);
    
    try {
        parseAndExecuteCommand(command);
        document.getElementById('commandInput').value = '';
        showNotification('✅ Commande exécutée avec succès', 'success');
    } catch (error) {
        console.error('❌ Erreur commande:', error);
        showNotification('❌ Erreur dans la commande: ' + error.message, 'error');
    }
}

// Parser et exécuter les commandes
function parseAndExecuteCommand(command) {
    const parts = command.split(' ');
    const cmd = parts[0].toLowerCase();
    const selector = parts[1];
    const value = parts.slice(2).join(' ').replace(/['"]/g, '');
    
    if (!selector) throw new Error('Sélecteur manquant');
    if (!value && cmd !== 'getinfo') throw new Error('Valeur manquante');
    
    switch (cmd) {
        case 'settext':
            setText(selector, value);
            break;
        case 'sethtml':
            setHTML(selector, value);
            break;
        case 'setimage':
            setImage(selector, value);
            break;
        case 'setstyle':
            const property = parts[2];
            const styleValue = parts.slice(3).join(' ').replace(/['"]/g, '');
            setStyle(selector, property, styleValue);
            break;
        case 'getinfo':
            getElementInfo(selector);
            break;
        default:
            throw new Error(`Commande inconnue: ${cmd}`);
    }
    
    // Sauvegarder dans l'historique
    saveToHistory('command', { command, selector, value });
}

// ========== IMPLÉMENTATION DES COMMANDES ==========

// Fonction setText
function setText(selector, text) {
    const element = document.querySelector(selector);
    if (!element) throw new Error(`Élément non trouvé: ${selector}`);
    
    const oldText = element.textContent;
    element.textContent = text;
    
    // Mettre à jour dans le DOM d'aperçu si c'est dans la prévisualisation
    const previewElement = document.querySelector('#websitePreview ' + selector);
    if (previewElement) {
        previewElement.textContent = text;
    }
    
    // Sauvegarder la modification
    saveModification('setText', selector, text, oldText);
    
    console.log(`✅ setText: ${selector} = "${text}"`);
}

// Fonction setHTML
function setHTML(selector, html) {
    const element = document.querySelector(selector);
    if (!element) throw new Error(`Élément non trouvé: ${selector}`);
    
    const oldHTML = element.innerHTML;
    element.innerHTML = html;
    
    const previewElement = document.querySelector('#websitePreview ' + selector);
    if (previewElement) {
        previewElement.innerHTML = html;
    }
    
    saveModification('setHTML', selector, html, oldHTML);
    console.log(`✅ setHTML: ${selector} = "${html}"`);
}

// Fonction setImage
function setImage(selector, url) {
    const element = document.querySelector(selector);
    if (!element) throw new Error(`Élément non trouvé: ${selector}`);
    
    let oldValue = '';
    
    if (element.tagName === 'IMG') {
        oldValue = element.src;
        element.src = url;
    } else {
        oldValue = element.style.backgroundImage;
        element.style.backgroundImage = `url(${url})`;
        element.style.backgroundSize = 'cover';
        element.style.backgroundPosition = 'center';
    }
    
    // Mise à jour dans l'aperçu
    const previewElement = document.querySelector('#websitePreview ' + selector);
    if (previewElement) {
        if (previewElement.tagName === 'IMG') {
            previewElement.src = url;
        } else {
            previewElement.style.backgroundImage = `url(${url})`;
            previewElement.style.backgroundSize = 'cover';
            previewElement.style.backgroundPosition = 'center';
        }
    }
    
    saveModification('setImage', selector, url, oldValue);
    console.log(`✅ setImage: ${selector} = "${url}"`);
}

// Fonction setStyle
function setStyle(selector, property, value) {
    const element = document.querySelector(selector);
    if (!element) throw new Error(`Élément non trouvé: ${selector}`);
    
    const oldValue = element.style[property];
    element.style[property] = value;
    
    const previewElement = document.querySelector('#websitePreview ' + selector);
    if (previewElement) {
        previewElement.style[property] = value;
    }
    
    saveModification('setStyle', selector, `${property}:${value}`, `${property}:${oldValue}`);
    console.log(`✅ setStyle: ${selector} ${property} = "${value}"`);
}

// Obtenir des infos sur un élément
function getElementInfo(selector) {
    const element = document.querySelector(selector);
    if (!element) throw new Error(`Élément non trouvé: ${selector}`);
    
    const info = {
        tagName: element.tagName,
        className: element.className,
        id: element.id,
        textContent: element.textContent.substring(0, 100),
        styles: window.getComputedStyle(element)
    };
    
    console.log('ℹ️ Info élément:', info);
    showNotification(`Info: ${info.tagName}.${info.className}`, 'info');
    return info;
}

// ========== GESTION DE L'HISTORIQUE ==========

function initEditHistory() {
    editHistory = [];
    editHistoryIndex = -1;
}

function saveToHistory(type, data) {
    // Supprimer l'historique après l'index actuel si on est pas à la fin
    if (editHistoryIndex < editHistory.length - 1) {
        editHistory = editHistory.slice(0, editHistoryIndex + 1);
    }
    
    editHistory.push({
        type: type,
        data: data,
        timestamp: new Date().toISOString()
    });
    
    editHistoryIndex = editHistory.length - 1;
    
    // Limiter l'historique à 50 actions
    if (editHistory.length > 50) {
        editHistory.shift();
        editHistoryIndex--;
    }
}

function undoChange() {
    if (editHistoryIndex > 0) {
        editHistoryIndex--;
        const change = editHistory[editHistoryIndex];
        // Implémenter l'annulation selon le type
        showNotification('↩️ Modification annulée', 'info');
    } else {
        showNotification('❌ Aucune modification à annuler', 'warning');
    }
}

function redoChange() {
    if (editHistoryIndex < editHistory.length - 1) {
        editHistoryIndex++;
        const change = editHistory[editHistoryIndex];
        // Implémenter la restauration selon le type
        showNotification('↪️ Modification restaurée', 'info');
    } else {
        showNotification('❌ Aucune modification à refaire', 'warning');
    }
}

// ========== AJOUT DE SECTIONS DYNAMIQUES ==========

function showSectionBuilder() {
    document.getElementById('sectionBuilder').classList.remove('hidden');
    document.getElementById('sectionBuilder').scrollIntoView({ behavior: 'smooth' });
}

function hideSectionBuilder() {
    document.getElementById('sectionBuilder').classList.add('hidden');
}

function addSection(type) {
    showSectionBuilder();
}

function insertSection(type) {
    console.log(`➕ Ajout de section: ${type}`);
    
    const sectionHTML = generateSectionHTML(type);
    const insertPoint = document.getElementById('mainSection');
    
    // Créer un nouvel élément
    const newSection = document.createElement('section');
    newSection.className = 'py-16 bg-gray-50';
    newSection.innerHTML = sectionHTML;
    newSection.setAttribute('data-editable', 'section');
    newSection.setAttribute('data-section-type', type);
    
    // Insérer avant le bouton d'ajout de section
    const sectionBuilder = document.getElementById('sectionBuilder');
    insertPoint.insertBefore(newSection, sectionBuilder);
    
    // Activer l'édition sur cette section
    enableEditableElements(newSection);
    
    hideSectionBuilder();
    showNotification(`✅ Section "${type}" ajoutée avec succès`, 'success');
    
    // Sauvegarder
    saveModification('addSection', null, type, null);
}

function generateSectionHTML(type) {
    const templates = {
        hero: `
            <div class="container mx-auto px-4 text-center">
                <h2 class="text-4xl font-bold text-gray-800 mb-6 editable-element" data-editable="text">
                    Nouveau Titre Hero
                    <div class="edit-overlay">Modifier</div>
                </h2>
                <p class="text-xl text-gray-600 mb-8 editable-element" data-editable="text">
                    Description de votre nouvelle section hero
                    <div class="edit-overlay">Modifier</div>
                </p>
                <button class="bg-blue-500 text-white px-8 py-3 rounded-lg hover:bg-blue-600">
                    Bouton d'action
                </button>
            </div>
        `,
        services: `
            <div class="container mx-auto px-4">
                <h2 class="text-3xl font-bold text-center mb-12 editable-element" data-editable="text">
                    Nos Services
                    <div class="edit-overlay">Modifier</div>
                </h2>
                <div class="grid md:grid-cols-3 gap-8">
                    <div class="text-center p-6 bg-white rounded-lg shadow">
                        <div class="text-4xl mb-4">⚙️</div>
                        <h3 class="text-xl font-bold mb-3">Service 1</h3>
                        <p class="text-gray-600">Description du service 1</p>
                    </div>
                    <div class="text-center p-6 bg-white rounded-lg shadow">
                        <div class="text-4xl mb-4">🚀</div>
                        <h3 class="text-xl font-bold mb-3">Service 2</h3>
                        <p class="text-gray-600">Description du service 2</p>
                    </div>
                    <div class="text-center p-6 bg-white rounded-lg shadow">
                        <div class="text-4xl mb-4">💎</div>
                        <h3 class="text-xl font-bold mb-3">Service 3</h3>
                        <p class="text-gray-600">Description du service 3</p>
                    </div>
                </div>
            </div>
        `,
        testimonials: `
            <div class="container mx-auto px-4">
                <h2 class="text-3xl font-bold text-center mb-12 editable-element" data-editable="text">
                    Témoignages Clients
                    <div class="edit-overlay">Modifier</div>
                </h2>
                <div class="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
                    <div class="bg-white p-6 rounded-lg shadow">
                        <p class="text-gray-600 mb-4">"Excellent service, je recommande vivement !"</p>
                        <div class="flex items-center">
                            <div class="w-12 h-12 bg-blue-500 rounded-full flex items-center justify-center text-white font-bold">
                                JD
                            </div>
                            <div class="ml-4">
                                <h4 class="font-bold">Jean Dupont</h4>
                                <p class="text-sm text-gray-500">Client satisfait</p>
                            </div>
                        </div>
                    </div>
                    <div class="bg-white p-6 rounded-lg shadow">
                        <p class="text-gray-600 mb-4">"Une équipe professionnelle et à l'écoute."</p>
                        <div class="flex items-center">
                            <div class="w-12 h-12 bg-green-500 rounded-full flex items-center justify-center text-white font-bold">
                                ML
                            </div>
                            <div class="ml-4">
                                <h4 class="font-bold">Marie Legrand</h4>
                                <p class="text-sm text-gray-500">Partenaire</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `,
        gallery: `
            <div class="container mx-auto px-4">
                <h2 class="text-3xl font-bold text-center mb-12 editable-element" data-editable="text">
                    Galerie
                    <div class="edit-overlay">Modifier</div>
                </h2>
                <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div class="aspect-square bg-gray-200 rounded-lg editable-element" data-editable="image">
                        <div class="edit-overlay">Ajouter image</div>
                    </div>
                    <div class="aspect-square bg-gray-200 rounded-lg editable-element" data-editable="image">
                        <div class="edit-overlay">Ajouter image</div>
                    </div>
                    <div class="aspect-square bg-gray-200 rounded-lg editable-element" data-editable="image">
                        <div class="edit-overlay">Ajouter image</div>
                    </div>
                    <div class="aspect-square bg-gray-200 rounded-lg editable-element" data-editable="image">
                        <div class="edit-overlay">Ajouter image</div>
                    </div>
                </div>
            </div>
        `,
        contact: `
            <div class="container mx-auto px-4">
                <h2 class="text-3xl font-bold text-center mb-12 editable-element" data-editable="text">
                    Contactez-nous
                    <div class="edit-overlay">Modifier</div>
                </h2>
                <div class="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
                    <div>
                        <h3 class="text-xl font-bold mb-4">Nos coordonnées</h3>
                        <div class="space-y-3">
                            <p class="flex items-center">
                                <i class="fas fa-phone mr-3"></i>
                                <span class="editable-element" data-editable="text">01 23 45 67 89</span>
                            </p>
                            <p class="flex items-center">
                                <i class="fas fa-envelope mr-3"></i>
                                <span class="editable-element" data-editable="text">contact@exemple.fr</span>
                            </p>
                            <p class="flex items-center">
                                <i class="fas fa-map-marker-alt mr-3"></i>
                                <span class="editable-element" data-editable="text">123 Rue Exemple, 75000 Paris</span>
                            </p>
                        </div>
                    </div>
                    <form class="space-y-4">
                        <input type="text" placeholder="Votre nom" class="w-full p-3 border rounded">
                        <input type="email" placeholder="Votre email" class="w-full p-3 border rounded">
                        <textarea placeholder="Votre message" class="w-full p-3 border rounded h-32"></textarea>
                        <button type="submit" class="w-full bg-blue-500 text-white p-3 rounded hover:bg-blue-600">
                            Envoyer
                        </button>
                    </form>
                </div>
            </div>
        `,
        custom: `
            <div class="container mx-auto px-4">
                <h2 class="text-3xl font-bold text-center mb-12 editable-element" data-editable="text">
                    Section Personnalisée
                    <div class="edit-overlay">Modifier</div>
                </h2>
                <div class="text-center">
                    <p class="text-xl text-gray-600 mb-8 editable-element" data-editable="text">
                        Ajoutez votre contenu personnalisé ici
                        <div class="edit-overlay">Modifier</div>
                    </p>
                </div>
            </div>
        `
    };
    
    return templates[type] || templates['custom'];
}

// ========== GESTION DES ÉLÉMENTS ÉDITABLES ==========

function enableEditableElements(container = document) {
    const editables = container.querySelectorAll('.editable-element');
    
    editables.forEach(element => {
        // Retirer les anciens listeners pour éviter les doublons
        element.removeEventListener('click', handleEditableClick);
        element.addEventListener('click', handleEditableClick);
        
        // Ajouter l'overlay d'édition s'il n'existe pas
        if (!element.querySelector('.edit-overlay')) {
            const overlay = document.createElement('div');
            overlay.className = 'edit-overlay';
            overlay.textContent = 'Cliquer pour modifier';
            element.appendChild(overlay);
        }
    });
}

function handleEditableClick(event) {
    if (!isEditModeActive) return;
    
    event.stopPropagation();
    event.preventDefault();
    
    const element = event.currentTarget;
    const editType = element.getAttribute('data-editable');
    
    switch (editType) {
        case 'text':
            editTextElement(element);
            break;
        case 'image':
            editImageElement(element);
            break;
        case 'html':
            editHTMLElement(element);
            break;
        default:
            editTextElement(element);
    }
}

function editTextElement(element) {
    const currentText = element.textContent.replace('Cliquer pour modifier', '').trim();
    const newText = prompt('Modifier le texte:', currentText);
    
    if (newText !== null && newText !== currentText) {
        // Sauvegarder l'ancien texte
        const oldText = currentText;
        
        // Mettre à jour l'élément
        const overlay = element.querySelector('.edit-overlay');
        element.textContent = newText;
        if (overlay) element.appendChild(overlay);
        
        // Sauvegarder la modification
        saveModification('editText', getElementSelector(element), newText, oldText);
        showNotification('✅ Texte modifié avec succès', 'success');
    }
}

function editImageElement(element) {
    // Ouvrir le sélecteur d'images
    showImageSelectorForElement(element);
}

function editHTMLElement(element) {
    const currentHTML = element.innerHTML;
    const newHTML = prompt('Modifier le HTML:', currentHTML);
    
    if (newHTML !== null && newHTML !== currentHTML) {
        element.innerHTML = newHTML;
        saveModification('editHTML', getElementSelector(element), newHTML, currentHTML);
        enableEditableElements(element); // Réactiver l'édition sur les nouveaux éléments
        showNotification('✅ HTML modifié avec succès', 'success');
    }
}

// ========== SÉLECTEUR D'IMAGES ==========

function showImageSelectorForElement(element) {
    selectedElement = element;
    const imageSelector = document.getElementById('imageSelector');
    imageSelector.scrollIntoView({ behavior: 'smooth' });
    showNotification('🖼️ Recherchez une image ci-dessous', 'info');
}

function searchImages(event) {
    if (event.key === 'Enter') {
        const query = event.target.value;
        if (query.trim()) {
            fetchImagesFromAPI(query);
        }
    }
}

async function fetchImagesFromAPI(query) {
    try {
        showNotification('🔍 Recherche d\'images en cours...', 'info');
        
        const response = await fetch(`${API_BASE_URL}/api/get-images?query=${encodeURIComponent(query)}&count=12`);
        const data = await response.json();
        
        if (data.success && data.images) {
            displayImageResults(data.images);
            showNotification(`✅ ${data.images.length} images trouvées`, 'success');
        } else {
            throw new Error('Aucune image trouvée');
        }
    } catch (error) {
        console.error('❌ Erreur recherche images:', error);
        showNotification('❌ Erreur lors de la recherche d\'images', 'error');
    }
}

function displayImageResults(images) {
    const container = document.getElementById('imageResults');
    container.innerHTML = '';
    
    images.forEach(image => {
        const imageDiv = document.createElement('div');
        imageDiv.className = 'image-option';
        imageDiv.onclick = () => selectImage(image.url, imageDiv);
        
        imageDiv.innerHTML = `
            <img src="${image.thumb}" alt="${image.description}" loading="lazy">
            <div class="text-xs p-2 bg-gray-100">
                <p class="font-semibold truncate">${image.description}</p>
                <p class="text-gray-500">par ${image.author}</p>
            </div>
        `;
        
        container.appendChild(imageDiv);
    });
}

function selectImage(imageUrl, imageDiv) {
    // Marquer comme sélectionnée
    document.querySelectorAll('.image-option').forEach(option => {
        option.classList.remove('selected');
    });
    imageDiv.classList.add('selected');
    
    // Appliquer l'image
    if (selectedElement) {
        applyImageToElement(selectedElement, imageUrl);
    }
}

function applyImageToElement(element, imageUrl) {
    if (element.tagName === 'IMG') {
        const oldSrc = element.src;
        element.src = imageUrl;
        saveModification('setImage', getElementSelector(element), imageUrl, oldSrc);
    } else {
        const oldBg = element.style.backgroundImage;
        element.style.backgroundImage = `url(${imageUrl})`;
        element.style.backgroundSize = 'cover';
        element.style.backgroundPosition = 'center';
        saveModification('setImage', getElementSelector(element), imageUrl, oldBg);
    }
    
    showNotification('✅ Image appliquée avec succès', 'success');
}

// ========== UTILITAIRES ==========

function getElementSelector(element) {
    // Générer un sélecteur CSS pour l'élément
    let selector = element.tagName.toLowerCase();
    
    if (element.id) {
        selector = `#${element.id}`;
    } else if (element.className) {
        const classes = element.className.split(' ').filter(c => c && !c.startsWith('edit'));
        if (classes.length > 0) {
            selector += '.' + classes.join('.');
        }
    }
    
    return selector;
}

function saveModification(type, selector, newValue, oldValue) {
    const modification = {
        id: Date.now().toString(),
        type: type,
        selector: selector,
        newValue: newValue,
        oldValue: oldValue,
        timestamp: new Date().toISOString()
    };
    
    modifications.push(modification);
    
    // Sauvegarder en local storage
    localStorage.setItem('iawebgen_modifications', JSON.stringify(modifications));
    
    // Envoyer au backend si on a un site ID
    if (currentSiteId) {
        sendModificationToBackend(modification);
    }
}

async function sendModificationToBackend(modification) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/edit-element?site_id=${currentSiteId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                command: modification.type,
                selector: modification.selector,
                value: modification.newValue,
                page: currentPage
            })
        });
        
        const result = await response.json();
        
        if (!result.success) {
            throw new Error(result.message || 'Erreur serveur');
        }
        
        console.log('✅ Modification sauvegardée sur le serveur');
        
    } catch (error) {
        console.error('❌ Erreur sauvegarde:', error);
        // Continuer en mode local si le serveur n'est pas disponible
    }
}

// ========== STYLES GLOBAUX ==========

function updateGlobalStyle(type, value) {
    const root = document.documentElement;
    
    switch (type) {
        case 'primary':
            root.style.setProperty('--primary-color', value);
            websiteData.primaryColor = value;
            break;
        case 'secondary':
            root.style.setProperty('--secondary-color', value);
            websiteData.secondaryColor = value;
            break;
        case 'font':
            document.body.style.fontFamily = value;
            break;
    }
    
    saveModification('globalStyle', type, value, null);
    showNotification('🎨 Style global mis à jour', 'info');
}

// ========== SAUVEGARDE ET EXPORTATION ==========

function saveChanges() {
    // Sauvegarder toutes les modifications
    const dataToSave = {
        websiteData: websiteData,
        modifications: modifications,
        timestamp: new Date().toISOString()
    };
    
    localStorage.setItem('iawebgen_save', JSON.stringify(dataToSave));
    showNotification('💾 Modifications sauvegardées localement', 'success');
}

async function exportWebsite() {
    try {
        showNotification('📤 Export en cours...', 'info');
        
        // Préparer les données d'export
        const exportData = {
            websiteData: websiteData,
            modifications: modifications,
            currentTemplate: selectedTemplate,
            pages: generatedPages
        };
        
        // Créer et télécharger le fichier
        const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `iawebgen-export-${Date.now()}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        showNotification('✅ Export terminé - fichier téléchargé', 'success');
        
    } catch (error) {
        console.error('❌ Erreur export:', error);
        showNotification('❌ Erreur lors de l\'export', 'error');
    }
}

function resetChanges() {
    if (confirm('⚠️ Êtes-vous sûr de vouloir réinitialiser toutes les modifications ?')) {
        modifications = [];
        editHistory = [];
        editHistoryIndex = -1;
        
        localStorage.removeItem('iawebgen_modifications');
        localStorage.removeItem('iawebgen_save');
        
        // Recharger la page pour restaurer l'état initial
        location.reload();
    }
}

// ========== MODE D'ÉDITION ==========

function toggleEditMode() {
    isEditModeActive = !isEditModeActive;
    const btn = document.getElementById('editModeBtn');
    
    if (isEditModeActive) {
        btn.innerHTML = '<i class="fas fa-edit mr-2"></i>Mode Édition: ON';
        btn.className = btn.className.replace('bg-purple-500', 'bg-green-500');
        document.body.classList.add('edit-mode-active');
        showNotification('🎨 Mode édition activé - Cliquez sur les éléments pour les modifier', 'info');
    } else {
        btn.innerHTML = '<i class="fas fa-edit mr-2"></i>Mode Édition: OFF';
        btn.className = btn.className.replace('bg-green-500', 'bg-purple-500');
        document.body.classList.remove('edit-mode-active');
        hideElementSelection();
        showNotification('🎨 Mode édition désactivé', 'info');
    }
}

function activateElementSelection() {
    if (!isEditModeActive) {
        toggleEditMode();
    }
    showNotification('👆 Cliquez sur un élément pour le modifier', 'info');
}

function hideElementSelection() {
    selectedElement = null;
}

// ========== FONCTIONS EXISTANTES ADAPTÉES ==========

// Gestion du formulaire avec support de l'éditeur
function handleFormSubmit(event) {
    console.log('🔥 DEBUT TRAITEMENT FORMULAIRE');
    event.preventDefault();
    event.stopPropagation();
    
    try {
        generateCompleteWebsite();
    } catch (error) {
        console.error('❌ ERREUR:', error);
        showNotification('❌ Erreur lors de la génération. Veuillez réessayer.');
    }
}

// Initialisation avec éditeur
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 IA WebGen Pro - Version Édition Avancée - Initialisation démarrée');
    
    // Vérifier que tous les éléments existent
    const form = document.getElementById('websiteForm');
    const mainSection = document.getElementById('mainSection');
    const templateSection = document.getElementById('qualityTemplates');
    const previewSection = document.getElementById('previewSection');
    const templateGrid = document.getElementById('templateGrid');
    
    console.log('✅ Éléments trouvés:', {
        form: !!form,
        mainSection: !!mainSection,
        templateSection: !!templateSection,
        previewSection: !!previewSection,
        templateGrid: !!templateGrid
    });
    
    if (currentUser) {
        showUserMenu();
    }
    
    setupPhotoUpload();
    allTemplates = TEMPLATES;
    
    // Initialiser l'éditeur avancé
    initializeAdvancedEditor();
    
    console.log('✅ Initialisation terminée - Templates:', TEMPLATES.length);
});

// Génération avec support de l'éditeur
function generateCompleteWebsite() {
    console.log('🎨 ==> GÉNÉRATION DU SITE COMPLET COMMENCÉE');
    
    const mainSection = document.getElementById('mainSection');
    const templateSection = document.getElementById('qualityTemplates');
    const previewSection = document.getElementById('previewSection');
    
    if (!mainSection || !templateSection || !previewSection) {
        console.error('❌ ERREUR: Éléments DOM manquants');
        showNotification('❌ Erreur technique. Rechargez la page.');
        return;
    }
    
    try {
        // Récupérer toutes les données du formulaire
        const businessName = document.getElementById('businessName').value.trim();
        const description = document.getElementById('description').value.trim();
        const siteType = document.getElementById('siteType').value;
        const userEmail = document.getElementById('userEmail').value.trim();
        const phone = document.getElementById('phone').value.trim();
        const address = document.getElementById('address').value.trim();
        const website = document.getElementById('website').value.trim();
        const slogan = document.getElementById('slogan').value.trim();
        const teamInfo = document.getElementById('teamInfo').value.trim();
        const servicesDetail = document.getElementById('servicesDetail').value.trim();
        
        console.log('📋 Données récupérées:', {
            businessName, 
            siteType, 
            userEmail,
            description: description.substring(0, 50) + '...'
        });
        
        // Réseaux sociaux
        const facebook = document.getElementById('facebook').value.trim();
        const instagram = document.getElementById('instagram').value.trim();
        const linkedin = document.getElementById('linkedin').value.trim();
        const twitter = document.getElementById('twitter').value.trim();
        
        // Pages sélectionnées
        const selectedPages = [];
        document.querySelectorAll('input[id^="page-"]:checked').forEach(checkbox => {
            selectedPages.push(checkbox.id.replace('page-', ''));
        });
        
        console.log('📄 Pages sélectionnées:', selectedPages);
        
        // Validation stricte
        if (!businessName || businessName.length < 2) {
            showNotification('❌ Le nom de votre entreprise est requis (minimum 2 caractères)');
            return;
        }
        if (!description || description.length < 10) {
            showNotification('❌ Veuillez décrire votre activité (minimum 10 caractères)');
            return;
        }
        if (!siteType) {
            showNotification('❌ Veuillez sélectionner le type de site');
            return;
        }
        if (!userEmail || !userEmail.includes('@')) {
            showNotification('❌ Veuillez saisir un email valide');
            return;
        }
        if (selectedPages.length === 0) {
            showNotification('❌ Au moins une page doit être sélectionnée');
            return;
        }
        
        console.log('✅ Validation passée');
        
        // Stocker toutes les données
        websiteData = {
            businessName,
            description,
            siteType,
            userEmail,
            phone,
            address,
            website,
            slogan,
            teamInfo,
            servicesDetail,
            socialMedia: { facebook, instagram, linkedin, twitter },
            selectedPages,
            photos: uploadedPhotos,
            mainTitle: businessName,
            subtitle: slogan || description,
            primaryColor: '#3b82f6',
            secondaryColor: '#1e40af'
        };
        
        console.log('💾 Données stockées dans websiteData');
        
        // Générer et afficher les templates
        console.log('🎨 Génération des templates...');
        displayTemplates();
        
        // Navigation avec vérification
        console.log('🔀 Navigation vers les templates...');
        mainSection.style.display = 'none';
        templateSection.style.display = 'block';
        previewSection.style.display = 'none';
        window.scrollTo(0, 0);
        
        showNotification(`✅ Site ${websiteData.selectedPages.length} pages prêt ! Choisissez votre thème.`);
        console.log('🎉 GÉNÉRATION TERMINÉE AVEC SUCCÈS');
        
    } catch (error) {
        console.error('❌ ERREUR DANS GÉNÉRATION:', error);
        showNotification('❌ Erreur technique. Veuillez réessayer.');
    }
}

// Fonction de notification améliorée
function showNotification(message, type = 'info') {
    const notification = document.getElementById('notification');
    const content = document.getElementById('notificationContent');
    const text = document.getElementById('notificationText');
    
    const colors = {
        info: 'bg-blue-500',
        success: 'bg-green-500',
        warning: 'bg-yellow-500',
        error: 'bg-red-500'
    };
    
    // Changer la couleur selon le type
    content.className = `${colors[type] || colors.info} text-white px-6 py-3 rounded-lg shadow-lg`;
    
    text.textContent = message;
    notification.style.display = 'block';
    
    // Auto-masquer après 4 secondes
    setTimeout(() => {
        notification.style.display = 'none';
    }, 4000);
}

console.log('🎨 IA WebGen - Système d\'édition avancé chargé avec succès');