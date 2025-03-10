document.addEventListener('DOMContentLoaded', function() {
  console.log("Planboard initialisatie gestart.");

  const containerEl = document.getElementById('external-events');
  if (containerEl) {
      new FullCalendar.Draggable(containerEl, {
          itemSelector: '.fc-event.external-event',  // Zorg dat beide klassen worden gebruikt
          eventData: function(eventEl) {
              console.log("Draggable event data:", eventEl.getAttribute('data-id'), eventEl.innerText.trim());
              return {
                  id: eventEl.getAttribute('data-id'),
                  title: eventEl.innerText.trim()
              };
          }
      });
      console.log("Draggable external events geactiveerd.");
  } else {
      console.error("Container voor externe events niet gevonden.");
  }
  
  // ... rest van de kalender-initialisatie
});
drop: function(info) {
    console.log("Extern event gedropt op kalender:", info);
    const draggedEl = info.draggedEl;
    const eventId = draggedEl.getAttribute('data-id');
    const newDate = info.dateStr;
    fetch(`/planning/api/werkbonnen/${eventId}/update/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify({ 'start': newDate })
    })
    .then(response => {
        if (!response.ok) {
            alert('Fout bij het plannen van de werkbon.');
        } else {
            calendar.refetchEvents();
            // Verwijder het externe event element uit de container
            if (draggedEl.parentNode) {
                draggedEl.parentNode.removeChild(draggedEl);
            }
        }
    })
    .catch(() => {
        alert('Fout bij het plannen van de werkbon.');
    });
}
