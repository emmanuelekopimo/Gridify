const openInputField = document.querySelector(".zip-file");
const openInputButton = document.querySelector(".choose-button");
const printButton = document.querySelector(".print-button");

function onWindowClose() {
  Neutralino.app.exit();
}

const openZipFile = async () => {
  let entries = await Neutralino.os.showOpenDialog("Open a zip file", {
    multiSelections: false,
    filters: [{ name: "Zip Archive", extensions: ["zip"] }],
  });
  openInputField.value = entries[0] === undefined ? "" : entries[0];
};

const render = async () => {
  if (openInputField.value.length == 0) {
    return;
  }
  let process = await Neutralino.os.spawnProcess(
    `"main/main.exe"  "${openInputField.value}"`
  );
};

Neutralino.init();

Neutralino.events.on("windowClose", onWindowClose);

openInputButton.addEventListener("click", () => {
  openZipFile();
});

printButton.addEventListener("click", () => {
  render();
});
