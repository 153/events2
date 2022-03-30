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
    var cnt = Math.floor(moment.duration(localized.diff(moment())).as('days'));
    if ((cnt < -1) || (cnt > 1)) {
	var until = moment().to(localized) + ", ";
    } else {
	var until = ""
    };
//    var until = moment(utc).duration().asDays();
    document.getElementById('utc').innerHTML =
	"&#8987; Local time (UTC " + tz.toString().padStart(2, '0') + "): <br> "
	 + "&emsp;<i>" + until + localized.calendar() + "</i>";
  }
