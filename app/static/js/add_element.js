'use strict'

$('.search_elems').on('click', '.list-group-item', e => {
    e.preventDefault()

    let addButton = e.target

    let taskPk = parseInt(addButton.dataset.task_pk)
    let wordPk = parseInt(addButton.dataset.word_pk)
    let grammarPk = parseInt(addButton.dataset.grammar_pk)

    console.log(taskPk, wordPk, grammarPk)

    if (wordPk) {
    $.ajax(
        {
            url: `/adminpanel/structure/tasks/update_with_ajax/${taskPk}/?add_word_id=${wordPk}`,
            success: data => {
                $('.task-words').html(data.task_words_html)
            }
        })
    }
    if (grammarPk) {
    $.ajax(
        {
            url: `/adminpanel/structure/tasks/update_with_ajax/${taskPk}/?add_grammar_id=${grammarPk}`,
            success: data => {
                $('.active-elements').html(data.active_elements_html)
            }
        })
    }
})

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
