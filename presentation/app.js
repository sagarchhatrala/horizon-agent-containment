const slides = Array.from(document.querySelectorAll(".slide"));
const current = document.getElementById("current");
const total = document.getElementById("total");
const slideTitle = document.getElementById("slideTitle");
const progress = document.getElementById("progress");
const prev = document.getElementById("prev");
const next = document.getElementById("next");
const full = document.getElementById("full");

let index = initialIndex();
total.textContent = String(slides.length);

function initialIndex() {
  const raw = window.location.hash.replace("#", "");
  const parsed = Number.parseInt(raw, 10);
  if (Number.isFinite(parsed) && parsed >= 1 && parsed <= slides.length) {
    return parsed - 1;
  }
  return 0;
}

function show(nextIndex, updateHash = true) {
  index = Math.max(0, Math.min(slides.length - 1, nextIndex));
  slides.forEach((slide, slideIndex) => {
    slide.classList.toggle("active", slideIndex === index);
    slide.setAttribute("aria-hidden", slideIndex === index ? "false" : "true");
  });

  current.textContent = String(index + 1);
  slideTitle.textContent = slides[index].dataset.title || "";
  progress.style.width = `${((index + 1) / slides.length) * 100}%`;
  prev.disabled = index === 0;
  next.disabled = index === slides.length - 1;

  if (updateHash) {
    history.replaceState(null, "", `#${index + 1}`);
  }
}

function go(delta) {
  show(index + delta);
}

prev.addEventListener("click", () => go(-1));
next.addEventListener("click", () => go(1));

full.addEventListener("click", async () => {
  try {
    if (!document.fullscreenElement) {
      await document.documentElement.requestFullscreen();
    } else {
      await document.exitFullscreen();
    }
  } catch {
    // Fullscreen can be blocked by browser policy. Navigation still works.
  }
});

window.addEventListener("keydown", (event) => {
  const tag = document.activeElement?.tagName;
  if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT") return;

  if (event.key === "ArrowRight" || event.key === "PageDown" || event.key === " ") {
    event.preventDefault();
    go(1);
  }
  if (event.key === "ArrowLeft" || event.key === "PageUp") {
    event.preventDefault();
    go(-1);
  }
  if (event.key === "Home") {
    event.preventDefault();
    show(0);
  }
  if (event.key === "End") {
    event.preventDefault();
    show(slides.length - 1);
  }
});

window.addEventListener("hashchange", () => {
  show(initialIndex(), false);
});

show(index, false);
