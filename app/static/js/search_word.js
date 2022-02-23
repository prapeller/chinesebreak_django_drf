'use strict'

$('input#search_word').keyup( e => {
    e.preventDefault()

    let input = e.target

    let searchStr = input.value
    let taskPk = input.dataset.task_pk
    console.log(searchStr, taskPk)

    $.ajax(
        {
            url: `/adminpanel/structure/tasks/update_with_ajax/${taskPk}/?search_words=${searchStr}`,
            success: data => {
                $('.search-words-list').html(data.search_words_list_html)
            }
        })
})
