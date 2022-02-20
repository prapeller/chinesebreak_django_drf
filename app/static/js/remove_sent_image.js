'use strict'

$('.sent-images').on('click', '.btn-close', e => {
    e.preventDefault()

    let delButton = e.target

    let sentImage = delButton.parentElement.parentElement
    let taskPk = parseInt(sentImage.dataset.task_pk)
    let sentImageIdx = parseInt(sentImage.dataset.sent_image_idx)

    $.ajax(
        {
            url: `/adminpanel/structure/tasks/update_with_ajax/${taskPk}/?remove_sent_image_idx=${sentImageIdx}`,
            success: data => {
                $('.sent-images').html(data.sent_images_html)
            }
        })
})
