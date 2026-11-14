(() => {
  // Load the design capture tool only when explicitly opened with a local capture URL.
  if (['localhost', '127.0.0.1', '[::1]'].includes(location.hostname) && location.hash.includes('figmacapture=')) {
    const capture = document.createElement('script');
    capture.src = 'https://mcp.figma.com/mcp/html-to-design/capture.js';
    capture.async = true;
    document.head.appendChild(capture);
  }
  const menu = document.getElementById('menuToggle');
  const nav = document.getElementById('mainNav');
  const closeMenu = () => { if (!menu) return; menu.setAttribute('aria-expanded', 'false'); nav.classList.remove('is-open'); };
  menu?.addEventListener('click', () => { const open = menu.getAttribute('aria-expanded') !== 'true'; menu.setAttribute('aria-expanded', String(open)); nav.classList.toggle('is-open', open); });
  document.addEventListener('keydown', event => { if (event.key === 'Escape' && menu?.getAttribute('aria-expanded') === 'true') { closeMenu(); menu.focus(); } });
  document.addEventListener('click', event => { if (!event.target.closest('.header-inner')) closeMenu(); });
  nav?.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
  const video = document.getElementById('heroVideo');
  const videoButton = document.getElementById('videoToggle');
  if (video && videoButton) {
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    const syncVideo = () => { videoButton.textContent = video.paused ? 'Reproducir video' : 'Pausar video'; videoButton.setAttribute('aria-pressed', String(!video.paused)); };
    const playVideo = async () => { if (!video.querySelector('source').src) { video.querySelector('source').src = video.querySelector('source').dataset.src; video.load(); } try { await video.play(); } catch { syncVideo(); } };
    video.addEventListener('play', syncVideo); video.addEventListener('pause', syncVideo);
    videoButton.addEventListener('click', () => video.paused ? playVideo() : video.pause());
    if (!reducedMotion.matches && !navigator.connection?.saveData) playVideo();
    reducedMotion.addEventListener('change', event => { if (event.matches) video.pause(); });
    document.addEventListener('visibilitychange', () => { if (document.hidden) video.pause(); });
  }
  document.querySelectorAll('.machine-video').forEach(container => {
    const preview = container.querySelector('.video-preview');
    const frame = container.querySelector('iframe');
    if (!preview || !frame) return;
    try {
      const url = new URL(frame.dataset.src);
      const id = url.pathname.match(/^\/embed\/([a-zA-Z0-9_-]{11})$/)?.[1];
      if (['www.youtube.com', 'youtube.com', 'www.youtube-nocookie.com'].includes(url.hostname) && id) {
        const image = document.createElement('img');
        image.src = `https://i.ytimg.com/vi/${id}/hqdefault.jpg`;
        image.alt = ''; image.loading = 'lazy'; image.width = 480; image.height = 360;
        image.addEventListener('error', () => image.remove());
        preview.prepend(image);
      }
    } catch {}
    preview.addEventListener('click', event => {
      event.preventDefault(); frame.src = frame.dataset.src; frame.hidden = false;
      preview.hidden = true; frame.tabIndex = 0; frame.focus();
    });
  });
  const display = document.getElementById('timerDisplay');
  if (!display) return;
  const start = document.getElementById('startTimerBtn');
  const reset = document.getElementById('resetTimerBtn');
  const status = document.getElementById('timerStatus');
  const presets = document.querySelectorAll('[data-time]');
  let duration = 60, remaining = 60, deadline = 0, interval = null;
  const render = () => { const seconds = Math.ceil(remaining); display.textContent = `${String(Math.floor(seconds / 60)).padStart(2, '0')}:${String(seconds % 60).padStart(2, '0')}`; };
  const stop = () => { clearInterval(interval); interval = null; };
  let audio;
  const beep = () => { if (!audio) return; const oscillator = audio.createOscillator(); const gain = audio.createGain(); oscillator.connect(gain); gain.connect(audio.destination); oscillator.frequency.value = 880; gain.gain.setValueAtTime(.15, audio.currentTime); gain.gain.exponentialRampToValueAtTime(.001, audio.currentTime + .4); oscillator.start(); oscillator.stop(audio.currentTime + .4); };
  const tick = () => { remaining = Math.max(0, (deadline - Date.now()) / 1000); render(); if (remaining === 0) { stop(); start.textContent = 'Iniciar descanso'; status.textContent = 'Descanso terminado. Puedes iniciar otro intervalo.'; beep(); } };
  start.addEventListener('click', () => {
    if (interval !== null) { remaining = Math.max(0, (deadline - Date.now()) / 1000); stop(); render(); start.textContent = 'Continuar'; status.textContent = 'Temporizador en pausa.'; return; }
    try { audio ||= new (window.AudioContext || window.webkitAudioContext)(); audio.resume().catch(() => {}); } catch {}
    if (remaining <= 0) remaining = duration;
    deadline = Date.now() + remaining * 1000; start.textContent = 'Pausar'; status.textContent = 'Descanso en curso.'; interval = setInterval(tick, 200); tick();
  });
  const resetTimer = () => { stop(); remaining = duration; render(); start.textContent = 'Iniciar descanso'; status.textContent = 'Listo para iniciar el descanso.'; };
  reset.addEventListener('click', resetTimer);
  presets.forEach(button => { button.setAttribute('aria-pressed', String(Number(button.dataset.time) === duration)); button.addEventListener('click', () => { duration = Number(button.dataset.time); presets.forEach(preset => { const selected = preset === button; preset.classList.toggle('active', selected); preset.setAttribute('aria-pressed', String(selected)); }); resetTimer(); }); });
})();
