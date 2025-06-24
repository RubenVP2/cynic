document.addEventListener('alpine:init', () => {
    Alpine.data('hallOfFameApp', () => ({
        // --- État de l'application ---
        entries: [],
        isLoading: false,
        error: null,

        // --- Actions ---

        /**
         * Récupère les données du palmarès depuis l'API.
         */
        async fetchData() {
            this.isLoading = true;
            this.error = null;

            try {
                const response = await fetch('/api/hall-of-fame');
                const data = await response.json();

                if (!response.ok) {
                    throw new Error(data.detail || 'Impossible de charger les données.');
                }

                // Trier les entrées par score (du plus haut au plus bas)
                this.entries = data.sort((a, b) => b.score - a.score);

            } catch (err) {
                this.error = err.message;
            } finally {
                this.isLoading = false;
                // S'assurer que les icônes sont re-rendues après l'affichage des données
                this.$nextTick(() => {
                    lucide.createIcons();
                });
            }
        },
    }));
});