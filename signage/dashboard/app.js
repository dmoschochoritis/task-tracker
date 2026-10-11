const API = location.origin.replace("5500", "8000");

async function playlistName(screenId) {
  const res = await fetch(`${API}/screens/${screenId}/playlist`);
  if (res.status === 404) return "no playlist";
  return (await res.json()).name;
}

async function loadScreens() {
  const screens = await (await fetch(`${API}/screens`)).json();
  const list = document.getElementById("screens");
  list.innerHTML = "";
  for (const s of screens) {
    const li = document.createElement("li");
    li.textContent = `${s.name} (${s.location}): ${await playlistName(s.id)}`;
    list.appendChild(li);
  }
}

loadScreens();
