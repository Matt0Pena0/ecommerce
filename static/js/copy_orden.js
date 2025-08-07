// Add this script to your template or a separate .js file
document.addEventListener('DOMContentLoaded', function() {
    // Select the button by its ID
    const copyButton = document.getElementById('copiar-txt-btn');

    if (copyButton) {
        // Add a click event listener to the button
        copyButton.addEventListener('click', async () => {
            // Get the URL directly from the button's data- attribute
            // The key is to use the camelCase version in JavaScript
            // for a kebab-case data attribute.
            const url = copyButton.dataset.urlCopyOrden;
            
            try {
                // Fetch the text content from the URL
                const response = await fetch(url);
                const text = await response.text();

                // Use the Clipboard API to write the text
                await navigator.clipboard.writeText(text);
                
                showToast('¡Texto copiado al portapapeles!');
            } catch (err) {
                console.error('Error al copiar el texto:', err);
                showToast('Error al copiar el texto. Inténtalo de nuevo.');
            }
        });
    }
});
