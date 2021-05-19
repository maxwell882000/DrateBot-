let NewUserPage = function() {
   let onTheFlyFunctions = function() {
      let addCompanyBtn = $('#addCompanyBtn');
      let addDepartmentBtn = $('#addDepartmentBtn');
      let cancelAddCompanyBtn = $('<a href="#" class="btn btn-sm btn-alt-primary ml-20"><i class="fa fa-fw fa-undo"></i></a>');
      let cancelAddDepartmentBtn = $('<a href="#" class="btn btn-sm btn-alt-primary ml-20"><i class="fa fa-fw fa-undo"></i></a>');
      let newDepartmentInput = $("<input type='text' class='form-control' name='departmentsSelect' id='departmentsSelect'>");
      let newCompanyInput = $("<input type='text' class='form-control' name='companiesSelect' id='companiesSelect'>");
      let companiesLabel = $('label[for=companiesSelect]');
      let departmentsLabel = $('label[for=departmentsSelect]');
      let companiesSelect = $('#companiesSelect');
      let departmentsSelect = $('#departmentsSelect');
      let depatmentsList = $('#departmentsList');
      let companyInput = $('#company');
      let departmentInput = $('#department');
      let isManagerInput = $('#is_manager');
      let companiesSelections = [];
      let departmentsSelections = [];
      companiesSelect.on('change', function() {
         let companyId = this.value;
         let departmentsOptions = depatmentsList.find(`option[data-company-id=${companyId}]`).clone();
         let departmentsCurrentOptions = departmentsSelect.children();
         if (departmentsCurrentOptions.length > 1) {
            departmentsCurrentOptions.slice(1).remove();
         }
         departmentsSelect.append(departmentsOptions);
         departmentsSelect.removeAttr('disabled');
         addDepartmentBtn.removeClass('disabled');
         companyInput.val(this.value);
      });
      departmentsSelect.on('change', function() {
         departmentInput.val(this.value);
      });
      addCompanyBtn.on('click', function() {
         companiesSelections.push(companiesSelect, companiesSelect.next());
         departmentsSelections.push(departmentsSelect, departmentsSelect.next());
         companiesSelect.next().detach();
         companiesSelect.detach();
         departmentsSelect.next().detach();
         departmentsSelect.detach();
         addCompanyBtn.detach();
         addDepartmentBtn.detach();
         newCompanyInput.val('');
         newDepartmentInput.val('');
         newCompanyInput.insertBefore(companiesLabel);
         cancelAddCompanyBtn.insertAfter(companiesLabel);
         newDepartmentInput.insertBefore(departmentsLabel);
      });
      cancelAddCompanyBtn.on('click', function() {
         newCompanyInput.detach();
         cancelAddCompanyBtn.detach();
         companiesSelections.forEach(function(selection) {
            selection.insertBefore(companiesLabel);
         });
         addCompanyBtn.insertAfter(companiesLabel);
         newDepartmentInput.detach();
         departmentsSelections.forEach(function(selection) {
            selection.insertBefore(departmentsLabel);
         });
         addDepartmentBtn.insertAfter(departmentsLabel);
         companiesSelections = [];
         departmentsSelections = [];
         companyInput.val(companiesSelect.val());
      });
      addDepartmentBtn.on('click', function() {
         departmentsSelections.push(departmentsSelect, departmentsSelect.next());
         departmentsSelect.next().detach();
         departmentsSelect.detach();
         addDepartmentBtn.detach();
         addCompanyBtn.detach();
         newDepartmentInput.val('');
         newDepartmentInput.insertBefore(departmentsLabel);
         cancelAddDepartmentBtn.insertAfter(departmentsLabel);
      });
      cancelAddDepartmentBtn.on('click', function() {
         newDepartmentInput.detach();
         cancelAddDepartmentBtn.detach();
         departmentsSelections.forEach(function(selection) {
            selection.insertBefore(departmentsLabel);
         });
         addDepartmentBtn.insertAfter(departmentsLabel);
         addCompanyBtn.insertAfter(companiesLabel);
         departmentsSelections = [];
         departmentInput.val(departmentsSelect.val());
      });
      newCompanyInput.on('change', function() {
         companyInput.val(this.value);
      });
      newDepartmentInput.on('change', function () {
         departmentInput.val(this.value);
      });
      isManagerInput.on('change', function() {
          if (this.checked) {
              companiesSelect.val('');
              departmentsSelect.val('');
              companiesSelect.attr('disabled', 'disabled');
              departmentsSelect.attr('disabled', 'disabled');
              addCompanyBtn.addClass('disabled');
              addDepartmentBtn.addClass('disabled');
          } else {
              companiesSelect.removeAttr('disabled');
              addCompanyBtn.removeClass('disabled');
          }
      })
   };
   let confirmDeleteModal = function() {
      let deleteButton = $('#userDeleteButton');
      if (!deleteButton) {
         return
      }
      swal.setDefaults({
         buttonsStyling: false,
         confirmButtonClass: 'btn btn-lg btn-alt-success m-5',
         cancelButtonClass: 'btn btn-lg btn-alt-danger m-5',
         inputClass: 'form-control'
     });
     deleteButton.on('click', function () {
      let userName = deleteButton.attr('data-user-name');
      swal({
          title: 'Вы уверены?',
          text: `При удалении пользователя ${userName} удаляться все его данные, рейтинги, которые поставили ему, но НЕ удалятся рейтинги, которые ставил он. Вы точно уверены в этом?`,
          type: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#d26a5c',
          confirmButtonText: 'Я уверен!',
          cancelButtonText: 'Не уверен',
          html: false,
      }).then(function(result) {
          $('#userDeleteForm').submit();
      }, function (dismiss) {
      })
  })

   };

   return {
      init() {
         onTheFlyFunctions();
         confirmDeleteModal();
      }
   }
}();
$(function () {
   NewUserPage.init();
});