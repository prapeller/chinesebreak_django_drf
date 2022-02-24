'use strict'

$('.task-words').on('change', '.word-checkbox', e => {

    let checkbox = e.target
    let isChecked = checkbox.checked

    let taskWord = checkbox.parentElement.parentElement
    let taskPk = parseInt(taskWord.dataset.task_pk)
    let wordIdx = parseInt(taskWord.dataset.word_idx)

    let taskWordBox = taskWord.getElementsByClassName('task-word-box')[0]
    if (isChecked) {
        taskWordBox.classList.remove('inactive-word')
        taskWordBox.classList.add('active-word')
    } else {
        taskWordBox.classList.remove('active-word')
        taskWordBox.classList.add('inactive-word')
    }


    $.ajax(
        {
            url: `/adminpanel/structure/tasks/update_with_ajax/${taskPk}/?act_deact_word_idx=${wordIdx}`,
            success: data => {
                $('.active-elements').html(data.active_elements_html)
            }
        })
})

$('.task-words').on('change', '.delete-word-checkbox', e => {

    let checkbox = e.target
    let isChecked = checkbox.checked

    let taskWord = checkbox.parentElement.parentElement
    let taskPk = parseInt(taskWord.dataset.task_pk)
    let wordIdx = parseInt(taskWord.dataset.word_idx)

    $.ajax(
        {
            url: `/adminpanel/structure/tasks/update_with_ajax/${taskPk}/?act_deact_to_delete_word_idx=${wordIdx}`,
        })
})

$('.task-words').on('change', '.display-word-checkbox', e => {

    let checkbox = e.target
    let isChecked = checkbox.checked

    let taskWord = checkbox.parentElement.parentElement
    let taskPk = parseInt(taskWord.dataset.task_pk)
    let wordIdx = parseInt(taskWord.dataset.word_idx)

    $.ajax(
        {
            url: `/adminpanel/structure/tasks/update_with_ajax/${taskPk}/?act_deact_to_display_word_idx=${wordIdx}`,
        })
})

$('.task-words').on('change', '.grammar-checkbox', e => {

    let checkbox = e.target

    let taskWord = checkbox.parentElement.parentElement
    let taskPk = parseInt(taskWord.dataset.task_pk)
    let wordIdx = parseInt(taskWord.dataset.word_idx)

    $.ajax(
        {
            url: `/adminpanel/structure/tasks/update_with_ajax/${taskPk}/?act_deact_grammar_for_word_idx=${wordIdx}`,
            success: data => {
                $('.active-elements').html(data.active_elements_html)
            }
        })
})