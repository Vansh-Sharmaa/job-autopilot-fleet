async (page) => {
  const btns = await page.evaluate(() => {
    return Array.from(document.querySelectorAll('[role="button"], button')).map(b => ({
      text: b.innerText.trim(),
      aria: b.getAttribute('aria-label'),
      classes: b.className
    })).filter(b => b.text || b.aria);
  });
  return btns;
}
