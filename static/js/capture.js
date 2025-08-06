let video = document.getElementById('video');
let canvas = document.getElementById('canvas');
let ctx = canvas.getContext('2d');
let captureBtn = document.getElementById('capture-btn');
let retakeBtn = document.getElementById('retake-btn');
let submitBtn = document.getElementById('submit-btn');
let uploadInput = document.getElementById('upload');
let capturedImage = document.getElementById('captured-image');

// Start camera
navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => {
    video.srcObject = stream;
  })
  .catch(err => {
    console.error("Camera access denied:", err);
  });

// Capture image
captureBtn.addEventListener('click', () => {
  canvas.classList.remove('is-hidden');
  video.classList.add('is-hidden');
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
  let imageDataURL = canvas.toDataURL('image/png');
  capturedImage.src = imageDataURL;
  capturedImage.classList.remove('is-hidden');
  captureBtn.classList.add('is-hidden');
  retakeBtn.classList.remove('is-hidden');
  submitBtn.disabled = false;
});

// Retake image
retakeBtn.addEventListener('click', () => {
  canvas.classList.add('is-hidden');
  capturedImage.classList.add('is-hidden');
  video.classList.remove('is-hidden');
  captureBtn.classList.remove('is-hidden');
  retakeBtn.classList.add('is-hidden');
  submitBtn.disabled = true;
});

// Enable submit on upload
uploadInput.addEventListener('change', () => {
  if (uploadInput.files.length > 0) {
    submitBtn.disabled = false;
  }
});
