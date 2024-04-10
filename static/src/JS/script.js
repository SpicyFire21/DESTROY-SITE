document.getElementById('file-input').addEventListener('change', function(event) {
    var selectedFile = event.target.files[0];
    var preview = document.getElementById('selected-image');

    // Crée un objet FileReader pour lire le contenu de l'image sélectionnée
    var reader = new FileReader();

    reader.onload = function(event) {
        preview.src = event.target.result;
        preview.style.display = 'block';
    };

    // Lit le contenu de l'image en tant qu'URL de données
    reader.readAsDataURL(selectedFile);
});
