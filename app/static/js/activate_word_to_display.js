'use strict'

$('.task-words').on('change', '.display-word-checkbox', e => {

    let checkbox = e.target
    let isChecked = checkbox.checked

    let taskWord = checkbox.parentElement.parentElement
    let taskPk = parseInt(taskWord.dataset.task_pk)
    let wordIdx = parseInt(taskWord.dataset.word_idx)

    $.ajax(
        {
            url: `/adminpanel/structure/tasks/update_with_ajax/${taskPk}/?act_deact_to_display_word_idx=${wordIdx}`,
        })
})
