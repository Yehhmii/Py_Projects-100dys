document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('uploadForm');
  const overlay = document.getElementById('overlay');
  const audioPlayer = document.getElementById('audioPlayer');
  const downloadBtn = document.getElementById('downloadBtn');
  const fileInput = form.querySelector('input[name="pdf"]');

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    // Show processing overlay
    overlay.style.display = 'flex';
    audioPlayer.style.display = 'none';
    downloadBtn.style.display = 'none';

    const formData = new FormData(form);
    fetch(form.action, {
      method: 'POST',
      body: formData
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Conversion failed');
      }
      return response.blob();
    })
    .then(blob => {
      // Hide overlay
      overlay.style.display = 'none';

      // Create object URL for audio
      const url = URL.createObjectURL(blob);
      audioPlayer.src = url;
      audioPlayer.style.display = 'block';

      // Prepare download button
      const originalName = fileInput.files[0].name;
      const baseName = originalName.replace(/\.[^/.]+$/, "");
      downloadBtn.href = url;
      downloadBtn.download = baseName + '.mp3';
      downloadBtn.style.display = 'inline-block';
    })
    .catch(err => {
      overlay.style.display = 'none';
      alert('Error: ' + err.message);
    });
  });
});
