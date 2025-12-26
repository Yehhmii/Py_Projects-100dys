const textarea = document.getElementById('writer');
const countdownEl = document.getElementById('countdown');
const modal = document.getElementById('resultModal');
const finalText = document.getElementById('finalText');
const metricsP = document.getElementById('metrics');
const toLB = document.getElementById('toLeaderboard');

let startTime = Date.now();
let inactiveTimer, countdownTimer;
const TIMEOUT = 5000;
const COUNTDOWN_START = 3000;

// preload sounds
const countdownSound = new Audio('/static/countdown.mp3');
const timeoutSound   = new Audio('/static/timeout.mp3');

function resetTimers() {
  clearTimeout(inactiveTimer);
  clearInterval(countdownTimer);
  countdownEl.textContent = '';
  const now = Date.now();
  startTime = startTime; // unchanged
  inactiveTimer = setTimeout(beginCountdown, TIMEOUT - COUNTDOWN_START);
}

function beginCountdown() {
  let remaining = COUNTDOWN_START / 1000; // in s
  countdownSound.play();
  countdownEl.textContent = remaining.toFixed(0);
  countdownTimer = setInterval(() => {
    remaining -= 1;
    if (remaining > 0) {
      countdownEl.textContent = remaining.toFixed(0);
    } else {
      clearInterval(countdownTimer);
      doTimeout();
    }
  }, 1000);
}

function doTimeout() {
  timeoutSound.play();
  const text = textarea.value;
  const elapsed = Date.now() - startTime;
  fetch('/submit', {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({ text, elapsed })
  })
  .then(r => r.json())
  .then(m => {
    finalText.textContent = text;
    metricsP.textContent = `WPM: ${m.wpm}  Words: ${m.words}  Sentences: ${m.sentences}  Score: ${m.score}/100`;
    modal.style.display = 'flex';
  });
}

// start timers on load
textarea.addEventListener('input', resetTimers);
window.onload = () => resetTimers();

// go to leaderboard
toLB.addEventListener('click', () => {
  window.location.href = '/leaderboard';
});
