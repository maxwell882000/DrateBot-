let UsersPage = function() {
    let Filter = function() {
        let companiesSelect = $('#companiesSelect');
        let departmentsSelect = $('#departmentsSelect');
        let isManagerCheckbox = $('#IsManager');
        let depatmentsList = $('#departmentsList');
        let usersTable = $('#usersTable');
        let usersRows = usersTable.find('tr.user-table-row');
        let resetButton = $('#resetFilter');
        companiesSelect.on('change', function() {
           let companyId = this.value;
           if (companyId === '') {
                return true;
           }
           let departmentsOptions = depatmentsList.find(`option[data-company-id=${companyId}]`).clone();
           let departmentsCurrentOptions = departmentsSelect.children();
           if (departmentsCurrentOptions.length > 1) {
              departmentsCurrentOptions.slice(1).remove();
           }
           departmentsSelect.append(departmentsOptions);
           departmentsSelect.removeAttr('disabled');
           for (let i = 0; i < usersRows.length; i++) {
               let userRow = $(usersRows[i]);
               let userCompanyId = userRow.attr('data-company-id');
               if (userCompanyId === companyId) {
                   if(userRow.hasClass('d-none')) {
                       userRow.removeClass('d-none');
                   }
               } else {
                   if(!userRow.hasClass('d-none')) {
                       userRow.addClass('d-none');
                   }
               }
           }
        });
        departmentsSelect.on('change', function() {
            let departmentId = this.value;
            for (let i = 0; i < usersRows.length; i++) {
                let userRow = $(usersRows[i]);
                let userDepartmentId = userRow.attr('data-department-id');
                if (userDepartmentId === departmentId) {
                   if(userRow.hasClass('d-none')) {
                       userRow.removeClass('d-none');
                   }
               } else {
                   if(!userRow.hasClass('d-none')) {
                       userRow.addClass('d-none');
                   }
               }
            }
        });
        resetButton.on('click', function() {
            let departmentsCurrentOptions = departmentsSelect.children();
            if (departmentsCurrentOptions.length > 1) {
                departmentsCurrentOptions.slice(1).remove();
            }
            departmentsSelect.attr('disabled', 'disabled');
            companiesSelect.val('').trigger('change');
            usersRows.removeClass('d-none');
            isManagerCheckbox.prop('checked', false);
        });
        isManagerCheckbox.on('change', function() {
            if (this.checked) {
                let departmentsCurrentOptions = departmentsSelect.children();
                if (departmentsCurrentOptions.length > 1) {
                    departmentsCurrentOptions.slice(1).remove();
                }
                departmentsSelect.attr('disabled', 'disabled');
                companiesSelect.val('').trigger('change');
                usersRows.removeClass('d-none');
                for (let i = 0; i < usersRows.length; i++) {
                    let userRow = $(usersRows[i]);
                    let attr = userRow.attr('data-is-manager');
                    if (typeof attr !== typeof undefined && attr !== false) {
                        if(userRow.hasClass('d-none')) {
                            userRow.removeClass('d-none');
                        }
                    } else {
                        if(!userRow.hasClass('d-none')) {
                            userRow.addClass('d-none');
                        }
                    }
                }
            } else {
                usersRows.removeClass('d-none');
            }
        })
    };

    let DataTable = function() {
        jQuery('.js-dataTable-simple').dataTable({
            ordering: true,
            pageLength: 10,
            lengthMenu: [[5, 8, 15, 20], [5, 8, 15, 20]],
            autoWidth: false,
            searching: false,
            oLanguage: {
                sLengthMenu: ""
            },
            dom: "<'row'<'col-sm-12'tr>>" +
                "<'row'<'col-sm-6'i><'col-sm-6'p>>"
        });
    };

    return {
        init() {
            Filter();
            DataTable();
        }
    }
}();

$(function() {
    UsersPage.init();
});