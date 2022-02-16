'use strict'

$('.task-words').on('click', '.btn-close', e => {

    let delButton = e.target

    let taskWord = delButton.parentElement.parentElement
    let taskPk = parseInt(taskWord.dataset.task_pk)
    let wordIdx = parseInt(taskWord.dataset.word_idx)

    $.ajax(
        {
            url: `/adminpanel/structure/tasks/update_with_ajax/${taskPk}/?remove_word_idx=${wordIdx}`,
            success: data => {
                $('.task-words').html(data.task_words_html)
                $('.active-elements').html(data.active_elements_html)
            }
        })
})
