var form = document.getElementById("upload-form");
var fileInput = document.getElementById("pdf-input");

//Listening for a newly added file
fileInput.onchange = function () {
  file = new FileReader();
  var displayer = document.getElementById('filename-display');
  //Check if there's a file added
  try {
    file.readAsBinaryString(fileInput.files[0]);
    //If there is a file then show the name of it
    console.log(fileInput.files[0].name);
    displayer.innerText = fileInput.files[0].name;
  } catch {
    displayer.innerText = 'No file selected';
    return;
  }
};

//Waiting for the form to be submitted
form.addEventListener("submit", async function (event) {
  event.preventDefault();

  file = new FileReader();

  try {
    //If theres a file added don't show any warning
    file.readAsBinaryString(fileInput.files[0]);
    document.getElementById("no-file-warn").hidden = true;
  } catch {
    //If not, then make the warning visible
    document.getElementById("no-file-warn").hidden = false;
    return;
  }

  var downloadLink = document.getElementById("file-downloader");
  var loader = document.getElementById("converting-loader");
  loader.hidden = false;

  //Waiting for the file to load
  file.onload = async function () {
    //Creating the url for the request
    var url = new URL(location.origin + "/convert_to_pdf");

    //Adding the binary to the form
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    //Sending the request with fetch
    var res = await fetch(url, { method: "POST", body: formData });

    //Creating a download link for the .zip file
    const file = await res.blob();
    const fileURL = URL.createObjectURL(file);

    loader.hidden = true;

    downloadLink.setAttribute("href", fileURL);
    downloadLink.setAttribute(
      "download",
      `${fileInput.files[0].name.slice(0, -4)}.zip`
    );
    downloadLink.hidden = false;
  };
});
