async (page) => {
  const submitInfo = await page.evaluate(() => {
    const modal = document.querySelector('.jobs-easy-apply-modal, [role="dialog"]') || document.body;
    const submitBtn = Array.from(modal.querySelectorAll('button')).find(b => b.innerText && b.innerText.trim().toLowerCase().includes('submit application'));
    
    if (!submitBtn) {
      const btns = Array.from(modal.querySelectorAll('button')).map(b => b.innerText.trim()).filter(Boolean);
      return { error: "No Submit application button found", buttons: btns };
    }

    submitBtn.click();
    return { clicked: true };
  });

  if (submitInfo.error) return submitInfo;

  await page.waitForTimeout(3000);

  const confirmation = await page.evaluate(() => {
    const pageText = document.body.innerText;
    const submitted = pageText.includes('Application sent') || pageText.includes('Your application was sent');
    
    // Close modal if dismiss/done button exists
    const dismissBtn = Array.from(document.querySelectorAll('button')).find(b => {
      const t = (b.innerText || b.getAttribute('aria-label') || '').toLowerCase();
      return t.includes('dismiss') || t.includes('done');
    });
    if (dismissBtn) dismissBtn.click();

    return { submitted, snippet: pageText.slice(0, 300) };
  });

  return confirmation;
}
