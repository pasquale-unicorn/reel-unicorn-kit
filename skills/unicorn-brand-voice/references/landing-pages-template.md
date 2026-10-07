# LANDING PAGES — Template e specifiche tecniche Unicorn
**Stack:** HTML + Tailwind CSS CDN + Lucide Icons + Montserrat (Google Fonts)
**Deploy:** File HTML completo importato in Go High Level
**Modal/Form:** GHL widget iframe embed oppure modal interno con iframe a `https://secure.unicorn-italia.com/widget/form/[ID]`

---

## STACK TECNICO OBBLIGATORIO

```html
<!-- SEMPRE in <head> — in questo ordine -->
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<script src="https://cdn.tailwindcss.com"></script>
<script src="https://unpkg.com/lucide@latest"></script>

<!-- Tailwind config custom — SEMPRE incluso -->
<script>
tailwind.config = {
  theme: {
    extend: {
      fontFamily: { sans: ['Montserrat', 'sans-serif'] },
      backgroundImage: {
        'unicorn-gradient': 'linear-gradient(to right, #06b6d4, #9333ea)',
      },
      animation: {
        'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'fade-in-up': 'fadeInUp 0.8s ease-out forwards',
      },
      keyframes: {
        fadeInUp: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        }
      }
    }
  }
}
</script>

<!-- CSS custom base -->
<style>
  body { font-family: 'Montserrat', sans-serif; overflow-x: hidden; }
  html { scroll-behavior: smooth; }
  .no-scrollbar::-webkit-scrollbar { display: none; }
  .no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
</style>
```

---

## IDENTITÀ VISIVA (da applicare in tutte le landing)

### Palette
- **Sfondo hero:** `bg-black` con `bg-purple-900/40` blur glow
- **Gradiente brand:** `from-cyan-500 to-purple-600` (ciano → viola)
- **Gradiente testo headline:** `text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-white to-purple-500`
- **Sezioni alternate:** `bg-black` e `bg-white text-black` (schema chiaro/scuro a blocchi)
- **Sezione CTA finale:** `bg-gradient-to-br from-cyan-900 via-black to-purple-900`
- **Card su nero:** `bg-gray-900/50 border border-gray-800 rounded-3xl`
- **Card su bianco:** `bg-white rounded-2xl shadow-xl border-t-4 border-[COLOR]`

### Logo
- URL: `https://assets.cdn.filesafe.space/PGqnJfdWUQKvCuZQDmPU/media/b4f5e860-1466-4a8e-8591-2db13fa1a3da.png`
- Dimensione: `h-8 md:h-12`
- Posizione: header top-left (hidden su mobile nella maggior parte delle landing)

### Angelo — foto da usare nelle landing
- Foto principale (formato hero): `https://storage.googleapis.com/msgsndr/PGqnJfdWUQKvCuZQDmPU/media/6936eaa451010872ae5e0062.webp`
- Foto evento/palco: `https://storage.googleapis.com/msgsndr/PGqnJfdWUQKvCuZQDmPU/media/6936e99f4b202f19e8b5a838.webp`
- Workshop hero: `https://storage.googleapis.com/msgsndr/PGqnJfdWUQKvCuZQDmPU/media/6980c1d23c458e61a9cda689.webp`

### Tipografia
- **Font:** Montserrat in tutto
- **Headline principale:** `font-black uppercase tracking-tighter leading-[1.1]`
- **Taglia headline:** `text-3xl sm:text-4xl md:text-5xl lg:text-6xl` (aggiustare per tipo landing)
- **Subheadline:** `font-medium text-gray-300` su nero / `font-medium text-gray-700` su bianco
- **Body:** `text-lg sm:text-xl font-medium leading-relaxed`
- **CTA button testo:** `font-black uppercase tracking-widest`

---

## COMPONENTI RIUTILIZZABILI

### CTA Button principale (gradient)
```html
<button onclick="openModal()" class="w-full bg-gradient-to-r from-cyan-500 to-purple-600 text-white font-black uppercase text-xl py-5 px-8 rounded-xl hover:opacity-95 transition-transform active:scale-95 flex items-center justify-center shadow-[0_0_40px_rgba(168,85,247,0.5)] tracking-tight">
  TESTO CTA
</button>
```

### CTA Button pill (rounded-full — usato nel workshop)
```html
<button onclick="openModal()" class="pointer-events-auto w-full max-w-sm py-4 bg-gradient-to-r from-cyan-500 to-purple-600 text-white text-base font-black uppercase tracking-widest rounded-full shadow-[0_0_25px_rgba(147,51,234,0.6)] border border-white/20 active:scale-95 transition-all duration-200">
  TESTO CTA
</button>
```

### Gradient glow orb (sfondo hero)
```html
<div class="absolute top-[-20%] left-1/2 -translate-x-1/2 w-[70vw] h-[60vh] bg-purple-900/40 rounded-full blur-[100px] z-0 pointer-events-none mix-blend-screen animate-pulse"></div>
```

### Card feature (su sfondo nero)
```html
<div class="group">
  <div class="flex flex-col h-full bg-gray-900/50 rounded-3xl border border-gray-800 p-8 transition-all duration-500 hover:border-cyan-500/50 hover:shadow-[0_0_50px_rgba(6,182,212,0.15)] relative overflow-hidden">
    <!-- accent glow -->
    <div class="absolute -top-10 -right-10 w-32 h-32 bg-cyan-600/10 rounded-full blur-[40px] group-hover:bg-purple-500/10 pointer-events-none"></div>
    <!-- icon dot -->
    <div class="w-16 h-16 rounded-2xl bg-gradient-to-br from-gray-800 to-gray-900 border border-gray-700 flex items-center justify-center mb-6">
      <div class="w-8 h-8 bg-cyan-400 rounded-full opacity-50"></div>
    </div>
    <h3 class="font-black text-2xl mb-4 uppercase tracking-tight text-white group-hover:text-transparent group-hover:bg-clip-text group-hover:bg-gradient-to-r group-hover:from-cyan-300 group-hover:to-purple-400 transition-all">TITOLO</h3>
    <p class="text-gray-300 text-lg leading-relaxed mt-auto">Testo.</p>
  </div>
</div>
```

### Card testimonial (su sfondo bianco)
```html
<div class="bg-white rounded-2xl p-8 shadow-xl border-t-4 border-cyan-500 h-full flex flex-col justify-between hover:-translate-y-2 transition-transform duration-300">
  <p class="text-gray-700 text-lg italic mb-6 font-medium leading-relaxed">"Testo testimonial."</p>
  <p class="font-black text-gray-900 uppercase tracking-wider">- Nome (Ruolo)</p>
</div>
```

### Card "per chi è / per chi non è"
```html
<!-- PER CHI È -->
<div class="bg-white rounded-3xl p-8 sm:p-10 shadow-xl border-t-8 border-green-500">
  <h3 class="text-3xl font-black uppercase mb-8 text-gray-900">Questo è per te se:</h3>
  <ul class="space-y-6">
    <li class="flex items-start gap-4">
      <span class="flex-shrink-0 w-6 h-6 rounded-full bg-green-100 text-green-600 flex items-center justify-center font-bold text-sm mt-1">✓</span>
      <p class="text-lg font-medium text-gray-700">Punto</p>
    </li>
  </ul>
</div>
<!-- PER CHI NON È -->
<div class="bg-white rounded-3xl p-8 sm:p-10 shadow-xl border-t-8 border-red-500">
  <h3 class="text-3xl font-black uppercase mb-8 text-gray-900">Non è per te se:</h3>
  <ul class="space-y-6">
    <li class="flex items-start gap-4">
      <span class="flex-shrink-0 w-6 h-6 rounded-full bg-red-100 text-red-600 flex items-center justify-center font-bold text-sm mt-1">✗</span>
      <p class="text-lg font-medium text-gray-700">Punto</p>
    </li>
  </ul>
</div>
```

### Sticky CTA mobile (fixed bottom)
```html
<!-- MOBILE -->
<div class="fixed bottom-0 left-0 right-0 z-[100] p-4 sm:hidden bg-gradient-to-t from-black/95 to-transparent flex justify-center pointer-events-none">
  <button onclick="openModal()" class="pointer-events-auto w-full max-w-sm py-4 bg-gradient-to-r from-cyan-500 to-purple-600 text-white text-base font-black uppercase tracking-widest rounded-full shadow-[0_0_25px_rgba(147,51,234,0.6)] border border-white/20 active:scale-95 transition-all duration-200">
    TESTO CTA
  </button>
</div>
<!-- DESKTOP (appare sullo scroll) -->
<div id="desktop-sticky-cta" class="hidden sm:flex fixed bottom-8 left-0 right-0 mx-auto w-fit z-[100] transition-all duration-500 translate-y-20 opacity-0">
  <button onclick="openModal()" class="group flex items-center gap-3 px-8 py-4 bg-gradient-to-r from-cyan-600 to-purple-600 text-white text-lg font-black uppercase tracking-widest rounded-full shadow-[0_0_30px_rgba(147,51,234,0.4)] border-2 border-white/20 hover:scale-105 hover:shadow-[0_0_50px_rgba(147,51,234,0.8)] transition-all duration-300">
    TESTO CTA
    <i data-lucide="arrow-right" class="w-5 h-5 group-hover:translate-x-1 transition-transform"></i>
  </button>
</div>
```

### Modal con iframe GHL
```html
<style>
  .animate-fadeIn { animation: fadeIn 0.3s ease-out forwards; }
  @keyframes fadeIn { from { opacity: 0; transform: scale(0.95); } to { opacity: 1; transform: scale(1); } }
  #modal { display: none; }
  #modal.open { display: flex; }
</style>

<div id="modal" class="fixed inset-0 z-[9999] items-center justify-center p-4 sm:p-0" role="dialog" aria-modal="true">
  <div class="absolute inset-0 bg-black/90 backdrop-blur-md" onclick="closeModal()"></div>
  <div class="relative transform overflow-hidden rounded-2xl bg-white text-left shadow-2xl w-full max-w-lg h-[600px] animate-fadeIn">
    <button onclick="closeModal()" class="absolute right-3 top-3 z-50 rounded-full bg-white/80 p-2 text-gray-500 hover:text-black focus:outline-none backdrop-blur-sm">
      <span class="sr-only">Close</span>
      <span class="text-xl font-bold leading-none">&times;</span>
    </button>
    <div class="w-full h-full bg-white">
      <iframe src="[[GHL_FORM_URL]]" class="w-full h-full border-0" title="Modulo"></iframe>
    </div>
  </div>
</div>

<script>
function openModal() {
  document.getElementById('modal').classList.add('open');
  document.body.style.overflow = 'hidden';
}
function closeModal() {
  document.getElementById('modal').classList.remove('open');
  document.body.style.overflow = '';
}
document.addEventListener('keydown', function(e) { if (e.key === 'Escape') closeModal(); });
</script>
```

### Script sticky CTA desktop
```html
<script>
  window.addEventListener('scroll', () => {
    const el = document.getElementById('desktop-sticky-cta');
    if (!el) return;
    if (window.scrollY > 400) {
      el.classList.remove('translate-y-20', 'opacity-0');
      el.classList.add('translate-y-0', 'opacity-100');
    } else {
      el.classList.add('translate-y-20', 'opacity-0');
      el.classList.remove('translate-y-0', 'opacity-100');
    }
  });
  lucide.createIcons();
</script>
```

### FAQ Accordion
```html
<div class="space-y-6">
  <div class="bg-gray-50 p-6 sm:p-8 rounded-2xl border border-gray-200 shadow-sm hover:shadow-md transition-shadow">
    <h3 class="text-xl sm:text-2xl font-bold text-gray-900 mb-3">Domanda?</h3>
    <p class="text-lg text-gray-700 font-medium leading-relaxed">Risposta.</p>
  </div>
</div>
```

### Sezione "Chi è Angelo" (standard)
```html
<section class="bg-white text-black py-24 px-4">
  <div class="max-w-6xl mx-auto">
    <div class="flex flex-col md:flex-row items-center gap-12">
      <div class="w-full md:w-1/2 relative">
        <div class="absolute inset-0 bg-gradient-to-tr from-cyan-500 to-purple-600 rounded-3xl transform rotate-3 scale-105 opacity-20 blur-lg"></div>
        <img src="[[FOTO_ANGELO]]" alt="Angelo Abate" class="relative w-full h-auto rounded-3xl shadow-2xl border border-gray-200 object-cover">
      </div>
      <div class="w-full md:w-1/2 flex flex-col">
        <h2 class="text-4xl sm:text-5xl font-black uppercase mb-2 tracking-tight">
          <span class="text-transparent bg-clip-text bg-gradient-to-r from-cyan-600 to-purple-600">Angelo Abate</span>
        </h2>
        <h3 class="text-2xl sm:text-3xl font-bold text-gray-700 mb-8">Imprenditore & Investitore</h3>
        <div class="space-y-6 text-gray-800 text-lg leading-relaxed mb-8 font-medium">
          [[BIO_TESTO]]
        </div>
        <div class="bg-gray-50 border-l-4 border-purple-600 p-6 rounded-r-2xl italic text-gray-800 text-lg font-bold shadow-sm">
          [[CITAZIONE_ANGELO]]
        </div>
      </div>
    </div>
  </div>
</section>
```

---

## STRUTTURA SEZIONI PER TIPO DI LANDING

### OPTIN PAGE (webinar / workshop / lezioni / VSL / challenge / quiz)
1. Hero — headline + data/ora + immagine + CTA
2. Problema — "ogni giorno ti fai questa domanda..."
3. Cosa scoprirai — grid 3-6 card su nero
4. Perché questa live è diversa
5. Chi è Angelo
6. Testimonial (3 card testo + 3 video YouTube)
7. Per chi è / per chi non è
8. CTA finale (sezione gradient)
9. FAQ
10. Footer
11. Sticky CTA (mobile bottom, desktop scroll)
12. Modal GHL

### SALES PAGE (evento / prodotto high ticket)
1. Hero — nome evento + data + luogo + countdown + CTA acquisto
2. Problema amplificato
3. La trasformazione promessa
4. Cosa succederà (programma dei giorni / delle serate)
5. Chi parlerà (Angelo + eventuali altri speaker)
6. Cosa imparerai — lista dettagliata
7. Chi è Angelo
8. Testimonial (3 testo + 3 video)
9. Cosa è incluso (bonus, materiali, accesso)
10. Per chi è / per chi non è
11. Garanzia (se presente)
12. CTA acquisto principale
13. FAQ
14. Footer
15. Sticky CTA

### THANK YOU PAGE
1. Header logo
2. Headline: "Sei dentro! / Complimenti!"
3. Istruzioni passo per passo (cosa fare adesso: controlla email, aggiungi al calendario, unisciti al gruppo Telegram se presente)
4. Breve video di Angelo (ringraziamento / anticipazione)
5. Social sharing (opzionale)
6. Footer

---

## VARIABILI DA SOSTITUIRE AD OGNI LANDING

Quando produco una landing, le variabili tra `[[DOPPIE_QUADRE]]` devono essere sostituite con i dati del funnel specifico:

| Variabile | Descrizione |
|---|---|
| `[[TITOLO_EVENTO]]` | Nome del webinar/workshop/evento |
| `[[DATA_ORA]]` | Es. "24 marzo ore 21:00" |
| `[[LUOGO]]` | Solo per eventi fisici |
| `[[GHL_FORM_URL]]` | URL iframe form GHL |
| `[[FOTO_ANGELO]]` | URL foto Angelo appropriata |
| `[[HEADLINE_PRINCIPALE]]` | Headline hero — max 8 parole |
| `[[SUBHEADLINE]]` | 1-2 righe sotto la headline |
| `[[CTA_TEXT]]` | Testo del bottone CTA |
| `[[BIO_TESTO]]` | Paragrafi bio Angelo (2 paragrafi standard) |
| `[[CITAZIONE_ANGELO]]` | Quote virgolettata di Angelo |
| `[[COSA_SCOPRIRAI_1-6]]` | Titolo + testo delle 6 card feature |
| `[[PER_CHI_E_1-5]]` | 5 punti "per chi è" |
| `[[NON_PER_CHI_1-4]]` | 4 punti "non è per te se" |
| `[[TESTIMONIAL_1-3]]` | Testo + nome testimonial |
| `[[VIDEO_YT_1-3]]` | URL embed YouTube testimonial |
| `[[FAQ_1-6]]` | Domanda + risposta FAQ |
| `[[PREZZO]]` | Solo per sales page |

---

## REGOLE OPERATIVE

1. **Ogni bottone CTA chiama `openModal()`** — non link diretti, sempre modal
2. **Il modal contiene un iframe** all'URL GHL del form specifico del funnel
3. **Sticky CTA sempre presente** — mobile fixed bottom + desktop scroll-triggered
4. **Lucide icons** inizializzate con `lucide.createIcons()` a fine body
5. **Nessun replay** menzionato nelle optin — usare "Nessun replay pubblico" o "Solo live"
6. **Sezioni alternate chiaro/scuro** — hero nero → sezione bianca → sezione nera → sezione bianca → CTA gradiente → footer nero
7. **Max-width contenuto:** `max-w-7xl` per grids, `max-w-5xl` per testo, `max-w-4xl` per sezioni strette
8. **Border radius card:** `rounded-3xl` per card grandi, `rounded-2xl` per card medie, `rounded-xl` per elementi small
