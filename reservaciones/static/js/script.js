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

    930: {
      slidesPerView: 3,
      spaceBetween: 10,
    },
    1200: {
      slidesPerView: 4,
      spaceBetween: 0,
    },
  },
});

var swiper = new Swiper(".mySwipers", {
  slidesPerView: 1,
  spaceBetween: 30,
  centeredSlides: true,
  autoplay: {
    delay: 3000,
    disableOnInteraction: false,
  },
  breakpoints: {
    640: {
      slidesPerView: 2,
      spaceBetween: 20,
    },
    830: {
      slidesPerView: 2,
      spaceBetween: 80,
    },
    1200: {
      slidesPerView: 1,
      spaceBetween: 0,
    },
  },
});




document.addEventListener("DOMContentLoaded", function () {
  const productContainers = document.querySelectorAll(
    ".flex.justify-between.gap-4"
  );

  productContainers.forEach((container) => {
    const decrementButton = container.querySelector(".decrement");
    const incrementButton = container.querySelector(".increment");
    const quantityElement = container.querySelector(".quantity");
    const priceElement = container.querySelector(".precio");

    decrementButton.addEventListener("click", function () {
      updateQuantity(quantityElement, priceElement, -1);
    });

    incrementButton.addEventListener("click", function () {
      updateQuantity(quantityElement, priceElement, 1);
    });
  });

  function updateQuantity(quantityElement, priceElement, change) {
    let currentQuantity = parseInt(quantityElement.innerText, 10) || 0;
    let priceText = priceElement.innerText.replace(/[^\d.,]/g, "");
    let price = parseFloat(priceText.replace(",", ".")) || 0;

    currentQuantity = Math.max(1, currentQuantity + change);
    quantityElement.innerText = currentQuantity;

    updateTotals();
  }

  function updateTotals() {
    let subTotal = 0;
    productContainers.forEach((container) => {
      let quantity = parseInt(container.querySelector(".quantity").innerText, 10) || 0;
      let priceText = container.querySelector(".precio").innerText.replace(/[^\d.,]/g, "");
      let price = parseFloat(priceText.replace(",", ".")) || 0;
      subTotal += quantity * price;
    });
    let iva = subTotal * 0.12;
    let ivaRedondeado = iva.toFixed(2);
    let total = subTotal + parseFloat(ivaRedondeado);

    document.getElementById("sub_total_carrito").innerText = `$${subTotal.toFixed(2)}`;
    document.getElementById("iva_redondeado").innerText = `$${ivaRedondeado}`;
    document.getElementById("total").innerText = `$${total.toFixed(2)}`;

  

  }

  document.querySelectorAll(".close-button").forEach(function (button) {
    button.addEventListener("click", function () {
      var toast = this.closest(".toast");
      if (toast) {
        toast.style.display = "none";
      }
    });
  });

  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      var cookies = document.cookie.split(";");
      for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }




  $('.enviar').click(function() {
    var id = $(this).data("id-producto");

    // Encuentra el elemento '.quantity' específico dentro del contenedor del botón presionado
    var eml = $(this).closest('.flex').find('.quantity');
    
    // Accede al valor numérico dentro del elemento span con la clase 'quantity'
    var cantidadp = parseFloat(eml.text());
    
    console.log("Cantidad:", cantidadp);
    
    $.ajax({
        type: "GET",
        url: "/productos/carrito/agg",
        data: {
            productoid: id,
            cantidad : cantidadp
        },
        success: function(data) {
            eml.text(data.quantity);
            document.getElementById("sub_total_carrito").innerText = "$ " +data.sub_total_carrito;
            document.getElementById("iva_redondeado").innerText = "$ " +data.iva_redondeado;
            document.getElementById("total").innerText = "$ " +data.total;
        }
    });
});




});


