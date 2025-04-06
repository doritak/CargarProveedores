document.addEventListener("DOMContentLoaded", function() {
    const alerts = document.querySelectorAll('.alert');

    alerts.forEach(alert => {
        setTimeout(() => {
            // Quitar la clase 'show' activa el desvanecimiento (gracias a Bootstrap)
            alert.classList.remove('show');

            // Eliminar la alerta del DOM después de la animación
            setTimeout(() => {
                alert.remove();
            }, 500); // 500 ms debe coincidir con el tiempo de transición en CSS
        }, 3000); // La alerta permanece visible por 3 segundos
    });
});

// código del Delete Modal confirmación
document.addEventListener('DOMContentLoaded', function () {
    const confirmDeleteModal = document.getElementById('confirmDeleteModal');
    const deleteForm = document.getElementById('deleteForm');
    const successAlert = document.getElementById('successAlert');

    if (confirmDeleteModal) {
        confirmDeleteModal.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;
            const recordId = button.getAttribute('data-record-id');
            deleteForm.action = `/delete_proveedor/${recordId}/`; // Asegúrate de que esta URL sea correcta
        });

        deleteForm.addEventListener('submit', function (e) {
            // Elimina la línea que previene el envío del formulario
            // e.preventDefault(); // ❌ Esta línea estaba impidiendo que se enviara la solicitud real

            const modal = bootstrap.Modal.getInstance(confirmDeleteModal);
            modal.hide();

            // Opcional: Mostrar una alerta de éxito si deseas manejarlo visualmente
            successAlert.style.display = 'block';

            // Opcional: Desvanecer la alerta automáticamente después de 3 segundos
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(successAlert);
                bsAlert.close();
            }, 3000);
        });
    }
});

// update Modal
document.addEventListener('DOMContentLoaded', function () {
    const updateForm = document.getElementById('updateForm');
    const confirmUpdateBtn = document.getElementById('confirmUpdateBtn');
    const updateSuccessAlert = document.getElementById('updateSuccessAlert');
    const confirmUpdateModal = document.getElementById('confirmUpdateModal');

    if (confirmUpdateBtn && updateForm) {
        confirmUpdateBtn.addEventListener('click', function () {
            // Cierra el modal
            const modal = bootstrap.Modal.getInstance(confirmUpdateModal);
            modal.hide();

            // Envía el formulario
            updateForm.submit();

            // Muestra la alerta de éxito
            updateSuccessAlert.style.display = 'block';

            // Desvanece la alerta automáticamente después de 3 segundos
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(updateSuccessAlert);
                bsAlert.close();
            }, 3000);
        });
    }
});
