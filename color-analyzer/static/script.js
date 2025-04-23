// Copy-to-clipboard for hex codes
document.querySelectorAll('.color-box').forEach(box => {
  box.addEventListener('click', () => {
    const hex = box.getAttribute('data-hex');
    // Use modern Clipboard API
    navigator.clipboard.writeText(hex).then(() => {
      // visual feedback
      box.classList.add('copied');
      setTimeout(() => box.classList.remove('copied'), 800);
    });
  });
});
