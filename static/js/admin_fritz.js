(() => {
  const password = document.querySelector('#login-form input[type="password"]');
  if (password) {
    const wrapper = document.createElement('div'); wrapper.className = 'admin-password-control';
    password.parentNode.insertBefore(wrapper, password); wrapper.append(password);
    const toggle = document.createElement('button'); toggle.type = 'button'; toggle.textContent = 'Mostrar';
    toggle.setAttribute('aria-controls', password.id); toggle.setAttribute('aria-pressed', 'false');
    toggle.setAttribute('aria-label', 'Mostrar contraseña');
    toggle.addEventListener('click', () => { const show = password.type === 'password'; password.type = show ? 'text' : 'password'; toggle.textContent = show ? 'Ocultar' : 'Mostrar'; toggle.setAttribute('aria-pressed', String(show)); toggle.setAttribute('aria-label', show ? 'Ocultar contraseña' : 'Mostrar contraseña'); });
    wrapper.append(toggle);
  }
  const form = document.querySelector('#maquina_form, #anuncio_form');
  if (form) {
    const status = document.createElement('span'); status.className = 'admin-save-status';
    status.setAttribute('role', 'status'); status.textContent = 'Sin cambios pendientes';
    document.querySelector('#content > h1')?.append(status);
    let dirty = false;
    form.addEventListener('input', () => { dirty = true; status.textContent = 'Cambios sin guardar'; status.classList.add('is-dirty'); });
    form.addEventListener('change', () => { dirty = true; status.textContent = 'Cambios sin guardar'; status.classList.add('is-dirty'); });
    form.addEventListener('submit', () => { dirty = false; });
    window.addEventListener('beforeunload', event => { if (dirty) { event.preventDefault(); event.returnValue = ''; } });
  }
  document.querySelectorAll('.errornote').forEach(note => { note.setAttribute('role', 'alert'); });
  const input = document.getElementById('id_url_video');
  const preview = document.getElementById('admin-video-preview');
  if (input && preview && !input.readOnly && !input.disabled) {
    let timeout;
    const parseVideo = value => {
      try {
        const url = new URL(value); if (url.protocol !== 'https:') return '';
        let id = '';
        if (['youtu.be', 'www.youtu.be'].includes(url.hostname)) id = url.pathname.slice(1);
        if (['youtube.com', 'www.youtube.com', 'm.youtube.com', 'youtube-nocookie.com', 'www.youtube-nocookie.com'].includes(url.hostname)) id = url.pathname === '/watch' ? url.searchParams.get('v') || '' : url.pathname.match(/^\/(?:embed|shorts)\/([^/]+)\/?$/)?.[1] || '';
        return /^[a-zA-Z0-9_-]{11}$/.test(id) ? id : '';
      } catch { return ''; }
    };
    const update = () => {
      preview.replaceChildren(); const id = parseVideo(input.value.trim());
      if (!id) { const text = document.createElement('p'); text.textContent = input.value.trim() ? 'Revisa el enlace: debe ser un video de YouTube con su identificador completo.' : 'Pega un enlace para ver la vista previa del tutorial.'; preview.append(text); return; }
      const image = document.createElement('img'); image.src = `https://i.ytimg.com/vi/${id}/hqdefault.jpg`; image.alt = 'Miniatura del tutorial'; image.width = 320; image.height = 180;
      image.addEventListener('error', () => { image.remove(); });
      const body = document.createElement('div'); const title = document.createElement('strong'); title.textContent = 'Tutorial vinculado';
      const description = document.createElement('p'); description.textContent = 'Comprueba que el ejercicio corresponde a esta máquina.';
      const link = document.createElement('a'); link.href = `https://www.youtube.com/watch?v=${id}`; link.target = '_blank'; link.rel = 'noopener noreferrer'; link.textContent = 'Ver en YouTube';
      body.append(title, description, link); preview.append(image, body);
    };
    input.addEventListener('input', () => { clearTimeout(timeout); timeout = setTimeout(update, 350); });
  }
})();
