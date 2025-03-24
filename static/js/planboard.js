document.addEventListener('DOMContentLoaded', function() {
    console.log("Planboard loaded.");

    // CSRF-token ophalen
    const csrfTokenElem = document.querySelector('[name=csrfmiddlewaretoken]');
    const csrfToken = csrfTokenElem ? csrfTokenElem.value : '';

    let allResources = [];

    // Externe events draggable maken
    const externalEventsContainer = document.getElementById('external-events');
    if (externalEventsContainer) {
        new FullCalendar.Draggable(externalEventsContainer, {
            itemSelector: '.fc-event.external-event',
            eventData: function(eventEl) {
                const id = eventEl.getAttribute('data-id');
                const title = eventEl.innerHTML;
                const duration = '01:00';
                console.log("Draggable event data:", id, title, "Duration:", duration);
                return { id: id, title: title, duration: duration };
            },
            removeOnDrop: true
        });
        console.log("External events are now draggable with removeOnDrop enabled.");
    } else {
        console.error("External events container not found.");
    }

    // Kalender initialiseren
    const calendarEl = document.getElementById('calendar');
    if (!calendarEl) {
        console.error("Calendar element not found.");
        return;
    }

    const calendar = new FullCalendar.Calendar(calendarEl, {
        schedulerLicenseKey: 'GPL-My-Project-Is-Open-Source',
        initialView: 'resourceTimeGridWeek',
        locale: 'nl',
        height: '100%',
        editable: true,
        droppable: true,
        eventResizableFromStart: true,
        defaultTimedEventDuration: '01:00:00',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'resourceTimeGridWeek,dayGridMonth,resourceTimeGridDay'
        },
        slotMinTime: '08:00:00',
        slotMaxTime: '18:00:00',
        slotDuration: '00:30:00',
        resources: '/planning/api/resources/',
        events: '/planning/api/werkbonnen/',
        // Gebruik eventContent om aangepaste inhoud te tonen (inclusief barcode indien beschikbaar)
        eventContent: function(arg) {
            let html = `<div class="fc-event-title">${arg.event.title}</div>`;
            if (arg.event.extendedProps.barcode) {
                html += `<div class="fc-event-barcode">Barcode: ${arg.event.extendedProps.barcode}</div>`;
            }
            return { html: html };
        },
        eventReceive: function(info) {
            console.log("External event received:", info.event.id);
            if (info.draggedEl) {
                info.draggedEl.remove();
            } else {
                const extContainer = document.getElementById('external-events');
                if (extContainer) {
                    const child = extContainer.querySelector(`[data-id="${info.event.id}"]`);
                    if (child) { child.remove(); }
                }
            }
        },
        eventDrop: function(info) {
            console.log("Event dropped:", info.event.id, "New start:", info.event.start.toISOString());
            const eventId = info.event.id;
            if (isNaN(Number(eventId))) {
                console.log("Tijdelijk event gedropt; lokaal bijgewerkt, geen server-update.");
                calendar.refetchEvents();
                return;
            }
            const resources = info.event.getResources();
            const resource = resources.length > 0 ? resources[0] : null;
            if (!resource) {
                console.warn("Geen resource gevonden, drop wordt teruggedraaid.");
                info.revert();
                return;
            }
            fetch(`/planning/api/werkbonnen/${eventId}/update/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    'start': info.event.start.toISOString(),
                    'resource': resource.title
                })
            })
            .then(response => {
                console.log("Response status (update):", response.status);
                if (!response.ok) {
                    return response.text().then(text => { throw new Error(text); });
                }
                return response.json();
            })
            .then(data => {
                console.log("Server response (update):", data);
                if (data.status !== 'success') {
                    let errorMsg = data.message || "Onbekende fout";
                    alert("Error: " + errorMsg);
                    info.revert();
                } else {
                    console.log("Event succesvol geüpdatet.");
                    calendar.refetchEvents();
                }
            })
            .catch(error => {
                console.error("Fout bij updaten event:", error);
                alert("Fout bij updaten event. Wijzigingen niet opgeslagen.");
                info.revert();
            });
        },
        eventClick: function(info) {
            // Doorsturen naar de detailpagina (waar je de volledige werkbon, inclusief barcode, ziet)
            window.location.href = `/planning/werkbon_overzicht/${info.event.id}/`;
        }
    });
    
    calendar.render();

    // Resources ophalen
    fetch('/planning/api/resources/')
        .then(response => response.json())
        .then(data => {
            console.log("Fetched resources:", data);
            allResources = data;
        })
        .catch(error => console.error("Error fetching resources:", error));

    // Filteren op medewerker
    const employeeSelect = document.getElementById('employee-select');
    if (employeeSelect) {
        employeeSelect.addEventListener('change', function() {
            const selected = this.value;
            if (selected === 'alle') {
                calendar.setOption('resources', allResources);
            } else {
                const filtered = allResources.filter(resource => resource.id == selected);
                calendar.setOption('resources', filtered);
            }
            calendar.refetchEvents();
        });
    }

    // Handler voor "Nieuwe werkbon toevoegen"
    const addWorkorderButton = document.getElementById('add-workorder');
    if (addWorkorderButton) {
        addWorkorderButton.addEventListener('click', function() {
            window.location.href = '/planning/aanmaken/';
        });
    }

    // Handler voor "Nieuwe Activiteit" met server-opslag
    const newActivityBtn = document.getElementById('new-activity-btn');
    if (newActivityBtn) {
        newActivityBtn.addEventListener('click', function() {
            const activityTypes = [
                { id: 'route', title: 'Route rijden' },
                { id: 'snipper', title: 'Snippermiddag' },
                { id: 'vrij', title: 'Vrije dag' }
            ];
            let message = "Selecteer een activiteit:\n";
            activityTypes.forEach((act, index) => {
                message += `${index + 1}. ${act.title}\n`;
            });
            const choice = prompt(message);
            const index = parseInt(choice) - 1;
            if (isNaN(index) || index < 0 || index >= activityTypes.length) {
                alert("Ongeldige keuze.");
                return;
            }
            const selectedActivity = activityTypes[index];
            
            // Forceer de starttijd op 09:00 lokale tijd ("9000")
            let newStart = new Date();
            newStart.setHours(9, 0, 0, 0);
            const start = newStart.toISOString();

            let defaultResource = (allResources.length > 0) ? allResources[0] : null;
            if (!defaultResource) {
                alert("Geen medewerker (behandelaar) beschikbaar. Voeg eerst een medewerker toe.");
                return;
            }
            let defaultResourceName = defaultResource.title;

            // Verstuur de nieuwe activiteit naar de server
            fetch('/planning/api/werkbonnen/create/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    title: selectedActivity.title,
                    start: start,
                    resource: defaultResourceName
                })
            })
            .then(response => {
                console.log("Response status (create):", response.status);
                if (!response.ok) {
                    return response.text().then(text => { throw new Error(text); });
                }
                return response.json();
            })
            .then(data => {
                console.log("Werkbon aangemaakt:", data);
                calendar.refetchEvents();
            })
            .catch(error => {
                console.error("Fout bij het aanmaken van werkbon:", error);
                alert("Fout bij het aanmaken van de werkbon.");
            });
        });
    }
});
