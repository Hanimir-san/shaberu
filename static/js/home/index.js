function delayFunction(callback, ms) {
    let timer = 0;
    return function() {
    const context = this, args = arguments;
      clearTimeout(timer);
      timer = setTimeout(function () {
        callback.apply(context, args);
      }, ms || 0);
    };
  }

function loadChatResponse() {
    console.log('hello');
}

document.getElementById("chat-input-main").addEventListener("keyup", delayFunction(loadChatResponse, 2000)); 