function getPlayBackTime() {
  let videoElement = document.querySelector("video");
  return Math.round(videoElement.currentTime * 1000);
}

chrome.runtime.onMessage.addListener((request, sender, response) => {
  if (request.msg == "get_time") {
    let timeInSeconds = getPlayBackTime();
    response(timeInSeconds);
  }
});
