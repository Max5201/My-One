async function getMessage() {
  const res = await fetch('https://my-one-fxkn.onrender.com/message');
  const data = await res.json();
  document.getElementById('response').innerText = data.message || data.text;
}
