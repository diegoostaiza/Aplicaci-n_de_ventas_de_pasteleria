const menuButton = document.querySelector("#menu-mobile");
menuButton.addEventListener("click", (e) => {
  const menu = document.querySelector(".mobile-links");
  menu.classList.toggle("hidden");
});


window.addEventListener("scroll", function () {
  var navbar = document.getElementById("navbar");
  var screenWidth =
    window.innerWidth ||
    document.documentElement.clientWidth ||
    document.body.clientWidth;
  if (screenWidth >= 640) {
    if (window.scrollY > 0) {
      navbar.classList.remove("lg:bg-transparent");
      navbar.classList.add("bg-red-950");
    } else {
      navbar.classList.remove("bg-red-950");
      navbar.classList.add("lg:bg-transparent");
    }
  } else {
    navbar.classList.remove("lg:bg-transparent");
    navbar.classList.add("bg-red-950");
  }
});

var swiper = new Swiper(".mySwiper", {
  slidesPerView: 1,
  spaceBetween: 10,
  freeMode: true,
  pagination: {
    el: ".swiper-pagination",
    clickable: true,
  },
  breakpoints: {
    640: {
      slidesPerView: 2,
      spaceBetween: 20,
    },
    
    930:{
      slidesPerView: 3,
      spaceBetween: 10,
    },
    1200:{
      slidesPerView: 4,
      spaceBetween: 0,
    }  
  },
});


var swiper = new Swiper(".mySwipers", {
  slidesPerView: 1,
  spaceBetween: 30,
  centeredSlides: true,
  autoplay: {
    delay: 2000,
    disableOnInteraction: false,
  },
  breakpoints: {
    640: {
      slidesPerView: 2,
      spaceBetween: 20,
    },
    830:{
      slidesPerView: 2,
      spaceBetween: 80,
    },
    1200:{
      slidesPerView: 1,
      spaceBetween: 0,
    }  
  },
 
});