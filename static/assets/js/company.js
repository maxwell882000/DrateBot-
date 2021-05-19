let CompanyPage = function() {
    let confirmModal = function() {
        swal.setDefaults({
            buttonsStyling: false,
            confirmButtonClass: 'btn btn-lg btn-alt-success m-5',
            cancelButtonClass: 'btn btn-lg btn-alt-danger m-5',
            inputClass: 'form-control'
        });
        let deleteButton = $('#companyDeleteButton');
        deleteButton.on('click', function () {
            let companyName = deleteButton.attr('data-company-name');
            swal({
                title: 'Вы уверены?',
                text: `При удалении компании ${companyName} удаляться все отделы, сотрудники, их рейтинги и все данные, связанные с ними. Вы точно уверены в этом?`,
                type: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#d26a5c',
                confirmButtonText: 'Я уверен!',
                cancelButtonText: 'Не уверен',
                html: false,
            }).then(function(result) {
                $('#companyDeleteForm').submit();
            }, function (dismiss) {
            })
        })
    };
    return {
        init() {
            confirmModal();
        }
    }
}();

$(function() {
    CompanyPage.init();
});