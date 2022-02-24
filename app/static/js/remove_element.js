'use strict'

$('.task-words').on('click', '.btn-close', e => {
    e.preventDefault()

    let delButton = e.target

    let taskWord = delButton.parentElement.parentElement
    let taskPk = parseInt(taskWord.dataset.task_pk)
    let wordIdx = parseInt(taskWord.dataset.word_idx)

    $.ajax(
        {
            url: `/adminpanel/structure/tasks/update_with_ajax/${taskPk}/?remove_word_idx=${wordIdx}`,
            success: data => {
                $('.task-words').html(data.task_words_html)
                $('.active-elements').html(data.active_elements_html)
            }
        })
})

$('.task-sents').on('click', '.btn-close', e => {
    e.preventDefault()

    let delButton = e.target

    let sentWrong = delButton.parentElement.parentElement
    let sentWrongIdx = parseInt(sentWrong.dataset.sent_wrong_idx)
    let taskPk = parseInt(sentWrong.dataset.task_pk)

    $.ajax(
        {
            url: `/adminpanel/structure/tasks/update_with_ajax/${taskPk}/?remove_sent_wrong_idx=${sentWrongIdx}`,
            success: data => {
                $('.task-sents').html(data.task_sents_html)
            }
        })
})

$('.lang-puzzle-words-right').on('click', '.btn-close', e => {
    e.preventDefault()

    let delButton = e.target

    let wrongWord = delButton.parentElement.parentElement
    let taskPk = parseInt(wrongWord.dataset.task_pk)
    let wordIdx = parseInt(wrongWord.dataset.word_idx)

    $.ajax(
        {
            url: `/adminpanel/structure/tasks/update_with_ajax/${taskPk}/?remove_lang_puzzle_word_right=${wordIdx}`,
            success: data => {
                $('.lang-puzzle-words-right').html(data.lang_puzzle_words_right_html)
            }
        })
})

$('.lang-puzzle-words-wrong').on('click', '.btn-close', e => {
    e.preventDefault()

    let delButton = e.target

    let wrongWord = delButton.parentElement.parentElement
    let taskPk = parseInt(wrongWord.dataset.task_pk)
    let wordIdx = parseInt(wrongWord.dataset.word_idx)

    $.ajax(
        {
            url: `/adminpanel/structure/tasks/update_with_ajax/${taskPk}/?remove_lang_puzzle_word_wrong=${wordIdx}`,
            success: data => {
                $('.lang-puzzle-words-wrong').html(data.lang_puzzle_words_wrong_html)
            }
        })
})

$('.sent-images').on('click', '.btn-close', e => {
    e.preventDefault()

    let delButton = e.target

    let sentImage = delButton.parentElement.parentElement
    let taskPk = parseInt(sentImage.dataset.task_pk)
    let sentImageIdx = parseInt(sentImage.dataset.sent_image_idx)

    $.ajax(
        {
            url: `/adminpanel/structure/tasks/update_with_ajax/${taskPk}/?remove_sent_image_idx=${sentImageIdx}`,
            success: data => {
                $('.sent-images').html(data.sent_images_html)
            }
        })
})

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


