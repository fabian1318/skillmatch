document.addEventListener('DOMContentLoaded', function () {
    
    // 1. Inicializar Tooltips de Bootstrap (usados en Insignias)
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // 2. Inicializar Popovers (si los usamos en el futuro)
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
      return new bootstrap.Popover(popoverTriggerEl)
    });

    console.log('SkillMatch JS cargado correctamente.');
});