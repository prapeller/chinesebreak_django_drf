'use strict'


$('#exampleModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget)
    let obj_type = button.data('type')
    let obj_pk = button.data('pk')
    var modal = $(this)
    modal.find('.modal-title').text(`Deleting ${obj_pk} from ${obj_type}`)
    modal.find('.delete-form').attr('action', `/adminpanel/structure/${obj_type}/delete/${obj_pk}/`)

    // $.ajax(
    //     {
    //         url: `structure/${obj_type}/delete/${obj_pk}/`,
    //         success: data => {
    //             $('.basket-list').html(data.result)
    //             $('.basket_total_qty').text(data.basket_total_qty)
    //         }
    //     })
})
