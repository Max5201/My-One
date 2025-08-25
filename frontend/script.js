async function getMessage() {
  const res = await fetch('https://你的后端域名/message');
  const data = await res.json();
  document.getElementById('response').innerText = data.message;
}
