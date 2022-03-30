window.onload =  function mydate() {
    var date = new Date();
    var tz = (date.getTimezoneOffset() / 60);
    if (tz > 0) {
	tz = "-" + tz.toString().padStart(2, '0');

    } else {
	tz = "+" + tz.toString().padStart(2, '0');
    }
    tz += "00"
    // Get the event date in UTC..
    var utc = document.getElementById('utc').innerHTML;
    // and convert it to local time
    var localized = moment(utc);
    var a = localized.clone()
    var b = moment();
    var cnt = (a.startOf('day').diff(b.endOf('day'), 'days'));
    if (cnt != 0) {
	var until = moment().to(localized) + ", on ";
    } else {
	var until = ""
    };
//    var until = moment(utc).duration().asDays();
    document.getElementById('utc').innerHTML =
	"&#8987; Local time (UTC " + tz.toString().padStart(2, '0') + "): <br> "
	 + "&emsp;<i>" + until + localized.calendar() + "</i>";
  }
