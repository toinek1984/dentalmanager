document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.dropdown-toggle').forEach(function (toggle) {
    toggle.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      const submenu = this.nextElementSibling;
      const isOpen = submenu.style.display === 'block';
      document.querySelectorAll('.submenu').forEach(m => m.style.display = 'none');
      submenu.style.display = isOpen ? 'none' : 'block';
    });
  });

  document.addEventListener('click', function () {
    document.querySelectorAll('.submenu').forEach(m => m.style.display = 'none');
  });
});
