/**
 * JavaScript pour la fonctionnalité Slido/Interactive
 */

document.addEventListener('DOMContentLoaded', function() {
    // Gestion des votes
    setupVoteHandlers();
    
    // Gestion des actions de modération
    setupModerationHandlers();
    
    // Rafraîchissement automatique des questions (toutes les 30 secondes)
    setupAutoRefresh();
});

/**
 * Configure les gestionnaires d'événements pour les votes
 */
function setupVoteHandlers() {
    document.querySelectorAll('.vote-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            
            const questionId = this.dataset.questionId;
            const voteUrl = this.dataset.voteUrl;
            
            // Animation de vote
            this.classList.add('vote-animate');
            setTimeout(() => {
                this.classList.remove('vote-animate');
            }, 500);
            
            // Envoyer la requête AJAX pour voter
            fetch(voteUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCsrfToken(),
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question_id: questionId }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Mettre à jour le compteur de votes
                    const voteCount = document.querySelector(`#vote-count-${questionId}`);
                    voteCount.textContent = data.votes_count;
                    
                    // Toggle de la classe active
                    if (data.user_has_voted) {
                        this.classList.add('active');
                    } else {
                        this.classList.remove('active');
                    }
                } else {
                    // Afficher un message d'erreur
                    showToast('Erreur', data.error || 'Une erreur est survenue', 'error');
                }
            })
            .catch(error => {
                console.error('Erreur:', error);
                showToast('Erreur', 'Impossible de traiter votre vote', 'error');
            });
        });
    });
}

/**
 * Configure les gestionnaires d'événements pour les actions de modération
 */
function setupModerationHandlers() {
    // Gestionnaire pour marquer une question comme répondue
    document.querySelectorAll('.mark-answered-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            
            const questionId = this.dataset.questionId;
            const actionUrl = this.dataset.url;
            const questionCard = document.querySelector(`#question-${questionId}`);
            
            fetch(actionUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCsrfToken(),
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question_id: questionId }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Appliquer la classe question-answered
                    questionCard.classList.toggle('question-answered');
                    
                    // Mettre à jour l'icône et le texte du bouton
                    if (data.est_repondue) {
                        this.innerHTML = '<i class="fas fa-undo me-1"></i> Marquer comme non répondue';
                        showToast('Succès', 'Question marquée comme répondue', 'success');
                    } else {
                        this.innerHTML = '<i class="fas fa-check-circle me-1"></i> Marquer comme répondue';
                        showToast('Succès', 'Question marquée comme non répondue', 'success');
                    }
                } else {
                    showToast('Erreur', data.error || 'Une erreur est survenue', 'error');
                }
            })
            .catch(error => {
                console.error('Erreur:', error);
                showToast('Erreur', 'Impossible de traiter votre demande', 'error');
            });
        });
    });
    
    // Gestionnaire pour épingler une question
    document.querySelectorAll('.pin-question-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            
            const questionId = this.dataset.questionId;
            const actionUrl = this.dataset.url;
            const questionCard = document.querySelector(`#question-${questionId}`);
            
            fetch(actionUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCsrfToken(),
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question_id: questionId }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Appliquer la classe question-pinned
                    questionCard.classList.toggle('question-pinned');
                    
                    // Mettre à jour l'icône et le texte du bouton
                    if (data.est_epinglee) {
                        this.innerHTML = '<i class="fas fa-unlink me-1"></i> Désépingler';
                        showToast('Succès', 'Question épinglée', 'success');
                    } else {
                        this.innerHTML = '<i class="fas fa-thumbtack me-1"></i> Épingler';
                        showToast('Succès', 'Question désépinglée', 'success');
                    }
                    
                    // Réorganiser les questions (déplacer les questions épinglées en haut)
                    if (data.est_epinglee) {
                        const questionsContainer = questionCard.parentElement;
                        questionsContainer.prepend(questionCard);
                    }
                } else {
                    showToast('Erreur', data.error || 'Une erreur est survenue', 'error');
                }
            })
            .catch(error => {
                console.error('Erreur:', error);
                showToast('Erreur', 'Impossible de traiter votre demande', 'error');
            });
        });
    });
    
    // Gestion des approbations/rejets de questions
    document.querySelectorAll('.approve-btn, .reject-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            
            const questionId = this.dataset.questionId;
            const actionUrl = this.dataset.url;
            const questionItem = document.querySelector(`#question-item-${questionId}`);
            
            fetch(actionUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCsrfToken(),
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question_id: questionId }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Animer la suppression de l'élément de la liste
                    questionItem.style.transition = 'all 0.3s ease';
                    questionItem.style.opacity = '0';
                    questionItem.style.height = '0';
                    
                    setTimeout(() => {
                        questionItem.remove();
                        
                        // Mettre à jour le compteur
                        const pendingCount = document.getElementById('pending-questions-count');
                        if (pendingCount) {
                            const currentCount = parseInt(pendingCount.textContent) || 0;
                            pendingCount.textContent = Math.max(0, currentCount - 1);
                        }
                        
                        if (this.classList.contains('approve-btn')) {
                            showToast('Succès', 'Question approuvée', 'success');
                        } else {
                            showToast('Succès', 'Question rejetée', 'success');
                        }
                    }, 300);
                } else {
                    showToast('Erreur', data.error || 'Une erreur est survenue', 'error');
                }
            })
            .catch(error => {
                console.error('Erreur:', error);
                showToast('Erreur', 'Impossible de traiter votre demande', 'error');
            });
        });
    });
}

/**
 * Configure le rafraîchissement automatique des questions
 */
function setupAutoRefresh() {
    const questionsContainer = document.getElementById('questions-container');
    const sessionSlug = document.querySelector('meta[name="session-slug"]')?.content;
    
    if (questionsContainer && sessionSlug) {
        // Rafraîchir toutes les 30 secondes
        setInterval(() => {
            fetch(`/interactive/session/${sessionSlug}/questions-json/`)
                .then(response => response.json())
                .then(data => {
                    if (data.questions) {
                        updateQuestionsList(data.questions);
                    }
                })
                .catch(error => console.error('Erreur de rafraîchissement:', error));
        }, 30000); // 30 secondes
    }
}

/**
 * Met à jour la liste des questions avec les nouvelles données
 * @param {Array} questions - Liste des questions à jour
 */
function updateQuestionsList(questions) {
    const questionsContainer = document.getElementById('questions-container');
    const existingQuestionIds = Array.from(
        document.querySelectorAll('.question-card')
    ).map(el => el.dataset.questionId);
    
    // Ajouter les nouvelles questions
    questions.forEach(question => {
        if (!existingQuestionIds.includes(question.id.toString())) {
            const questionHtml = createQuestionCard(question);
            questionsContainer.insertAdjacentHTML('afterbegin', questionHtml);
        } else {
            // Mettre à jour les questions existantes
            const questionCard = document.querySelector(`#question-${question.id}`);
            if (questionCard) {
                const voteCount = questionCard.querySelector('.vote-count');
                if (voteCount) {
                    voteCount.textContent = question.votes_count;
                }
                
                // Mettre à jour les états
                if (question.est_repondue) {
                    questionCard.classList.add('question-answered');
                } else {
                    questionCard.classList.remove('question-answered');
                }
                
                if (question.est_epinglee) {
                    questionCard.classList.add('question-pinned');
                    questionsContainer.prepend(questionCard);
                } else {
                    questionCard.classList.remove('question-pinned');
                }
            }
        }
    });
}

/**
 * Crée le HTML pour une carte de question
 * @param {Object} question - Données de la question
 * @returns {string} HTML de la carte de question
 */
function createQuestionCard(question) {
    return `
    <div id="question-${question.id}" data-question-id="${question.id}" class="question-card card mb-3 ${question.est_epinglee ? 'question-pinned' : ''} ${question.est_repondue ? 'question-answered' : ''}">
        <div class="card-body">
            <div class="d-flex">
                <div class="me-3 text-center">
                    <div class="vote-btn ${question.user_has_voted ? 'active' : ''}" data-question-id="${question.id}" data-vote-url="/interactive/question/${question.id}/vote/">
                        <i class="fas fa-caret-up fa-2x"></i>
                    </div>
                    <div id="vote-count-${question.id}" class="vote-count">${question.votes_count}</div>
                </div>
                <div class="flex-grow-1">
                    <p class="card-text">${question.contenu}</p>
                    <div class="d-flex justify-content-between align-items-center">
                        <small class="text-muted">
                            ${question.est_anonyme ? '<span class="anonymous-badge">Anonyme</span>' : `Par ${question.auteur_nom}`} 
                            · ${question.date_creation}
                        </small>
                        <div class="question-actions">
                            ${question.can_moderate ? `
                            <button class="btn btn-sm btn-outline-primary pin-question-btn" data-question-id="${question.id}" data-url="/interactive/question/${question.id}/epingler/">
                                <i class="fas ${question.est_epinglee ? 'fa-unlink' : 'fa-thumbtack'} me-1"></i>
                                ${question.est_epinglee ? 'Désépingler' : 'Épingler'}
                            </button>
                            <button class="btn btn-sm btn-outline-success ms-1 mark-answered-btn" data-question-id="${question.id}" data-url="/interactive/question/${question.id}/repondre/">
                                <i class="fas ${question.est_repondue ? 'fa-undo' : 'fa-check-circle'} me-1"></i>
                                ${question.est_repondue ? 'Marquer comme non répondue' : 'Marquer comme répondue'}
                            </button>
                            ` : ''}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>`;
}

/**
 * Récupère le token CSRF à partir des cookies
 * @returns {string} Token CSRF
 */
function getCsrfToken() {
    const name = 'csrftoken';
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Affiche un message toast
 * @param {string} title - Titre du toast
 * @param {string} message - Message du toast
 * @param {string} type - Type de toast (success, error, warning, info)
 */
function showToast(title, message, type = 'info') {
    // Vérifier si toastr est disponible
    if (typeof toastr !== 'undefined') {
        toastr[type](message, title);
        return;
    }
    
    // Fallback si toastr n'est pas disponible
    const toast = document.createElement('div');
    toast.className = `toast-notification toast-${type}`;
    toast.innerHTML = `
        <div class="toast-header">
            <strong>${title}</strong>
            <button type="button" class="btn-close"></button>
        </div>
        <div class="toast-body">${message}</div>
    `;
    
    document.body.appendChild(toast);
    
    // Animation d'entrée
    setTimeout(() => {
        toast.style.opacity = '1';
        toast.style.transform = 'translateY(0)';
    }, 10);
    
    // Fermeture automatique après 3 secondes
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(-20px)';
        
        // Supprimer l'élément après l'animation de sortie
        setTimeout(() => {
            toast.remove();
        }, 300);
    }, 3000);
    
    // Gestion du bouton de fermeture
    const closeBtn = toast.querySelector('.btn-close');
    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateY(-20px)';
            
            setTimeout(() => {
                toast.remove();
            }, 300);
        });
    }
}
