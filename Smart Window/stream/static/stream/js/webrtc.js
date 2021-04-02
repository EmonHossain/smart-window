$(document).ready(function () {

    var streaming = false;
    var canvas = null;
    var prevPoiTitle = "";

    var video = document.getElementById("video-panel");

    video.addEventListener('playing', (event) => {
        clockrun();
    });

    $('[data-toggle="tooltip"]').tooltip();
    const locations = ["Bahnhofstraße. 1","Theaterplatz. 2","Brückenstr. 10","Str. der Nationen. 3","Chemnitz-Zentrum"];

    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({video: {width: { min: 1280 }, height: { min: 720 }}, audio: false}).then(function (stream) {
            video.srcObject = stream;
            video.play();
            streaming = true;

        }).catch(function (err) {
            console.log(err);
        });
    }

    function takephoto() {
        canvas = document.getElementById("canvas-panel");
        var context = canvas.getContext('2d');
        if (video.videoWidth && video.videoHeight) {
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            context.drawImage(video, 0, 0, video.videoWidth, video.videoHeight);

            var data = canvas.toDataURL('image/png');
            sendToAnalysis(data)
        } else {
            clearphoto();
        }
    }

    function clearphoto() {
        var context = canvas.getContext('2d');
        context.fillStyle = "#AAA";
        context.fillRect(0, 0, canvas.width, canvas.height);
    }

});