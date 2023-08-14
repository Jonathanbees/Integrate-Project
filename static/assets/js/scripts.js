document.addEventListener('DOMContentLoaded', function () {
    const profileIcon = document.getElementById('profile-icon');
    const profileMenu = document.getElementById('profile-menu');
    const cartIcon = document.getElementById('cart-icon');
    const cartMenu = document.getElementById('cart-menu');
    //eventos menu profile
    profileIcon.addEventListener('click', function () {
        profileMenu.style.display = (profileMenu.style.display === 'block') ? 'none' : 'block';
    });

    window.addEventListener('click', function (event) {
        if (!profileIcon.contains(event.target) && !profileMenu.contains(event.target)) {
            profileMenu.style.display = 'none';
        }
    });
    //eventos menu carrito
    cartIcon.addEventListener('click', function () {
        cartMenu.style.display = (cartMenu.style.display === 'block') ? 'none' : 'block';
    });

    window.addEventListener('click', function (event) {
        if (!cartIcon.contains(event.target) && !cartMenu.contains(event.target)) {
            cartMenu.style.display = 'none';
        }
    });
});






