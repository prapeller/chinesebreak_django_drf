'use strict'

$('.search_elems').on('click', '.list-group-item', e => {
    e.preventDefault()

    let addButton = e.target

    let taskPk = parseInt(addButton.parentElement.dataset.task_pk)
    let wordId = parseInt(addButton.dataset.word_id)
    let grammarId = parseInt(addButton.dataset.grammar_id)

    if (wordId) {
    $.ajax(
        {
            url: `/adminpanel/structure/tasks/update_with_ajax/${taskPk}/?add_word_id=${wordId}`,
            success: data => {
                $('.task-words').html(data.task_words_html)
            }
        })
    }
    if (grammarId) {
    $.ajax(
        {
            url: `/adminpanel/structure/tasks/update_with_ajax/${taskPk}/?add_grammar_id=${grammarId}`,
            success: data => {
                $('.active-elements').html(data.active_elements_html)
            }
        })
    }
})
