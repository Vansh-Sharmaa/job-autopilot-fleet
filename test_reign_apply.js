async (page) => {
  const easyBtn = await page.evaluate(() => {
    const btn = Array.from(document.querySelectorAll('button')).find(b => {
      const t = (b.innerText || '').trim();
      return t.includes('Easy Apply');
    });
    if (btn) {
      btn.click();
      return true;
    }
    return false;
  });

  await page.waitForTimeout(2000);

  const modalText = await page.evaluate(() => {
    const modal = document.querySelector('.jobs-easy-apply-modal, [role="dialog"]') || document.body;
    return modal.innerText.slice(0, 600);
  });

  return { clicked: easyBtn, modalText };
}
