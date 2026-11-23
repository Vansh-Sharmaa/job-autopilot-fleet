async (page) => {
  const btnDetails = await page.evaluate(() => {
    const btn = Array.from(document.querySelectorAll('button')).find(b => (b.innerText || '').trim() === 'Apply Now');
    if (!btn) return null;
    return {
      outerHTML: btn.outerHTML,
      onclick: btn.getAttribute('onclick'),
      dataAttributes: Array.from(btn.attributes).map(a => `${a.name}="${a.value}"`)
    };
  });
  return btnDetails;
}
