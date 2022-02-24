'use strict'

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
