function openLinkedInConnections() {
    // Select each connection card's name element
    document.querySelectorAll('.mn-connection-card__name').forEach(card => {
        // Attempt to find the URL from a known data attribute or surrounding link
        let profileUrl = card.closest('.mn-connection-card').querySelector('a')?.href;
        
        // Open each profile URL in a new tab if found
        if (profileUrl) {
            window.open(profileUrl, '_blank');
        } else {
            console.log("No URL found for one of the connections.");
        }
    });
}

openLinkedInConnections();
