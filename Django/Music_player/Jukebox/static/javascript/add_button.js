document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.add_btn');
    const popups = document.querySelectorAll('.popup');
    const closeButtons = document.querySelectorAll('.closePopup');

    buttons.forEach((button, index) => {
        button.addEventListener('click', () => {
            popups[index].style.display = 'block';
        });
    });

    closeButtons.forEach((button, index) => {
        button.addEventListener('click', () => {
            popups[index].style.display = 'none';
        });
    });
});
