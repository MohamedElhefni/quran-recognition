//webkitURL is deprecated but nevertheless
URL = window.URL || window.webkitURL;

var gumStream; //stream from getUserMedia()
var rec; //Recorder.js object
var input; //MediaStreamAudioSourceNode we'll be recording

// shim for AudioContext when it's not avb.
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext; //audio context to help us record

var recordButton = document.getElementById("recordButton");
var outer1 = document.getElementsByClassName("outer")[0];
var outer2 = document.getElementsByClassName("outer-2")[0];
var state = document.getElementsByClassName("state")[0];
//add events to those 2 buttons
recordButton.addEventListener("click", startRecording);

function startRecording() {

  /*
		Simple constraints object, for more advanced audio features see
		https://addpipe.com/blog/audio-constraints-getusermedia/
	*/

  var constraints = { audio: true, video: false };

  /*
    	Disable the record button until we get a success or fail from getUserMedia() 
	*/

  recordButton.disabled = true;

  /*
    	We're using the standard promise based getUserMedia() 
    	https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia
	*/

  navigator.mediaDevices
    .getUserMedia(constraints)
    .then(function (stream) {
  

      /*
			create an audio context after getUserMedia is called
			sampleRate might change after getUserMedia is called, like it does on macOS when recording through AirPods
			the sampleRate defaults to the one set in your OS for your playback device

		*/
      audioContext = new AudioContext();

      //update the format
      // document.getElementById("formats").innerHTML="Format: 1 channel pcm @ "+audioContext.sampleRate/1000+"kHz"

      /*  assign to gumStream for later use  */
      gumStream = stream;

      /* use the stream */
      input = audioContext.createMediaStreamSource(stream);

      /* 
			Create the Recorder object and configure to record mono sound (1 channel)
			Recording 2 channels  will double the file size
		*/
      rec = new Recorder(input, { numChannels: 1 });

      //start the recording process
      rec.record();
      state.textContent = "listening .....";
      outer1.classList.remove("none");
      outer2.classList.remove("none");
      recordButton.disabled = true;
      recordButton.classList.add("disabled");
      setTimeout(stopRecording, 7000);
    })
    .catch(function (err) {
      //enable the record button if getUserMedia() fails
      recordButton.disabled = false;
      console.log(err);
    });
}

function stopRecording() {
  outer1.classList.add("none");
  outer2.classList.add("none");
  //disable the stop button, enable the record too allow for new recordings
  recordButton.disabled = false;

  //reset button just in case the recording is stopped while paused

  //tell the recorder to stop the recording
  rec.stop();

  //stop microphone access
  gumStream.getAudioTracks()[0].stop();

  //create the st blob and pass it on to createDownloadLink
  rec.exportWAV(createDownloadLink);
}

function createDownloadLink(blob) {
  state.textContent = "recognizing .....";

  var filename = new Date().toISOString();
  var fd = new FormData();
  fd.append("audio_data", blob, filename);
  fetch("/", {
    method: "POST",
    body: fd,
  })
    .then((response) => response.json())
    .then((data) => {
      let songName = data.results[0]
      state.textContent = songName.song_name;
      recordButton.disabled = false;
      recordButton.classList.remove("disabled");
    })
    .catch((err) => (state.textContent = err));
}
