'use strict'

$('.wrong-words').on('click', '.btn-close', e => {
    e.preventDefault()

    let delButton = e.target

    let wrongWord = delButton.parentElement.parentElement
    let taskPk = parseInt(wrongWord.dataset.task_pk)
    let wordPk = parseInt(wrongWord.dataset.word_pk)

    $.ajax(
        {
            url: `/adminpanel/structure/tasks/update_with_ajax/${taskPk}/?remove_wrong_word=${wordPk}`,
            success: data => {
                $('.wrong-words').html(data.wrong_words_html)
            }
        })
})
