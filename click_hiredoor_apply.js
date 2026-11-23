async (page) => {
  const result = await page.evaluate(() => {
    const applyBtns = Array.from(document.querySelectorAll('button, a')).filter(b => (b.innerText || '').trim() === 'Apply Now');
    if (applyBtns.length > 0) {
      applyBtns[0].click();
      return { clicked: true, tag: applyBtns[0].tagName, href: applyBtns[0].href || null };
    }
    return { clicked: false };
  });

  await page.waitForTimeout(3000);

  const afterClick = await page.evaluate(() => {
    return {
      url: window.location.href,
      modalText: document.body.innerText.slice(0, 600)
    };
  });

  return { result, afterClick };
}
