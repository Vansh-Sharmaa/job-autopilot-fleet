async (page) => {
  // Find and click the Easy Apply button
  const easyBtn = await page.evaluate(() => {
    const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Easy Apply'));
    if (btn) {
      btn.click();
      return true;
    }
    return false;
  });

  if (!easyBtn) return { error: "No Easy Apply button found" };

  await page.waitForTimeout(2000);

  // Inspect the modal
  const modalInfo = await page.evaluate(() => {
    const modal = document.querySelector('.jobs-easy-apply-modal, [role="dialog"]');
    if (!modal) return { modalFound: false };
    
    const header = modal.querySelector('h2, h3, [id*="header"]');
    const headerText = header ? header.innerText.trim() : '';
    
    const inputs = Array.from(modal.querySelectorAll('input, select, textarea')).map(i => ({
      type: i.type,
      name: i.name || i.id,
      value: i.value,
      required: i.required
    }));

    const buttons = Array.from(modal.querySelectorAll('button')).map(b => b.innerText.trim()).filter(Boolean);

    return {
      modalFound: true,
      headerText,
      inputsCount: inputs.length,
      inputs,
      buttons
    };
  });

  return modalInfo;
}
