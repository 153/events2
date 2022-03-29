window.onload =  function mydate() {
    var date = new Date();
    var tz = -1 * (date.getTimezoneOffset() / 60);
    var utc = document.getElementById('utc').innerHTML;
    console.log(utc);
    var localized = moment(utc);
    var until = localized.fromNow();
    document.getElementById('utc').innerHTML =
	"<br>Local time (UTC " + tz.toString().padStart(2, '0') + "): <br> "
	+ until + ", on " + localized.calendar();
  }
