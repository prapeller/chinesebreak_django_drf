'use strict'

$('.task-sents').on('click', '.btn-close', e => {
    e.preventDefault()

    let delButton = e.target

    let sentWrong = delButton.parentElement.parentElement
    let sentWrongIdx = parseInt(sentWrong.dataset.sent_wrong_idx)
    let taskPk = parseInt(sentWrong.dataset.task_pk)

    $.ajax(
        {
            url: `/adminpanel/structure/tasks/update_with_ajax/${taskPk}/?remove_sent_wrong_idx=${sentWrongIdx}`,
            success: data => {
                $('.task-sents').html(data.task_sents_html)
            }
        })
})
