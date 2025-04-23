document.addEventListener('DOMContentLoaded', function() {
  console.log("Planboard loaded.");

  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
  const token = "MIJNVEILIGETOKEN123";

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
  }

  const calendarEl = document.getElementById('calendar');
  if (!calendarEl) return;

  const calendar = new FullCalendar.Calendar(calendarEl, {
    schedulerLicenseKey: 'GPL-My-Project-Is-Open-Source',
    initialView: 'resourceTimeGridWeek',
    locale: 'nl',
    height: '100%',
    editable: true,
    droppable: true,
    eventResourceEditable: true,
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

    eventReceive(info) {
      console.log("External event received:", info.event.id);
      info.draggedEl?.remove();

      const eventId = Number(info.event.id);
      const resourceId = info.event.getResources()?.[0]?.id || null;
      const startTime = info.event.start.toISOString();

      if (!eventId || !resourceId) {
        console.warn("Missing eventId or resourceId.");
        return;
      }

      fetch(`/planning/api/werkbonnen/${eventId}/update/?token=${token}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          start: startTime,
          resourceId: resourceId,
          status: 'in_behandeling'
        })
      })
        .then(res => res.ok ? res.json() : res.text().then(txt => Promise.reject(txt)))
        .then(data => {
          console.log("Werkbon opgeslagen:", data);
          calendar.refetchEvents();
          refreshUnscheduledWerkbonnen();
        })
        .catch(err => {
          console.error("Fout bij opslaan:", err);
          alert("Werkbon kon niet worden opgeslagen. Teruggezet.");
          info.revert();
        });
    },

    eventDrop(info) {
      const eventId = Number(info.event.id);
      const resourceId = info.event.getResources()?.[0]?.id || null;
      const startTime = info.event.start.toISOString();

      if (!eventId || !resourceId) return;

      fetch(`/planning/api/werkbonnen/${eventId}/update/?token=${token}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          start: startTime,
          resourceId: resourceId,
          status: 'in_behandeling'
        })
      })
        .then(res => res.ok ? res.json() : res.text().then(txt => Promise.reject(txt)))
        .then(data => {
          calendar.refetchEvents();
          refreshUnscheduledWerkbonnen();
        })
        .catch(err => {
          console.error("Update failed:", err);
          info.revert();
        });
    },

    eventClick(info) {
      window.open(`/planning/werkbon/${info.event.id}/print/`, '_blank');
    }
  });

  calendar.render();

  let allResources = [];
  fetch('/planning/api/resources/')
    .then(r => r.json())
    .then(data => {
      allResources = data;
    });

  const employeeSelect = document.getElementById('employee-select');
  if (employeeSelect) {
    employeeSelect.addEventListener('change', () => {
      const val = employeeSelect.value;
      calendar.setOption('resources', val === 'alle' ? allResources : allResources.filter(r => String(r.id) === val));
      calendar.refetchEvents();
    });
  }

  document.getElementById('add-workorder')?.addEventListener('click', () => {
    window.location.href = '/planning/aanmaken/';
  });

  document.getElementById('new-activity-btn')?.addEventListener('click', () => {
    const types = [
      { id: 'route', title: 'Route rijden' },
      { id: 'snipper', title: 'Snippermiddag' },
      { id: 'vrij', title: 'Vrije dag' }
    ];
    let msg = "Selecteer activiteit:\n";
    types.forEach((t, i) => msg += `${i + 1}. ${t.title}\n`);
    const idx = parseInt(prompt(msg), 10) - 1;
    if (isNaN(idx) || !types[idx]) return alert("Ongeldige keuze.");

    const now = new Date();
    now.setHours(9, 0, 0, 0);
    const payload = {
      title: types[idx].title,
      start: now.toISOString(),
      resource: allResources[0]?.title || ''
    };

    fetch(`/planning/api/werkbonnen/create/?token=${token}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    })
      .then(r => r.ok ? calendar.refetchEvents() : r.text().then(txt => Promise.reject(txt)))
      .catch(err => {
        console.error("Error creating activity:", err);
        alert("Kan activiteit niet aanmaken.");
      });
  });

  function refreshUnscheduledWerkbonnen() {
    fetch('/planning/api/werkbonnen/unscheduled/')
      .then(res => res.json())
      .then(data => {
        const container = document.getElementById('external-events');
        container.innerHTML = '';

        if (data.length === 0) {
          container.innerHTML = '<p>Geen werkbonnen beschikbaar.</p>';
          return;
        }

        data.forEach(wb => {
          const div = document.createElement('div');
          div.className = 'fc-event external-event werkbon-kaart';
          div.setAttribute('data-id', wb.id);
          div.setAttribute('draggable', 'true');
          div.innerHTML = `<strong>${wb.werkbonnummer}</strong><br><em>${wb.klant}</em>`;
          container.appendChild(div);
        });

        new FullCalendar.Draggable(container, {
          itemSelector: '.fc-event.external-event',
          eventData(eventEl) {
            return {
              id: eventEl.dataset.id,
              title: eventEl.querySelector('strong')?.innerText || '',
              duration: '01:00'
            };
          },
          removeOnDrop: true
        });
      })
      .catch(err => {
        console.error("Fout bij verversen van werkbonnen:", err);
      });
  }

  window.refreshUnscheduledWerkbonnen = refreshUnscheduledWerkbonnen;
});
