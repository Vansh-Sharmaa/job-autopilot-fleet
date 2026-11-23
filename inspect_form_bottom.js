async (page) => {
  const pageBottom = await page.evaluate(() => {
    const text = document.body.innerText;
    const checkboxes = Array.from(document.querySelectorAll('[role="checkbox"], [role="radio"], input')).map(el => ({
      type: el.getAttribute('role') || el.type,
      text: el.closest('div')?.innerText || '',
      checked: el.getAttribute('aria-checked') || el.checked
    }));
    return {
      lastText: text.slice(-800),
      checkboxes
    };
  });
  return pageBottom;
}
