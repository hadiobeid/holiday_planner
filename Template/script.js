

document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
      initialView: 'dayGridMonth'
    });
    
    calendar.render();
    let _startdate = new Date('01/01/2025')
    calendar.gotoDate(_startdate)
  });