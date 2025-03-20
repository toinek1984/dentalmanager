document.addEventListener('DOMContentLoaded', function() {
    console.log("Planboard loaded.");

    // Haal de CSRF-token op (indien aanwezig)
    const csrfTokenElem = document.querySelector('[name=csrfmiddlewaretoken]');
    const csrfToken = csrfTokenElem ? csrfTokenElem.value : '';

    // Maak externe events draggable met removeOnDrop
    const externalEventsContainer = document.getElementById('external-events');
    if (externalEventsContainer) {
        new FullCalendar.Draggable(externalEventsContainer, {
            itemSelector: '.fc-event.external-event',
            eventData: function(eventEl) {
                const id = eventEl.getAttribute('data-id');
                const title = eventEl.innerText.trim();
                console.log("Draggable event data:", id, title);
                return { id: id, title: title };
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
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'resourceTimeGridWeek,dayGridMonth,timeGridDay'
        },
        resources: '/planning/api/resources/',
        events: '/planning/api/werkbonnen/',
        eventDrop: function(info) {
            console.log("Event dropped:", info.event.id, "New start:", info.event.start.toISOString());
            const resources = info.event.getResources();
            const resource = resources.length > 0 ? resources[0] : null;
            if (!resource) {
                console.warn("No resource found, reverting drop.");
                info.revert();
                return;
            }
            // Verstuur update naar de server
            fetch(`/planning/api/werkbonnen/${info.event.id}/update/`, {
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
                    // Probeer eerst de dragged element te verwijderen
                    if (info.draggedEl) {
                        console.log("Removing dragged element using info.draggedEl.");
                        info.draggedEl.remove();
                    } else {
                        // Fallback: zoek in de external-events container op data-id
                        const extContainer = document.getElementById('external-events');
                        if (extContainer) {
                            const child = extContainer.querySelector(`[data-id="${info.event.id}"]`);
                            if (child) {
                                console.log("Removing dragged element using fallback lookup.");
                                child.remove();
                            } else {
                                console.warn("No external event element found with data-id:", info.event.id);
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

    // Globale opslag voor resources voor filtering
    let allResources = [];
    fetch('/planning/api/resources/')
        .then(response => response.json())
        .then(data => {
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

    // Handler voor de knop "Nieuwe werkbon toevoegen"
    const addWorkorderButton = document.getElementById('add-workorder');
    if (addWorkorderButton) {
        addWorkorderButton.addEventListener('click', function() {
            window.location.href = '/planning/aanmaken/';
        });
    }
});
