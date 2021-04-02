$(document).ready(function () {
    var upnext_reg = [];
    //showPosition();


    /*time*/
	var time = {};

    (function () {
        var clock = document.getElementById('clock');

        (function tick() {
            var minutes, d = new Date();
            time.weekday = d.getDay();
            time.day = d.getDate();
            time.month = d.getMonth() + 1; //JS says jan = 0
            time.year = d.getFullYear();
            time.minutes = d.getMinutes();
            time.hours = d.getHours(); //eastern time zone
            time.seconds = d.getSeconds();
            time.ms = d.getMilliseconds();

            minutes = (time.minutes < 10 ? '0' + time.minutes : time.minutes);
            $("#cur-time").text(time.hours + ':' + minutes + ' ' +time.day  + '/' + time.month + '/' + time.year);

            window.setTimeout(tick, 1000);
        }()); // Note the parens here, we invoke these functions right away
    }());
	

    $('#info-pos').click(function (event) {
        $('.info-cards').slideToggle("slow");
        $('#info-queue').slideToggle('slow');
        $('#widgets').slideToggle('slow');
    });


    // Set global variable
    var watchID;

    function showPosition() {
        if (navigator.geolocation) {
            watchID = navigator.geolocation.watchPosition(successCallback);
        } else {
            alert("Sorry, your browser does not support HTML5 geolocation.");
        }
    }

    function successCallback(position) {


        // Check position has been changed or not before doing anything
        if (true) {

            // Set previous location
            var prevLat = position.coords.latitude;
            var prevLong = position.coords.longitude;

            // Get current position
            var positionInfo = position.coords.latitude + ", " + position.coords.longitude;
            console.log("position info" + positionInfo);
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function () {
                if (this.readyState == 4 && this.status == 200) {


                    var data = JSON.parse(this.responseText);

                    /*var current_location = document.getElementById("location_info_card");
                    current_location.innerHTML = data.current_loc;*/
                    //var cur_loc = data.current_loc;
                    if(data.current_loc != null){
                        var sp = data.current_loc;
                        console.log(data.current_loc);
                        var loc="";
                        for(var i=0;i<sp.length-1;i++){
                            loc = loc+sp[i];
                        }
                        $("#loc-now").text("abc");
                    }
                    /*$.each(data.museums, function (index, val) {
                        if(val.img != ""){

                            $(".up-next").parent();
                            var main = $(".up-next").last();
                            var cloned = main.clone();
                            cloned.find("img").attr('src',val.img);
                            cloned.find(".title").text(val.title);
                            cloned.find(".distance").text(val.distance);
                            cloned.insertAfter(main);

                        }
                    });*/
                    $.each(data.museums, function (index, val) {
                        var isExist = upnext_reg.includes(val.title);

                        if(!isExist){
                            if(val.img != ""){
                                upnext_reg.push(val.title);
                                $(".up-next").parent();
                                var main = $(".up-next").first();
                                var cloned = main.clone();
                                cloned.find("img").attr('src',val.img);
                                cloned.find("img").attr("title",val.title+", "+val.distance+"m")
                                cloned.insertAfter(main);
                                if(upnext_reg.length == 1){
                                    main.remove();
                                }
                            }
                        }
                    });

                    $.each(data.landmarks, function (index, val) {
                        var isExist = upnext_reg.includes(val.title);

                        if(!isExist){
                            if(val.img != ""){
                                upnext_reg.push(val.title);
                                $(".up-next").parent();
                                var main = $(".up-next").last();
                                var cloned = main.clone();
                                cloned.find("img").attr('src',val.img);
                                cloned.find("img").attr("title",val.title+", "+val.distance+"m")
                                /*cloned.find(".title").text(val.title);
                                cloned.find(".distance").text(val.distance+"m");*/
                                cloned.insertAfter(main);
                                if(upnext_reg.length == 1){
                                    main.remove();
                                }
                            }
                        }
                    });

                    /*fetch('https://api.openweathermap.org/data/2.5/weather?q=' + data.current_loc + '&appid=a7049cdf5b04e184b6314f4c5660b41d').then(
                        function (response) {
                            if (response.status !== 200) {
                                console.log('Looks like there was a problem. Status Code: ' +
                                    response.status);
                                return;
                            }

                            // Examine the text in the response
                            response.json().then(function (data) {
                                console.log(data);
                                var name_value = data['name'];
                                var temp_value = data['main']['temp'] - 274;
                                temp_value = Math.floor(temp_value);
                                console.log(temp_value);
                                var description = data['weather'][0]['description'];

                                $('#temp-deg').text(temp_value);
                                $('#desc').text(description);

                            });
                        }
                        )
                    .catch(function (err) {
                        console.log('Fetch Error :-S', err);
                    });*/
                }
            };
            var token = $('input[name="csrfmiddlewaretoken"]').attr('value');
            xhttp.open("POST", "/geoinfo/");
            xhttp.setRequestHeader("Content-type", "application/json");
            xhttp.setRequestHeader("X-CSRFToken", token);
            xhttp.send(JSON.stringify({loc: positionInfo}));

        }

    }

});

