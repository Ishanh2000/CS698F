# AUM SHREEGANESHAAYA NAMAH|| AUM SHREEHANUMATE NAMAH||
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = "Content-Type"

@app.route("/helloworld")
@cross_origin()
def hello_world():
  return "Hello, World!"

@app.route("/")
@cross_origin()
def recog():
  # return "recog"
  return """
    <body style="font-size: 3rem;">
      <!--div id="div1" style="color: white;">AUM NAMAH SHIVAAYA||</div-->
      <div id="div10">IMU Testing</div>
      <div id="div2"></div>
      <div id="div3"></div>
      <button id="button" style="font-size: 3rem;">CLICK HERE</button>
    </body>

    <script>
      var d2 = document.getElementById("div2");
      var d3 = document.getElementById("div3");
      
      
      function handleMotion(event) {
        d3.innerText = 'Accelerometer_x' + event.acceleration.x;
      }
      var curr = 0;
      function permission () {
          try {
            window.addEventListener("devicemotion", (e) => {
              // curr++;
              // if (curr === 100) window.addEventListener()
              // alert("ax = " + e.acceleration.x + "\nay = " + e.acceleration.y + "\naz = " + e.acceleration.z + "\nwx = " + e.rotationRate.x + "\nwy = " + e.rotationRate.x + "\nwz = " + e.rotationRate.z);
              alert(e.acceleration.x);

            } );
          }
          catch {
            alert("bad");
          }
          return;
          if ( typeof( DeviceOrientationEvent ) !== "undefined" && typeof( DeviceOrientationEvent.requestPermission ) === "function" ) {
              // (optional) Do something before API request prompt.
              DeviceOrientationEvent.requestPermission()
                  .then( response => {
                  // (optional) Do something after API prompt dismissed.
                  if ( response == "granted" ) {
                      window.addEventListener( "deviceorientation", (e) => {
                          // do something for 'e' here.
                      })
                  }
              })
                  .catch( console.error )
          } else {
              alert( "DeviceOrientationEvent is not defined" );
          }
      }
      const btn = document.getElementById( "button" );
      btn.addEventListener( "click", permission );

    </script>
  """


      # document.getElementById("button").onclick = function (event) {
      #   event.preventDefault();
      #   if (DeviceMotionEvent) d2.innerHTML = 'Accelerometer_x';
      #   else d2.innerHTML = 'Accelerometer_y';
      #   if (typeof DeviceMotionEvent === "function") d2.innerHTML = 'func';
      #   else d2.innerHTML = 'nofunc';
        
      #   DeviceMotionEvent.requestPermission();

      #   window.addEventListener("devicemotion", handleMotion });
      # }


# #### EVENTS ####
# @app.route("/events", methods=["POST"])
# @cross_origin()
# def events():
#   if request.method != "POST": return "Bad Request", 400
#   try: