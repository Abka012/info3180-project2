// 3-step verification checklist
// Run in browser console after: npm run dev

console.log('=== STEP 1: DOM Attribute Check ===');
const html = document.documentElement;
html.setAttribute('data-theme', 'dark');
console.log('✓ data-theme="dark" set:', html.getAttribute('data-theme') === 'dark');

console.log('\n=== STEP 2: Computed Style Check ===');
const computed = getComputedStyle(html);
console.log('--text-primary:', computed.getPropertyValue('--text-primary').trim());
console.log('--bg:', computed.getPropertyValue('--bg').trim());

console.log('\n=== STEP 3: Toggle Test ===');
html.setAttribute('data-theme', 'light');
const lightBg = getComputedStyle(html).getPropertyValue('--bg').trim();
html.setAttribute('data-theme', 'dark');
const darkBg = getComputedStyle(html).getPropertyValue('--bg').trim();
console.log('Light --bg:', lightBg);
console.log('Dark --bg:', darkBg);
console.log('✓ Theme switching works:', lightBg !== darkBg);
