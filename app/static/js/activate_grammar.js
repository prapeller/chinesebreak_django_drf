'use strict'

$('.task-words').on('change', '.grammar-checkbox', e => {

    let checkbox = e.target

    let taskWord = checkbox.parentElement.parentElement
    let taskPk = parseInt(taskWord.dataset.task_pk)
    let wordIdx = parseInt(taskWord.dataset.word_idx)

    console.log(taskPk, wordIdx)

    $.ajax(
        {
            url: `/adminpanel/structure/tasks/update_with_ajax/${taskPk}/?act_deact_grammar_for_word_idx=${wordIdx}`,
            success: data => {
                $('.active-elements').html(data.active_elements_html)
            }
        })
})
