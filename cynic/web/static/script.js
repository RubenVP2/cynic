document.addEventListener('alpine:init', () => {
    Alpine.data('cynicApp', () => ({
        // --- État de l'application (les variables) ---
        contexte: '',
        reponse: '',
        proposerAuPalmares: false,
        isLoading: false,
        result: null,
        error: null,

        // --- Logique dérivée (computed properties) ---

        /**
         * Calcule la couleur du score en fonction de sa valeur.
         * @returns {string} Classes Tailwind pour la couleur.
         */
        get scoreColor() {
            if (!this.result) return 'text-white';
            const score = this.result.score;
            if (score >= 7) return 'text-red-400';
            if (score >= 4) return 'text-yellow-400';
            return 'text-green-400';
        },

        /**
         * Génère le HTML de la réponse avec les expressions cyniques surlignées.
         * @returns {string} HTML de la réponse formatée.
         */
        get highlightedResponse() {
            if (!this.result) return '';

            let texteSurligne = this.reponse;

            // Fonction pour échapper les caractères spéciaux pour la RegExp
            const escapeRegExp = (string) => {
                return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
            };

            if (this.result.expressions_cyniques && this.result.expressions_cyniques.length > 0) {
                this.result.expressions_cyniques.forEach(phrase => {
                    const escapedPhrase = escapeRegExp(phrase);
                    const regex = new RegExp(escapedPhrase, 'gi');
                    texteSurligne = texteSurligne.replace(regex, `<mark>$&</mark>`);
                });
            }
            return texteSurligne;
        },

        // --- Actions (les fonctions) ---

        /**
         * Fonction principale appelée lors de la soumission du formulaire.
         */
        async analyze() {
            // Réinitialiser l'état avant chaque appel
            this.isLoading = true;
            this.result = null;
            this.error = null;

            try {
                const response = await fetch('/api/analyze', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        contexte: this.contexte,
                        reponse: this.reponse,
                        proposer_au_palmares: this.proposerAuPalmares
                    }),
                });

                const data = await response.json();

                if (!response.ok) {
                    // Si l'API retourne une erreur (ex: 503), la récupérer du JSON
                    throw new Error(data.detail || 'Une erreur inconnue est survenue.');
                }

                // Mettre à jour le résultat en cas de succès
                this.result = data;

            } catch (err) {
                // Capturer les erreurs réseau ou celles levées manuellement
                this.error = err.message;
            } finally {
                // Dans tous les cas, arrêter le chargement
                this.isLoading = false;
                // S'assurer que les icônes sont re-rendues si elles apparaissent dynamiquement
                this.$nextTick(() => {
                    lucide.createIcons();
                });
            }
        }
    }));
});