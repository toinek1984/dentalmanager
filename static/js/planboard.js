document.addEventListener('DOMContentLoaded', function() {
  console.log("Planboard loaded.");

  // 1) Grab CSRF token
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';

  // 2) Make external events draggable
  const externalEl = document.getElementById('external-events');
  if (externalEl) {
    new FullCalendar.Draggable(externalEl, {
      itemSelector: '.fc-event.external-event',
      eventData(eventEl) {
        return {
          id: eventEl.dataset.id,
          title: eventEl.textContent.trim(),
          duration: '01:00'
        };
      },
      removeOnDrop: true
    });
    console.log("External events draggable ready.");
  } else {
    console.warn("No external-events container found.");
  }

  // 3) Find and validate the calendar element
  const calendarEl = document.getElementById('calendar');
  if (!calendarEl) {
    console.error("Calendar element not found.");
    return;
  }

  // 4) Initialize FullCalendar
  const calendar = new FullCalendar.Calendar(calendarEl, {
    schedulerLicenseKey: 'GPL-My-Project-Is-Open-Source',
    initialView: 'resourceTimeGridWeek',
    locale: 'nl',
    height: '100%',
    editable: true,
    droppable: true,
    eventResourceEditable: true,      // ← allow dragging between resources
    eventResizableFromStart: true,
    defaultTimedEventDuration: '01:00:00',
    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: 'resourceTimeGridWeek,dayGridMonth,resourceTimeGridDay'
    },
    slotMinTime: '07:00:00',
    slotMaxTime: '18:00:00',
    slotDuration: '00:30:00',
    resources: '/planning/api/resources/',
    events: '/planning/api/werkbonnen/',

    // Custom content: show title, client & barcode
    eventContent(arg) {
      let html = `<div class="fc-event-title">${arg.event.title}</div>`;
      if (arg.event.extendedProps.client) {
        html += `<div class="fc-event-client">Klant: ${arg.event.extendedProps.client}</div>`;
      }
      if (arg.event.extendedProps.barcode) {
        html += `<div class="fc-event-barcode">Barcode: ${arg.event.extendedProps.barcode}</div>`;
      }
      return { html };
    },

    // Dropped from external list
    eventReceive(info) {
      console.log("External event received:", info.event.id);
      info.draggedEl?.remove();
    },

    // Moved inside the calendar
    eventDrop(info) {
      console.log("Event dropped:", info.event.id, "New start:", info.event.start.toISOString());

      const eventId = Number(info.event.id);
      if (isNaN(eventId)) {
        console.log("Temporary event, only local.");
        calendar.refetchEvents();
        return;
      }

      const resources = info.event.getResources();
      if (!resources.length) {
        console.warn("No resource found, reverting.");
        info.revert();
        return;
      }
      const resourceId = resources[0].id;

      fetch(`/planning/api/werkbonnen/${eventId}/update/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
          start: info.event.start.toISOString(),
          resourceId: resourceId
        })
      })
      .then(res => {
        if (!res.ok) return res.text().then(txt => Promise.reject(txt));
        return res.json();
      })
      .then(data => {
        if (data.status !== 'ok') {
          return Promise.reject(data.message || "Unknown update error");
        }
        console.log("Update succeeded:", data);
        calendar.refetchEvents();
      })
      .catch(err => {
        console.error("Update failed:", err);
        alert("Kon werkbon niet updaten. Wijziging wordt teruggedraaid.");
        info.revert();
      });
    },

    // Click → go to detail page
    eventClick(info) {
      window.location.href = `/planning/werkbon_overzicht/${info.event.id}/`;
    }
  });

  calendar.render();

  // 5) Load & cache resources so the filter can work
  let allResources = [];
  fetch('/planning/api/resources/')
    .then(r => r.json())
    .then(data => {
      allResources = data;
      console.log("Resources loaded:", allResources);
    })
    .catch(err => console.error("Error fetching resources:", err));

  // 6) Wire up the employee‑filter dropdown
  const employeeSelect = document.getElementById('employee-select');
  if (employeeSelect) {
    employeeSelect.addEventListener('change', () => {
      const val = employeeSelect.value;
      if (val === 'alle') {
        calendar.setOption('resources', allResources);
      } else {
        calendar.setOption(
          'resources',
          allResources.filter(r => String(r.id) === val)
        );
      }
      calendar.refetchEvents();
    });
  }

  // 7) “Nieuwe werkbon” button
  document.getElementById('add-workorder')?.addEventListener('click', () => {
    window.location.href = '/planning/aanmaken/';
  });

  // 8) “Nieuwe Activiteit” button
  document.getElementById('new-activity-btn')?.addEventListener('click', () => {
    const types = [
      { id: 'route', title: 'Route rijden' },
      { id: 'snipper', title: 'Snippermiddag' },
      { id: 'vrij', title: 'Vrije dag' }
    ];
    let msg = "Selecteer activiteit:\n";
    types.forEach((t, i) => msg += `${i+1}. ${t.title}\n`);
    const idx = parseInt(prompt(msg),10) - 1;
    if (isNaN(idx) || !types[idx]) return alert("Ongeldige keuze.");

    const now = new Date();
    now.setHours(9,0,0,0);
    const payload = {
      title: types[idx].title,
      start: now.toISOString(),
      resource: allResources[0]?.title || ''
    };

    fetch('/planning/api/werkbonnen/create/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify(payload)
    })
    .then(r => r.ok ? calendar.refetchEvents() : r.text().then(txt => Promise.reject(txt)))
    .catch(err => {
      console.error("Error creating activity:", err);
      alert("Kan activiteit niet aanmaken.");
    });
  });
});
