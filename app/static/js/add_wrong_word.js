'use strict'

$('.search-wrong-words-list').on('click', '.list-group-item', e => {
    e.preventDefault()

    let addButton = e.target

    let taskPk = parseInt(addButton.dataset.task_pk)
    let wordPk = parseInt(addButton.dataset.word_pk)

    $.ajax(
        {
            url: `/adminpanel/structure/tasks/update_with_ajax/${taskPk}/?add_wrong_word_word_id=${wordPk}`,
            success: data => {
                $('.wrong-words').html(data.wrong_words_html)
            }
        })
})
