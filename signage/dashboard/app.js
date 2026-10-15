const API = location.origin.replace("5500", "8000");
const DOWN = "Cannot reach the signage API. Check that it is running and try again.";

function showError(msg) {
  document.getElementById("error").textContent = msg;
}

async function api(path, options) {
  const res = await fetch(`${API}${path}`, options);
  if (!res.ok) throw new Error(`The API returned error ${res.status}.`);
  return res;
}

async function playlistName(screenId) {
  const playlist = await (await api(`/screens/${screenId}/playlist`)).json();
  return playlist ? playlist.name : "no playlist";
}

async function loadScreens() {
  const screens = await (await api("/screens")).json();
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
  const playlists = await (await api("/playlists")).json();
  const select = document.getElementById("assign-playlist");
  select.innerHTML = "";
  for (const p of playlists) select.add(new Option(p.name, p.id));
}

async function run(action) {
  try {
    await action();
    showError("");
  } catch (err) {
    showError(err instanceof TypeError ? DOWN : err.message);
  }
}

document.getElementById("new-playlist").addEventListener("submit", (e) => {
  e.preventDefault();
  run(async () => {
    const name = document.getElementById("pl-name").value;
    const items = document.getElementById("pl-items").value.split(",").map(i => i.trim());
    await api("/playlists", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ name, items }) });
    e.target.reset();
    await loadPlaylists();
  });
});

document.getElementById("assign-btn").addEventListener("click", () => {
  run(async () => {
    const screenId = document.getElementById("assign-screen").value;
    const playlistId = Number(document.getElementById("assign-playlist").value);
    await api(`/screens/${screenId}/playlist`, { method: "PUT", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ playlist_id: playlistId }) });
    await loadScreens();
  });
});

run(async () => {
  await loadScreens();
  await loadPlaylists();
});
