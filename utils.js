numgames = 0

async function loadAllGames() {
    // Centralized list of team member JSON files
    const jsonFiles = [
        "games.json",
        "metadata/grant_games.json",
        "metadata/naijei_games.json",
        "metadata/ziqi_games.json",
        "metadata/gene_games.json",
        "scraping/GNHUST/games_data/games_metadata.json",
        "scraping/js13/games_metadata.json"
        // Add new members' files here as needed
    ];

    const allGames = [];

    for (const file of jsonFiles) {
        try {
            const response = await fetch(file);
            if (response.ok) {
                const data = await response.json();
                allGames.push(...data);
            } else {
                console.error(`Error loading ${file}:`, response.statusText);
            }
        } catch (error) {
            console.error(`Error loading ${file}:`, error);
        }
    }

    numgames = allGames.length
    updateTotalGames();
    return allGames;
}


function updateTotalGames() {
    const numGamesElement = document.querySelector('.numgames');
    if (numGamesElement) {
        numGamesElement.textContent = `Currently holding ${numgames} games!`;
    }
}