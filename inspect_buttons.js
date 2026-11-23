async (page) => {
  await page.waitForTimeout(2000);
  const title = await page.title();
  const buttons = await page.$$eval('button', btns => btns.map(b => ({
    text: b.innerText.trim(),
    classes: b.className,
    ariaLabel: b.getAttribute('aria-label')
  })).filter(b => b.text || b.ariaLabel));

  const textSnippets = await page.evaluate(() => {
    return document.body.innerText.slice(0, 1000);
  });

  return { title, buttons: buttons.slice(0, 15), textSnippets: textSnippets.slice(0, 500) };
}
