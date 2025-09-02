document.addEventListener('DOMContentLoaded', () => {
    const searchButton = document.getElementById('searchButton');
    const ingredientInput = document.getElementById('ingredientInput');
    const recipesContainer = document.getElementById('recipesContainer');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const errorIndicator = document.getElementById('errorIndicator');
    const premiumButton = document.getElementById('premiumButton');
    const paymentModal = document.getElementById('paymentModal');
    const closeModalBtn = document.getElementById('closeModalBtn');

    searchButton.addEventListener('click', async () => {
        const ingredients = ingredientInput.value.split(',').map(s => s.trim()).filter(s => s);
        if (ingredients.length === 0) {
            // Using a custom message box instead of alert()
            // In a full implementation, you would use a dedicated UI element
            alert('Please enter at least one ingredient.');
            return;
        }

        loadingIndicator.classList.remove('hidden');
        errorIndicator.classList.add('hidden');
        recipesContainer.innerHTML = '';

        try {
            const response = await fetch('/search_recipes', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ ingredients: ingredients })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const recipes = await response.json();
            if (recipes && recipes.length > 0) {
                recipes.forEach(recipe => {
                    const recipeCard = `
                        <a href="${recipe.url}" target="_blank" class="card block">
                            <img src="https://placehold.co/600x400/000000/FFFFFF?text=Recipe" alt="Recipe Image" class="recipe-image">
                            <div class="p-4">
                                <h2 class="text-xl font-semibold text-gray-800 mb-2">${recipe.label}</h2>
                                <ul class="text-sm text-gray-600">
                                    ${recipe.ingredientLines.map(line => `<li>- ${line}</li>`).join('')}
                                </ul>
                            </div>
                        </a>
                    `;
                    recipesContainer.innerHTML += recipeCard;
                });
            } else {
                recipesContainer.innerHTML = '<p class="text-center text-gray-500 col-span-full">No recipes found for these ingredients.</p>';
            }
        } catch (error) {
            console.error('Error fetching recipes:', error);
            errorIndicator.classList.remove('hidden');
        } finally {
            loadingIndicator.classList.add('hidden');
        }
    });

    premiumButton.addEventListener('click', () => {
        paymentModal.classList.remove('hidden');
    });

    closeModalBtn.addEventListener('click', () => {
        paymentModal.classList.add('hidden');
    });
});