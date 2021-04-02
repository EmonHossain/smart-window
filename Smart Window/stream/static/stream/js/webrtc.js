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
	
	//The clock will work only if video stream starts
    function clockrun() {
        if (streaming) {
            (function tick() {
                takephoto();
                console.log("tic - toc");
                window.setTimeout(tick, 1000);
            }());
        }
    }

    function sendToAnalysis(img64) {

        var impos = new Object();
        impos.img = img64.split(",")[1];

        var token = $('input[name="csrfmiddlewaretoken"]').attr('value');


        $.ajax({
            url: '/img/analysis/',
            type: 'POST',
            dataType: 'json',
            contentType:"application/json",
            data: JSON.stringify(impos),
            headers: {'contentType': 'application/json', 'X-CSRFToken': token}
        })
            .done(function (data) {
                if(data.found && prevPoiTitle != data.poi) {

                    $('#main-panel-poi-img').attr('src', data.img);
                    $('#main-panel-poi-title').text(data.poi);
                    $('#main-panel-poi-desc').text(data.desc);

                    prevPoiTitle = data.poi;

                    console.log("poi changed to "+data.poi);
                    $('#poi-panel').removeAttr("hidden");
                    $('#welcome-panel').hide();

                    $('#img-q').prepend("<img src='"+data.img+"' >");

                    if(data.poi =="Opera House Chemnitz"){
                        $("#cn-opera").parent().remove();
                    }else if (data.poi == "Karl marx monument"){
                        $("#cn-karl").parent().remove();
                    }
                }
            })
            .fail(function () {
                console.log("error");
            })
            .always(function () {
                console.log("complete");
            });
    }
    var pressCounter = 0;
    $(this).keypress(function(e) {

        if(e.which == 97 ){
            if (pressCounter <= locations.length) {
                $("#loc-now").text(locations[pressCounter]);
                pressCounter++;
            }else {
                pressCounter = 0;
            }
        }
        else if(e.which == 99){
            var nth = $(".info-next").children();
            if(nth.length > 1){
                nth.first().remove();
            }
        }
    });

});