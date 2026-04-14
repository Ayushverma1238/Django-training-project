function getCSRFToken() {
  return document.cookie
    .split("; ")
    .find((row) => row.startsWith("csrftoken"))
    ?.split("=")[1];
}

function updateCount(id) {
  let el = document.querySelector(id);
  el.innerHTML = parseInt(el.innerHTML) + 1;
}

function addToCart(id) {
  fetch(`/add-to-cart/${id}/`, {
    method: "POST", // ✅ FIXED (not GET)
    headers: {
      "X-CSRFToken": getCSRFToken(),
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Failed request");
      }
      return response.json();
    })
    .then((data) => {
      if (data.status === "success") {
        updateCount("#totalBag");
        alert(`✅ Added! Quantity: ${data.quantity}`);
      } else {
        alert(data.error || "Something went wrong");
      }
    })
    .catch((error) => console.error("Error:", error));
}

function addToWishlist(id) {
  fetch(`/add-to-wishlist/${id}/`, {
    method: "GET",
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.status === "added") {
        updateCount("#totalWishlist");
        alert("❤️ Item added to wishlist");
      }
    })
    .catch((error) => console.error("Error:", error));
}

function removeFromWishlist(id) {
  if (!confirm("Are you sure?")) return;

  fetch(`/remove-wishlist/${id}/`, {
    method: "GET", // keep GET for simplicity
  })
    .then((res) => res.json())
    .then((data) => {
      location.reload();
    });
}

function removeFromCart(id) {
  if (!confirm("Are you sure?")) return;

  fetch(`/remove_from_cart/${id}`, {
    method: "GET",
  })
    .then((res) => res.json())
    .then((data) => {
      location.reload();
    })
    .catch((err) => console.error("Error removing from cart", err));
}

function moveToWishlist(id) {
  removeFromCart(id);
  addToWishlist(id);
}

function updateQty(id, qty) {
  fetch(`/update-cart-qty/?id=${id}&qty=${qty}`)
    .then((res) => res.json())
    .then((data) => {
      // Update full cart totals
      document.getElementById("total_mrp").innerText = "₹" + data.total_mrp;
      document.getElementById("discount").innerText = "-₹" + data.discount;
      delivery = 50;
      if (data.total_mrp >= 500) {
        delivery = 0;
      }
      document.querySelector("#delivery").innerText =
        delivery === 0 ? "FREE" : `+ ₹${delivery}`;
      data.total -= delivery;
      document.getElementById("total").innerText = "₹" + data.total;

      // ✅ Update THIS item subtotal
      document.getElementById(`item_total_${id}`).innerText =
        "₹" + data.item_total;
    });
}
