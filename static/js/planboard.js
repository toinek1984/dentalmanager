document.addEventListener('DOMContentLoaded', function() {
    console.log("Planboard geladen.");

    // Functie om de externe events draggable te maken
    function initDraggableEvents() {
        var externalEventsContainer = document.getElementById('external-events');
        if (externalEventsContainer) {
            // Maak een nieuwe Draggable-instantie; dit zorgt voor alle child-elementen
            new FullCalendar.Draggable(externalEventsContainer, {
                itemSelector: '.fc-event.external-event',
                eventData: function(eventEl) {
                    const id = eventEl.getAttribute('data-id');
                    const title = eventEl.innerText.trim();
                    console.log("Draggable event data:", id, title);
                    return { id: id, title: title };
                }
            });
            console.log("Draggable external events geactiveerd.");
        } else {
            console.error("Container met id 'external-events' niet gevonden.");
        }
    }

    // Roep de functie aan bij pageload
    initDraggableEvents();

    // Initialiseer de kalender
    const calendarEl = document.getElementById('calendar');
    if (!calendarEl) {
        console.error("Element met id 'calendar' niet gevonden.");
        return;
    }
    const calendar = new FullCalendar.Calendar(calendarEl, {
        schedulerLicenseKey: 'GPL-My-Project-Is-Open-Source',
        initialView: 'resourceTimeGridWeek',
        locale: 'nl',
        height: '100%',
        editable: true,
        droppable: true,
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'resourceTimeGridWeek,dayGridMonth,timeGridDay'
        },
        resources: '/planning/api/resources/',
        events: '/planning/api/werkbonnen/',
        eventDrop: function(info) {
            console.log("Werkbon verplaatst:", info.event.id, "Nieuwe datum:", info.event.start.toISOString());
            
            // Haal het eerste resource-object op
            const resources = info.event.getResources();
            const resource = resources.length > 0 ? resources[0] : null;
            if (!resource) {
                console.warn("Geen resource gevonden, drop niet toegestaan.");
                info.revert();
                return;
            }

            // Update de werkbon via de API
            fetch(`/planning/api/werkbonnen/${info.event.id}/update/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({
                    'start': info.event.start.toISOString(),
                    'resourceId': resource.id
                })
            })
            .then(response => {
                if (!response.ok) {
                    return response.text().then(text => { throw new Error(text) });
                }
                return response.json();
            })
            .then(data => {
                console.log("Response van server:", data);
                if (data.status !== 'success') {
                    let errorMsg = data.message || "Onbekende fout";
                    alert("Er is een fout opgetreden: " + errorMsg);
                    info.revert();
                } else {
                    console.log("Werkbon succesvol geüpdatet.");
                    // Als de externe event-element in de container zit, verwijder deze
                    if (info.draggedEl && info.draggedEl.parentNode) {
                        info.draggedEl.parentNode.removeChild(info.draggedEl);
                    }
                    calendar.refetchEvents();
                }
            })
            .catch(error => {
                console.error("Netwerkfout of serverfout:", error);
                alert("Fout bij het plannen van de werkbon.");
                info.revert();
            });
        }
    });

    calendar.render();

    // Filteren op medewerker
    const employeeSelect = document.getElementById('employee-select');
    if (employeeSelect) {
        employeeSelect.addEventListener('change', function() {
            const selected = this.value;
            const resourceUrl = selected === 'alle' ? '/planning/api/resources/' : `/planning/api/resources/?medewerker=${selected}`;
            fetch(resourceUrl)
                .then(response => response.json())
                .then(data => {
                    console.log("Bijgewerkte resources:", data);
                    calendar.setOption('resources', data);
                    calendar.refetchEvents();
                })
                .catch(error => console.error("Fout bij ophalen van resources:", error));
        });
    }
});
