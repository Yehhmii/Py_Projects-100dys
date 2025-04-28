document.addEventListener("DOMContentLoaded", () => {
    // Handle all "Add to Cart" buttons
    document.querySelectorAll(".add-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        const id = btn.dataset.id;
        let qty = 1;
        // on detail page, use the qty input if present
        const qtyInput = document.querySelector("#qty");
        if (qtyInput) qty = parseInt(qtyInput.value) || 1;
  
        fetch("/add_to_cart", {
          method: "POST",
          headers: { "Content-Type":"application/x-www-form-urlencoded" },
          body: new URLSearchParams({
            product_id: id,
            quantity: qty
          })
        })
        .then(r => r.json())
        .then(data => {
          if (data.success) {
            document.getElementById("cart-count").innerText = data.cartSize;
            btn.innerText = "✔ Added";
            setTimeout(() => btn.innerText = "Add to Cart", 1000);
          }
        });
      });
    });
  
    // Detail page: + / – buttons
    const inc = document.getElementById("inc"), dec = document.getElementById("dec"), qty = document.getElementById("qty");
    if (inc && dec && qty) {
      inc.addEventListener("click", () => qty.value = parseInt(qty.value||0) + 1);
      dec.addEventListener("click", () => qty.value = Math.max(1, parseInt(qty.value||1) - 1));
    }
  });
  




//   css animation for product grid card items
document.addEventListener("DOMContentLoaded", () => {
    const cards = document.querySelectorAll(".product-grid .card");
  
    // Give each card its own index (for staggered delay)
    cards.forEach((card, i) => {
      card.dataset.index = i;
    });
  
    // IntersectionObserver callback
    const obs = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
  
        const card = entry.target;
        const delay = card.dataset.index * 100; // ms per card
        setTimeout(() => {
          card.classList.add("in-view");
        }, delay);
  
        observer.unobserve(card);
      });
    }, {
      threshold: 0.1  // fire when 10% of card is visible
    });
  
    // Observe each card
    cards.forEach(card => obs.observe(card));
  });

  


// creating the typewriter effect 
document.addEventListener('DOMContentLoaded', () => {
    const container = document.querySelector('.my-subtitle-1');
    // pull the original phrases
    const phrases = Array.from(container.querySelectorAll('h1')).map(h1 => h1.textContent);
    // clear them out; we'll re-create
    container.innerHTML = '';
  
    const TYPING_SPEED = 100;   // ms per character
    const LINE_DELAY   = 500;   // ms between lines
    const RESTART_DELAY= 2000;  // ms before full restart
  
    function typeLines() {
      container.innerHTML = '';
      let lineIndex = 0;
  
      function typeLine() {
        if (lineIndex >= phrases.length) {
          // all lines done → wait & restart
          setTimeout(typeLines, RESTART_DELAY);
          return;
        }
        const text = phrases[lineIndex];
        const h1   = document.createElement('h1');
        container.appendChild(h1);
  
        let charIndex = 0;
        function typeChar() {
          if (charIndex < text.length) {
            h1.textContent += text[charIndex++];
            setTimeout(typeChar, TYPING_SPEED);
          } else {
            // line done → next line
            lineIndex++;
            setTimeout(typeLine, LINE_DELAY);
          }
        }
        typeChar();
      }
  
      typeLine();
    }
  
    typeLines();
  }); 




//  observer for the product device section
document.addEventListener("DOMContentLoaded", () => {
    const opts = {
      root: null,
      rootMargin: "0px",
      threshold: 0.1
    };
  
    const observer = new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        const el = entry.target;
  
        if (el.classList.contains("product-device-2")) {
          el.classList.add("animate__animated", "animate__rotateInDownRight");
        } else {
          el.classList.add("animate__animated", "animate__rotateInDownLeft");
        }
  
        // When the animation finishes, tilt back to rotate(30deg)
        el.addEventListener('animationend', () => {
          el.style.transform = 'rotate(30deg)';
        }, { once: true });
  
        obs.unobserve(el);
      });
    }, opts);
  
    document.querySelectorAll(".product-device, .product-device-2")
      .forEach(el => observer.observe(el));
  });
  

  


//   for the text in product device section
document.addEventListener("DOMContentLoaded", () => {
    const headings = document.querySelectorAll(".text-display");
  
    const observer = new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
  
        const el        = entry.target;
        const effect    = el.dataset.anim;          // e.g. "rollIn" or "hinge"
        const animClass = `animate__${effect}`;
  
        el.classList.add("animate__animated", animClass);
        obs.unobserve(el);
      });
    }, {
      threshold: 0.2   // fire when 20% of the heading is visible
    });
  
    headings.forEach(h => observer.observe(h));
  });

  

//   handling stripe payment to handle the click
document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("checkout-button");
    if (!btn) return;
  
    btn.addEventListener("click", () => {
      btn.disabled = true;
      btn.textContent = "Redirecting…";
  
      fetch("/create-checkout-session", { method: "POST" })
        .then(res => res.json())
        .then(data => {
          if (data.sessionId) {
            return stripe.redirectToCheckout({ sessionId: data.sessionId });
          }
          throw new Error("No sessionId returned");
        })
        .catch(err => {
          console.error(err);
          alert("Failed to start checkout.");
          btn.disabled = false;
          btn.textContent = "Proceed to Checkout";
        });
    });
  });

  

//   search bar functionality with a littile bit of autocomplete
const input = document.querySelector('input[name="q"]');
const list  = document.createElement('ul');
list.className = 'autocomplete-list';
input.parentNode.append(list);

let timer;
input.addEventListener('input', () => {
  clearTimeout(timer);
  const q = input.value.trim();
  if (!q) { list.innerHTML = ''; return; }
  timer = setTimeout(() => {
    fetch(`/api/suggest?q=${encodeURIComponent(q)}`)
      .then(r => r.json())
      .then(suggestions => {
        list.innerHTML = suggestions
          .map(item => `<li class="suggest-item">${item}</li>`)
          .join('');
      });
  }, 200);
});

// when user clicks one suggestion, fill and submit
list.addEventListener('click', e => {
  if (e.target.matches('.suggest-item')) {
    input.value = e.target.textContent;
    input.form.submit();
  }
});

