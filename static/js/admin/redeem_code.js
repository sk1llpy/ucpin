document.addEventListener('DOMContentLoaded', function() {
    let container = document.getElementById("changelist-form");
    let button = document.createElement("a");

    button.textContent = "Create Many";
    button.style.justifyContent = 'center';
    button.style.padding = "12px";
    button.style.paddingLeft = "110px";
    button.style.paddingRight = "110px";
    button.style.backgroundColor = "#9333EA";
    button.style.color = "white";
    button.style.borderRadius = "10px";
    button.style.textAlignLast = "center";
    button.style.fontWeight = "600";
    button.href = "/admin/shop/redeemcode/add/many/";

    container.appendChild(button);
});
