'use strict'

$('input#search_wrong_word').keyup( e => {
    e.preventDefault()

    let input = e.target

    let searchStr = input.value
    let taskPk = input.dataset.task_pk

    $.ajax(
        {
            url: `/adminpanel/structure/tasks/update_with_ajax/${taskPk}/?search_wrong_words=${searchStr}`,
            success: data => {
                $('.search-wrong-words-list').html(data.search_wrong_words_list_html)
            }
        })
})
