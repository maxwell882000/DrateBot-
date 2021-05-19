let RatingsPage = function() {
    let Filters = function() {
        let companiesSelect = $('#companiesSelect');
        let departmentsSelect = $('#departmentsSelect');
        let depatmentsList = $('#departmentsList');
        let ratingsTable = $('#ratingsTable');
        let ratingsRows = ratingsTable.find('tr.rating-tabler-row');
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
            for (let i = 0; i < ratingsRows.length; i++) {
                let ratingRow = $(ratingsRows[i]);
                let ratingCompanyId = ratingRow.attr('data-company-id');
                if (ratingCompanyId === companyId) {
                    ratingRow.removeClass('d-none');
                } else {
                    ratingRow.addClass('d-none');
                }
            }
        });
        departmentsSelect.on('change', function() {
            let departmentId = this.value;
            for (let i = 0; i < ratingsRows.length; i++) {
                let ratingRow = $(ratingsRows[i]);
                let ratingDepartmentId = ratingRow.attr('data-department-id');
                if (ratingDepartmentId === departmentId) {
                    ratingRow.removeClass('d-none');
                } else {
                    ratingRow.addClass('d-none');
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
            ratingsRows.removeClass('d-none');
        })
    }

    return {
        init() {
            Filters();
        }
    }
}();

$(function() {
    RatingsPage.init();
})