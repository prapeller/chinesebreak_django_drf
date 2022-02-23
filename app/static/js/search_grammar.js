'use strict'

$('input#search_grammar').keyup( e => {
    e.preventDefault()

    let input = e.target

    let searchStr = input.value
    let taskPk = input.dataset.task_pk

    $.ajax(
        {
            url: `/adminpanel/structure/tasks/update_with_ajax/${taskPk}/?search_grammars=${searchStr}`,
            success: data => {
                $('.search-grammars-list').html(data.search_grammars_list_html)
            }
        })
})
