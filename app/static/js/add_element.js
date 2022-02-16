'use strict'

$('.search_elems').on('click', '.list-group-item', e => {
    e.preventDefault()

    let addButton = e.target

    let taskPk = parseInt(addButton.parentElement.dataset.task_pk)
    let wordId = parseInt(addButton.dataset.word_id)

    $.ajax(
        {
            url: `/adminpanel/structure/tasks/update_with_ajax/${taskPk}/?add_word_id=${wordId}`,
            success: data => {
                $('.task-words').html(data.task_words_html)
            }
        })
})
