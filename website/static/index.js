function deleteOrder(orderId) {
  if( confirm("Are u confirm to remove it from cart?")) {
      fetch("/delete-order", {
        method: "POST",
        body: JSON.stringify({ orderId: orderId }),
      }).then((_res) => {
        window.location.href = "/products";
      });
  }
}
