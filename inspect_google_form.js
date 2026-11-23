async (page) => {
  const data = await page.evaluate(() => {
    const text = document.body.innerText;
    const inputs = Array.from(document.querySelectorAll('input, textarea')).map(i => ({
      name: i.name,
      type: i.type,
      ariaLabel: i.getAttribute('aria-label'),
      value: i.value
    }));
    return { text: text.slice(0, 1500), inputs };
  });
  return data;
}
