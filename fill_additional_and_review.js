async (page) => {
  // Find all text / numeric inputs in the modal
  const result = await page.evaluate(() => {
    const modal = document.querySelector('.jobs-easy-apply-modal, [role="dialog"]') || document.body;
    const inputs = Array.from(modal.querySelectorAll('input[type="text"], input[type="number"], textarea'));
    
    let filled = [];
    inputs.forEach(input => {
      if (!input.value || input.value.trim() === '') {
        // Label check or default to 1
        const label = input.closest('div')?.innerText || '';
        input.value = "1";
        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
        filled.push({ label: label.slice(0, 50), value: "1" });
      } else {
        filled.push({ label: "already_filled", value: input.value });
      }
    });

    // Find review button
    const reviewBtn = Array.from(modal.querySelectorAll('button')).find(b => b.innerText && b.innerText.trim() === 'Review');
    if (reviewBtn) {
      reviewBtn.click();
      return { filled, clickedReview: true };
    }
    return { filled, clickedReview: false };
  });

  await page.waitForTimeout(1500);

  const finalSnippet = await page.evaluate(() => {
    const modalText = document.body.innerText;
    const match = modalText.match(/Apply to [^\n]+[\s\S]{1,600}/);
    return match ? match[0] : modalText.slice(0, 600);
  });

  return { result, finalSnippet };
}
