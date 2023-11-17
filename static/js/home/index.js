function delayFunction(ms, callback) {
  let timer = 0;
  return function() {
  const context = this, args = arguments;
    clearTimeout(timer);
    timer = setTimeout(function () {
      callback.apply(context, args);
    }, ms || 0);
  };
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

function getBaseUrl() {
   baseUrl = window.location.origin;
   return baseUrl;
}

function loadChatResponse() {
    console.log(this);
    const baseUrl = getBaseUrl();
    const endpointUrl = '/ajax/get-chat-response/';
    const requestUrl = baseUrl + endpointUrl;
    const requestData = new FormData(this.form);
    const csrfToken = getCookie('csrftoken');
    const requestHeader = {
      // 'Content-Type': 'multipart/form-data',
      "X-Requested-With": "XMLHttpRequest",
      'X-CSRFTOKEN': csrfToken
    }

    console.log(requestUrl);
    console.log(csrfToken)

    const response = fetch(requestUrl, {
      method: "POST",
      mode: "cors",
      cache: "no-cache",
      credentials: "same-origin",
      headers: requestHeader,
      redirect: "follow",
      referrerPolicy: "no-referrer",
      body: requestData,
    }).then(function(data) {
      console.log(data);
    });
}

document.getElementById("chat-input-main").addEventListener("keyup", delayFunction(700, loadChatResponse)); 