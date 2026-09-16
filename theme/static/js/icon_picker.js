document.addEventListener('DOMContentLoaded', function() {
    const iconPicker = document.querySelector('.icon-picker');
    const iconPaths = iconPicker.getAttribute('data-icon-paths').split(',');

    // Membuat tombol untuk memilih ikon
    iconPicker.addEventListener('click', function() {
        const iconSelector = document.createElement('div');
        iconSelector.classList.add('icon-selector');

        iconPaths.forEach(function(iconClass) {
            const iconImage = document.createElement('img');
            iconImage.src = `https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/svgs/${iconClass}.svg`;  // Gambar SVG untuk setiap ikon FontAwesome
            iconImage.classList.add('icon-image');
            iconImage.setAttribute('data-icon', iconClass);
            iconSelector.appendChild(iconImage);
        });

        // Menambahkan pemilih ikon ke halaman
        document.body.appendChild(iconSelector);

        iconSelector.addEventListener('click', function(event) {
            if (event.target && event.target.matches('img')) {
                iconPicker.value = event.target.getAttribute('data-icon');
                iconSelector.remove();  // Menutup pemilih ikon setelah memilih
            }
        });
    });
});
