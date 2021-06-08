let titleInput = document.querySelector("#title");
let startInput = document.querySelector("#start-input");
let endInput = document.querySelector("#end-input");
let startBtn = document.querySelector("#start");
let endBtn = document.querySelector("#end");
let submitBtn = document.querySelector("#submit");

let videoId = "";

startBtn.addEventListener("click", () => {  
  getAndSetInput(startInput);
});

endBtn.addEventListener("click", () => {  
  getAndSetInput(endInput);
});

submitBtn.addEventListener("click", () => {  
  let data = {
    cstart: startInput.value,
    cend: endInput.value,
    title: titleInput.value,
    cID: videoId,
  };

  var params = new URLSearchParams(data);
    
  fetch(`http://flask-env.eba-tt8quthp.us-west-2.elasticbeanstalk.com/newclip?${params.toString()}`)
  .then(res => res.json())
  .then(result => console.log(result) )
});

function getAndSetInput(el) {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    let url = new URL(tabs[0].url);
    videoId = url.searchParams.get("v");
    chrome.tabs.sendMessage(
      tabs[0].id,
      { msg: "get_time" },
      (value) => (el.value = value)
    );
  });
}
