'use strict'

$('#exampleModal').on('show.bs.modal', e => {
    let button = $(e.relatedTarget)
    let app = button.data('app')
    let obj_type = button.data('type')
    let obj_pk = button.data('pk')

    let title = document.getElementsByClassName('modal-title')[0]
    title.innerHTML = `Deleting ${obj_pk} from ${obj_type}`

    let deleteForm = document.getElementsByClassName('delete-form')[0]
    deleteForm.setAttribute('action', `/adminpanel/${app}/${obj_type}/delete/${obj_pk}/`)

})
