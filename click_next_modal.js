async (page) => {
  // Find button with text 'Next'
  const nextBtn = await page.evaluate(() => {
    const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.trim() === 'Next');
    if (btn) {
      btn.click();
      return true;
    }
    return false;
  });

  await page.waitForTimeout(1500);

  const snippet = await page.evaluate(() => {
    const modalText = document.body.innerText;
    const match = modalText.match(/Apply to [^\n]+[\s\S]{1,600}/);
    return match ? match[0] : modalText.slice(0, 600);
  });

  return { nextClicked: nextBtn, snippet };
}
