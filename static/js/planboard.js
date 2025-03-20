document.addEventListener('DOMContentLoaded', function() {
    console.log("Planboard loaded.");

    // Haal de CSRF-token op (indien aanwezig)
    const csrfTokenElem = document.querySelector('[name=csrfmiddlewaretoken]');
    const csrfToken = csrfTokenElem ? csrfTokenElem.value : '';

    // Globale opslag voor resources (voor filtering)
    let allResources = [];

    // Maak externe events draggable met removeOnDrop
    const externalEventsContainer = document.getElementById('external-events');
    if (externalEventsContainer) {
        new FullCalendar.Draggable(externalEventsContainer, {
            itemSelector: '.fc-event.external-event',
            eventData: function(eventEl) {
                const id = eventEl.getAttribute('data-id');
                // Gebruik innerHTML zodat de volledige opmaak (bijv. een "kaart") wordt meegenomen
                const title = eventEl.innerHTML;
                const duration = '01:00'; // standaardduur van 1 uur
                console.log("Draggable event data:", id, title, "Duration:", duration);
                return { id: id, title: title, duration: duration };
            },
            removeOnDrop: true
        });
        console.log("External events are now draggable with removeOnDrop enabled.");
    } else {
        console.error("External events container not found.");
    }

    // Initialiseer de kalender
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
            right: 'resourceTimeGridWeek,dayGridMonth,timeGridDay'
        },
        resources: '/planning/api/resources/',
        events: '/planning/api/werkbonnen/',
        // Wanneer een extern event wordt overgenomen (bij drop)
        eventReceive: function(info) {
            console.log("External event received:", info.event.id);
            if (info.draggedEl) {
                console.log("Removing external element via eventReceive using info.draggedEl.");
                info.draggedEl.remove();
            } else {
                const extContainer = document.getElementById('external-events');
                if (extContainer) {
                    const child = extContainer.querySelector(`[data-id="${info.event.id}"]`);
                    if (child) {
                        console.log("Removing external element via fallback in eventReceive.");
                        child.remove();
                    }
                }
            }
        },
        eventDrop: function(info) {
            console.log("Event dropped:", info.event.id, "New start:", info.event.start.toISOString());
            const eventId = info.event.id;
            // Controleer of eventId een numerieke waarde is (reguliere werkbon) of niet (extra activiteit)
            if (isNaN(Number(eventId))) {
                // Als het geen numeriek id is, is dit een extra activiteit die nog niet op de server staat
                console.log("Extra activiteit gedropt; lokaal bijgewerkt. Geen server-update.");
                // Verwijder het externe element indien aanwezig:
                if (info.draggedEl) {
                    info.draggedEl.remove();
                }
                // Update de kalender lokaal
                calendar.refetchEvents();
                return;
            }
            const resources = info.event.getResources();
            const resource = resources.length > 0 ? resources[0] : null;
            if (!resource) {
                console.warn("No resource found, reverting drop.");
                info.revert();
                return;
            }
            // Verstuur update naar de server voor reguliere werkbonnen
            fetch(`/planning/api/werkbonnen/${eventId}/update/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    'start': info.event.start.toISOString(),
                    'resourceId': resource.id
                })
            })
            .then(response => {
                if (!response.ok) {
                    return response.text().then(text => { throw new Error(text); });
                }
                return response.json();
            })
            .then(data => {
                console.log("Server response:", data);
                if (data.status !== 'success') {
                    let errorMsg = data.message || "Unknown error";
                    alert("Error: " + errorMsg);
                    info.revert();
                } else {
                    console.log("Event updated successfully.");
                    if (info.draggedEl) {
                        console.log("Removing dragged element using info.draggedEl in eventDrop.");
                        info.draggedEl.remove();
                    } else {
                        const extContainer = document.getElementById('external-events');
                        if (extContainer) {
                            const child = extContainer.querySelector(`[data-id="${eventId}"]`);
                            if (child) {
                                console.log("Removing dragged element using fallback lookup in eventDrop.");
                                child.remove();
                            } else {
                                console.warn("No external event element found with data-id:", eventId);
                            }
                        }
                    }
                    calendar.refetchEvents();
                }
            })
            .catch(error => {
                console.error("Error updating event:", error);
                alert("Error updating event.");
                info.revert();
            });
        }
    });
    
    calendar.render();

    // Haal resources op voor filtering en sla ze op in allResources
    fetch('/planning/api/resources/')
        .then(response => response.json())
        .then(data => {
            allResources = data;
        })
        .catch(error => console.error("Error fetching resources:", error));

    // Filteren op medewerker: schakel tussen collectieve en individuele weergave
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

    // Handler voor de knop "Nieuwe werkbon toevoegen"
    const addWorkorderButton = document.getElementById('add-workorder');
    if (addWorkorderButton) {
        addWorkorderButton.addEventListener('click', function() {
            window.location.href = '/planning/aanmaken/';
        });
    }

    // Handler voor de knop "Nieuwe Activiteit" met standaard keuzes
    const newActivityBtn = document.getElementById('new-activity-btn');
    if (newActivityBtn) {
        newActivityBtn.addEventListener('click', function() {
            // Vooraf gedefinieerde activiteitstypes
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
            // Gebruik de huidige datum en tijd als startmoment
            const now = new Date();
            const start = now.toISOString();
            // Wijs standaard de eerste resource toe (voor een extra activiteit kun je dit eventueel later aanpassen)
            let defaultResourceId = allResources.length > 0 ? allResources[0].id : null;
            // Maak een nieuw event met een tijdelijk (niet-numeriek) id zodat we weten dat het een extra activiteit is
            const newEvent = {
                id: 'temp-' + Date.now().toString(),  // id begint met 'temp-' zodat eventDrop weet dat dit geen server-event is
                title: selectedActivity.title,
                start: start,
                duration: '01:00', // standaardduur van 1 uur
                resourceId: defaultResourceId
            };
            calendar.addEvent(newEvent);
            alert("Activiteit toegevoegd! Je kunt deze verplaatsen of resizen.");
        });
    }
});
