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
  const screenSelect = document.getElementById("assign-screen");
  screenSelect.innerHTML = "";
  for (const s of screens) {
    const li = document.createElement("li");
    li.textContent = `${s.name} (${s.location}): ${await playlistName(s.id)}`;
    list.appendChild(li);
    screenSelect.add(new Option(s.name, s.id));
  }
}

async function loadPlaylists() {
  const playlists = await (await fetch(`${API}/playlists`)).json();
  const select = document.getElementById("assign-playlist");
  select.innerHTML = "";
  for (const p of playlists) select.add(new Option(p.name, p.id));
}

document.getElementById("new-playlist").addEventListener("submit", async (e) => {
  e.preventDefault();

    const name = document.getElementById("pl-name").value;
  const items = document.getElementById("pl-items").value.split(",").map(i => i.trim());
  await fetch(`${API}/playlists`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ name, items }) });
  e.target.reset();
  await loadPlaylists();
});

document.getElementById("assign-btn").addEventListener("click", async () => {
  const screenId = document.getElementById("assign-screen").value;
  const playlistId = Number(document.getElementById("assign-playlist").value);
  await fetch(`${API}/screens/${screenId}/playlist`, { method: "PUT", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ playlist_id: playlistId }) });
  await loadScreens();
});

loadScreens();
loadPlaylists();
