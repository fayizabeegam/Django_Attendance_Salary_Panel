

window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

});



document.addEventListener('DOMContentLoaded', function () {
    // Edit employee
    const editButtons = document.querySelectorAll('[data-bs-target="#exampleModalCenter"]');

    editButtons.forEach(button => {
        button.addEventListener('click', function () {
            const id = this.getAttribute('data-id');
            const name = this.getAttribute('data-name');
            const ifid = this.getAttribute('data-ifid');
            const mobile = this.getAttribute('data-mobile');

            // Populate modal fields
            document.getElementById('edit_ifid').value = ifid;
            document.getElementById('edit_empname').value = name;
            document.getElementById('edit_mobile').value = mobile;

            // Update form action with the employee ID
            const form = document.querySelector('#exampleModalCenter form');
            form.action = `/adminapp/employee/edit/${id}/`;
        });
    });

    // Delete employee
    const deleteButtons = document.querySelectorAll('[data-bs-target="#deleteEmployeeModal"]');

        deleteButtons.forEach(button => {
            button.addEventListener('click', function () {
                const id = this.getAttribute('data-id');
                const name = this.getAttribute('data-name');

                // Update the modal content
                document.getElementById('deleteEmployeeName').textContent = name;

                // Update the form action URL
                const deleteForm = document.getElementById('deleteForm');
                deleteForm.action = `/adminapp/employees/delete/${id}/`;
            });
        });
    
});
