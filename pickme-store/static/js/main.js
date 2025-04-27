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
  