document.addEventListener("DOMContentLoaded", function () {
    const textElement = document.getElementById("typing-text");
    const textArray = ["Welcome to SSIT", "Constituent of SAHE", "NAAC accrideted A+"];
    let textIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    
    function typeEffect() {
        const currentText = textArray[textIndex];
        
        if (!isDeleting) {
            textElement.textContent = currentText.substring(0, charIndex + 1);
            charIndex++;
        } else {
            textElement.textContent = currentText.substring(0, charIndex - 1);
            charIndex--;
        }

        let typingSpeed = isDeleting ? 100 : 150; // Adjusting speed
        let delay = isDeleting ? 100 : 150; // Delay per letter

        if (!isDeleting && charIndex === currentText.length) {
            delay = 2000; // Wait time after full text is displayed
            isDeleting = true;
        } else if (isDeleting && charIndex === 0) {
            isDeleting = false;
            textIndex = (textIndex + 1) % textArray.length;
            delay = 1000; // Wait time before typing new text
        }

        setTimeout(typeEffect, delay);
    }

    typeEffect();
});
