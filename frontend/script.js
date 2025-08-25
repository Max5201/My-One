async function getMessage() {
  const res = await fetch('https://storied-souffle-48614e.netlify.app/');
  const data = await res.json();
  document.getElementById('response').innerText = data.message;
}
