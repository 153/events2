window.onload =  function mydate() {
    var date = new Date();
    var tz = (date.getTimezoneOffset() / 60);
    if (tz > 0) {
	tz = "-" + tz.toString().padStart(2, '0');

    } else {
	tz = "+" + tz.toString().padStart(2, '0');
    }
    tz += "00"
    var utc = document.getElementById('utc').innerHTML;
    console.log(utc);
    var localized = moment(utc);
    var until = localized.fromNow();
    document.getElementById('utc').innerHTML =
	"&#8987; Local time (UTC " + tz.toString().padStart(2, '0') + "): <br> "
	+ "&emsp;<i>" + until + ", on " + localized.calendar() + "</i>";
  }
