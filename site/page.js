const lang = document.documentElement.lang;
const languageKey = 'videos-ia-enriqueite.site.language';
const en = lang === 'en';
if (!en) {
  let choice;
  try { choice = localStorage.getItem(languageKey); } catch {}
  choice ||= (navigator.languages || [navigator.language]).map(tag => tag.split('-')[0]).find(code => code === 'en' || code === 'es');
  if (choice === 'en') location.replace('en/index.html' + location.search + location.hash);
}
document.querySelectorAll('[data-language]').forEach(link => link.addEventListener('click', () => {
  try { localStorage.setItem(languageKey, link.dataset.language); } catch {}
}));
const topic = document.querySelector('#topic');
const prompt = document.querySelector('#prompt');
function renderBrief() {
  const subject = topic.value.trim() || (en ? '[your topic]' : '[tu tema]');
  const vertical = document.querySelector('input[name=format]:checked').value === 'reel';
  prompt.textContent = en
    ? 'Use the videos-ia-enriqueite skill to plan a ' + (vertical ? 'vertical short' : 'landscape YouTube video') + ' about “' + subject + '”. Suggest sources and wait for my approval of the script before producing the scenes.'
    : 'Usa la skill videos-ia-enriqueite para preparar un ' + (vertical ? 'reel vertical' : 'vídeo horizontal de YouTube') + ' sobre «' + subject + '». Propón fuentes y espera mi aprobación del guion antes de producir las escenas.';
  document.querySelector('.composer .status').textContent = '';
}
document.querySelector('.composer').addEventListener('input', renderBrief);
renderBrief();
document.querySelectorAll('[data-copy]').forEach(button => {
  button.hidden = false;
  button.addEventListener('click', async () => {
    const source = document.getElementById(button.dataset.copy);
    const status = button.nextElementSibling;
    try {
      await navigator.clipboard.writeText(source.textContent);
      status.textContent = en ? 'Copied.' : 'Copiado.';
    } catch {
      const range = document.createRange();
      range.selectNodeContents(source);
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      status.textContent = en ? 'Text selected. Use Copy.' : 'Texto seleccionado. Usa Copiar.';
    }
  });
});
