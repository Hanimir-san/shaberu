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

//API to handle audio recording
 
const audioRecorder = {
  /** Start recording the audio
    * @returns {Promise} - returns a promise that resolves if audio recording successfully started
    */
  /** Stores the recorded audio as Blob objects of audio data as the recording continues*/
  audioBlobs: [], /*of type Blob[]*/
  /** Stores the reference of the MediaRecorder instance that handles the MediaStream when recording starts*/
  mediaRecorder: null, /*of type MediaRecorder*/
  /** Stores the reference to the stream currently capturing the audio*/
  streamBeingCaptured: null, /*of type MediaStream*/
  start: function () {
    //Feature Detection
    if (!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia)) {
        //Feature is not supported in browser
        //return a custom error
        return Promise.reject(new Error('mediaDevices API or getUserMedia method is not supported in this browser.'));
      }
      else {
        //Feature is supported in browser
         
        //create an audio stream
        return navigator.mediaDevices.getUserMedia({ audio: true }/*of type MediaStreamConstraints*/)
            //returns a promise that resolves to the audio stream
            .then(stream /*of type MediaStream*/ => {
                 
                //save the reference of the stream to be able to stop it when necessary
                 audioRecorder.streamBeingCaptured = stream;

                //create a media recorder instance by passing that stream into the MediaRecorder constructor
                audioRecorder.mediaRecorder = new MediaRecorder(stream); /*the MediaRecorder interface of the MediaStream Recording
                API provides functionality to easily record media*/

                //clear previously saved audio Blobs, if any
                audioRecorder.audioBlobs = [];

                //add a dataavailable event listener in order to store the audio data Blobs when recording
                audioRecorder.mediaRecorder.addEventListener("dataavailable", event => {
                    //store audio Blob object
                    audioRecorder.audioBlobs.push(event.data);
                });

                //start the recording by calling the start method on the media recorder
                audioRecorder.mediaRecorder.start();
        });
    }
  },
  stop: function () {
    //return a promise that would return the blob or URL of the recording
    return new Promise(resolve => {
        //save audio type to pass to set the Blob type
        let mimeType = audioRecorder.mediaRecorder.mimeType;

        //listen to the stop event in order to create & return a single Blob object
        audioRecorder.mediaRecorder.addEventListener("stop", () => {
            //create a single blob object, as we might have gathered a few Blob objects that needs to be joined as one
            let audioBlob = new Blob(audioRecorder.audioBlobs, { type: mimeType });

            //resolve promise with the single audio blob representing the recorded audio
            resolve(audioBlob);
        });

    //stop the recording feature
    audioRecorder.mediaRecorder.stop();

    //stop all the tracks on the active stream in order to stop the stream
    audioRecorder.stopStream();

    //reset API properties for next recording
    audioRecorder.resetRecordingProperties();
    });
  },
  /** Cancel audio recording*/
  cancel: function () {
    //stop the recording feature
    audioRecorder.mediaRecorder.stop();

    //stop all the tracks on the active stream in order to stop the stream
    audioRecorder.stopStream();

    //reset API properties for next recording
    audioRecorder.resetRecordingProperties();
  },
  /** Stop all the tracks on the active stream in order to stop the stream and remove
   * the red flashing dot showing in the tab
   */
  stopStream: function() {
      //stopping the capturing request by stopping all the tracks on the active stream
      audioRecorder.streamBeingCaptured.getTracks() //get all tracks from the stream
              .forEach(track /*of type MediaStreamTrack*/ => track.stop()); //stop each one
  },
  /** Reset all the recording properties including the media recorder and stream being captured*/
  resetRecordingProperties: function () {
      audioRecorder.mediaRecorder = null;
      audioRecorder.streamBeingCaptured = null;

      /*No need to remove event listeners attached to mediaRecorder as
      If a DOM element which is removed is reference-free (no references pointing to it), the element itself is picked
      up by the garbage collector as well as any event handlers/listeners associated with it.
      getEventListeners(audioRecorder.mediaRecorder) will return an empty array of events.*/
  }
}

function startAudioRecording() {
  //start recording using the audio recording API
  console.log('starting recording')
  this.parentElement.querySelector("#chat-main-audio-stop").classList.remove('d-none');
  this.classList.add('d-none');
  audioRecorder.start()
      .then(() => { //on success
          console.log("Recording Audio...")
      })    
      .catch(error => { //on error
          //No Browser Support Error
          console.log(error)
          if (error.message.includes("mediaDevices API or getUserMedia method is not supported in this browser.")) {       
              console.log("To record audio, use browsers like Chrome and Firefox.");
          }
          switch (error.name) {
            case 'AbortError': //error from navigator.mediaDevices.getUserMedia
                console.log("An AbortError has occured.");
                break;
            case 'NotAllowedError': //error from navigator.mediaDevices.getUserMedia
                console.log("A NotAllowedError has occured. User might have denied permission.");
                break;
            case 'NotFoundError': //error from navigator.mediaDevices.getUserMedia
                console.log("A NotFoundError has occured.");
                break;
            case 'NotReadableError': //error from navigator.mediaDevices.getUserMedia
                console.log("A NotReadableError has occured.");
                break;
            case 'SecurityError': //error from navigator.mediaDevices.getUserMedia or from the MediaRecorder.start
                console.log("A SecurityError has occured.");
                break;
            case 'TypeError': //error from navigator.mediaDevices.getUserMedia
                console.log("A TypeError has occured.");
                break;
            case 'InvalidStateError': //error from the MediaRecorder.start
                console.log("An InvalidStateError has occured.");
                break;
            case 'UnknownError': //error from the MediaRecorder.start
                console.log("An UnknownError has occured.");
                break;
            default:
                console.log("An error occured with the error name " + error.name);
                console.log(error);
          };
      });
}

document.getElementById("chat-main-audio-start").addEventListener("click", startAudioRecording); 


function stopAudioRecording() {
  console.log('stopping recording')
  //stop the recording using the audio recording API
  this.parentElement.querySelector("#chat-main-audio-start").classList.remove('d-none');
  this.classList.add('d-none');
  console.log("Stopping Audio Recording...")
  audioRecorder.stop()
      .then(audioAsblob => { //stopping makes promise resolves to the blob file of the recorded audio
          console.log("stopped with audio Blob:", audioAsblob);

          const baseUrl = getBaseUrl();
          const endpointUrl = '/ajax/process-chat-audio/';
          const requestUrl = baseUrl + endpointUrl;

          const requestData = new FormData();
          requestData.append('chat-user-audio', audioAsblob);

          const csrfToken = getCookie('csrftoken');
          const requestHeader = {
            // 'Content-Type': 'multipart/form-data',
            "X-Requested-With": "XMLHttpRequest",
            'X-CSRFTOKEN': csrfToken
          }

          const response = fetch(requestUrl, {
            method: "POST",
            mode: "cors",
            cache: "no-cache",
            credentials: "same-origin",
            headers: requestHeader,
            redirect: "follow",
            referrerPolicy: "no-referrer",
            body: requestData,
          }).then(
            response => response.json()
          ).then(
            function(responseData) {
              const input = document.getElementById('chat-input-main');
              input.setAttribute('value', responseData.result)
          });

          //Do something with the recorded audio
          //...
      })
      .catch(error => {
          //Error handling structure
          console.log(error)
          switch (error.name) {
              case 'InvalidStateError': //error from the MediaRecorder.stop
                  console.log("An InvalidStateError has occured.");
                  break;
              default:
                  console.log("An error occured with the error name " + error.name);
          };

      });
}

document.getElementById("chat-main-audio-stop").addEventListener("click", stopAudioRecording); 


function cancelAudioRecording() {
    console.log("Canceling audio...");
    //cancel the recording using the audio recording API
    audioRecorder.cancel();
  
    //Do something after audio recording is cancelled
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

    fetch(requestUrl, {
      method: "POST",
      mode: "cors",
      cache: "no-cache",
      credentials: "same-origin",
      headers: requestHeader,
      redirect: "follow",
      referrerPolicy: "no-referrer",
      body: requestData,
    }).then(
      response => response.json()
    ).then(function(responseData) {
      console.log(responseData)
      const rowRequestData = new FormData();
      rowRequestData.append('chat-user-resp', responseData.result);

      getCharRow(rowRequestData).then(function(rowResponseData) {
        const chatRowPartial = rowResponseData.result;
        const chatContainer = document.getElementById('chat-resp-container');
        console.log(chatRowPartial)
        chatContainer.innerHTML = chatRowPartial;
      });
      

    });
}

function getCharRow(requestData) {
  
  let out;

  const baseUrl = getBaseUrl();
  const endpointUrl = '/ajax/get-chat-row/';
  const requestUrl = baseUrl + endpointUrl;
  const csrfToken = getCookie('csrftoken');
  const requestHeader = {
    // 'Content-Type': 'multipart/form-data',
    "X-Requested-With": "XMLHttpRequest",
    'X-CSRFTOKEN': csrfToken
  }

  return fetch(requestUrl, {
    method: "POST",
    mode: "cors",
    cache: "no-cache",
    credentials: "same-origin",
    headers: requestHeader,
    redirect: "follow",
    referrerPolicy: "no-referrer",
    body: requestData,
  }).then(
    response => response.json()
  )
}

document.getElementById("chat-submit-main").addEventListener("click", delayFunction(700, loadChatResponse));
document.getElementById("chat-input-main").addEventListener("keypress", function(event) {
  if (event.key === "Enter") {
    event.preventDefault();
    document.getElementById("chat-submit-main").click();
  }
}); 