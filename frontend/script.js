async function getMessage() {
  const res = await fetch('https://your-backend-name.onrender.com/message');
  const data = await res.json();
  document.getElementById('response').innerText = `${data.text} (${data.created_at})`;
}
