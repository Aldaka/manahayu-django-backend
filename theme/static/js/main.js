function filterMenu(category) {
    const items = document.querySelectorAll('[data-category]');
    items.forEach(item => {
      if (category === 'all' || item.getAttribute('data-category') === category) {
        item.style.display = 'flex';
      } else {
        item.style.display = 'none';
      }
    });
  }
  
  function setActiveCategory(button, category) {
    // Hapus semua kelas aktif
    document.querySelectorAll('.category-btn').forEach(btn => {
      btn.classList.remove('bg-secondary', 'text-white', 'shadow');
      btn.classList.add('text-gray-500');
    });
  
    // Tambahkan kelas aktif ke tombol yang diklik
    button.classList.add('bg-secondary', 'text-white', 'shadow');
    button.classList.remove('text-gray-500');
  
    // Jalankan fungsi filter jika ada
    if (typeof filterMenu === 'function') {
      filterMenu(category);
    }
  }
  
  document.addEventListener("DOMContentLoaded", function () {
    // Aktifkan menu dropdown untuk mobile
    setupMenu();
  
    // Aktifkan interaksi FAQ di footer
    setupFAQ();
  
    // Carousel setup
    let currentIndex = 0;
    const images = document.getElementById('carouselImages')?.children || [];
    const indicators = document.getElementById('carouselIndicators')?.children || [];
  
    function updateCarousel() {
      const offset = -currentIndex * 100;
      const container = document.getElementById('carouselImages');
      if (container) {
        container.style.transform = `translateX(${offset}%)`;
      }
  
      for (let i = 0; i < indicators.length; i++) {
        indicators[i].classList.remove('bg-green-600');
        indicators[i].classList.add('bg-gray-300');
      }
      if (indicators[currentIndex]) {
        indicators[currentIndex].classList.add('bg-green-600');
      }
    }
  
    function moveSlide(step) {
      if (!images.length) return;
      currentIndex += step;
      if (currentIndex >= images.length) currentIndex = 0;
      if (currentIndex < 0) currentIndex = images.length - 1;
      updateCarousel();
    }
  
    setInterval(() => moveSlide(1), 3000);
  
    const prevBtn = document.querySelector(".prev-slide");
    if (prevBtn) {
      prevBtn.addEventListener("click", () => moveSlide(-1));
    }
  
    const nextBtn = document.querySelector(".next-slide");
    if (nextBtn) {
      nextBtn.addEventListener("click", () => moveSlide(1));
    }
  });
  
  // Menu mobile toggle
  function setupMenu() {
    const btn = document.getElementById("menu-btn");
    const menu = document.getElementById("nav-menu");
  
    if (btn && menu) {
      btn.addEventListener("click", () => {
        menu.classList.toggle("hidden");
      });
    }
  }
  
  // FAQ interaktif
  function setupFAQ() {
    const buttons = document.querySelectorAll('.faq-toggle');
  
    buttons.forEach(button => {
      button.addEventListener('click', () => {
        const content = button.nextElementSibling;
        const icon = button.querySelector('span:last-child');
  
        buttons.forEach(otherBtn => {
          const otherContent = otherBtn.nextElementSibling;
          const otherIcon = otherBtn.querySelector('span:last-child');
          if (otherBtn !== button) {
            otherContent.classList.add('hidden');
            otherIcon.textContent = '+';
          }
        });
  
        const isHidden = content.classList.contains('hidden');
        content.classList.toggle('hidden', !isHidden);
        icon.textContent = isHidden ? '−' : '+';
  
        if (isHidden) {
          content.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      });
    });
  }

  // Menu Filter
  function setActiveCategory(button, category) {
    // Ubah style tombol aktif
    const buttons = document.querySelectorAll(".category-btn");
    buttons.forEach(btn => btn.classList.remove("bg-secondary", "text-white"));
    button.classList.add("bg-secondary", "text-white");
  
    // Filter kartu menu
    const cards = document.querySelectorAll("[data-category]");
    cards.forEach(card => {
      if (category === "all" || card.dataset.category === category) {
        card.style.display = "block";
      } else {
        card.style.display = "none";
      }
    });
  }


  // Carousel Room
//   document.addEventListener("DOMContentLoaded", function () {
//     const images = document.querySelectorAll("#carouselImages img");
//     const indicators = document.querySelectorAll("#carouselIndicators span");
//     let currentIndex = 0;

//     // Show the first image and set the first indicator as active
//     images[currentIndex].classList.add("active");
//     indicators[currentIndex].classList.add("bg-green-600");

//     // Set up auto slide every 3 seconds
//     setInterval(function () {
//         changeSlide(1);  // Auto move to the next slide every 3 seconds
//     }, 3000);

//     // Next button functionality
//     document.querySelector(".next-slide").addEventListener("click", function () {
//         changeSlide(1);  // Move to the next slide when clicked
//     });

//     // Previous button functionality
//     document.querySelector(".prev-slide").addEventListener("click", function () {
//         changeSlide(-1);  // Move to the previous slide when clicked
//     });

//     function changeSlide(direction) {
//         // Remove the "active" class from the current image and indicator
//         images[currentIndex].classList.remove("active");
//         indicators[currentIndex].classList.remove("bg-green-600");

//         // Calculate the next index
//         currentIndex = (currentIndex + direction + images.length) % images.length;

//         // Add the "active" class to the new image and indicator
//         images[currentIndex].classList.add("active");
//         indicators[currentIndex].classList.add("bg-green-600");
//     }
// });



// Menus Script




