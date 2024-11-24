'use strict';

// 確認画面_送信ボタン押下処理
function send(){
    let form = document.getElementsByTagName("form")[0];
    form.action="/send";
    form.method="post";
    form.submit();
}

// 確認画面_戻るボタン押下処理
function back(){
    let form = document.getElementsByTagName("form")[0];
    form.action="/back";
    form.method="post";
    form.submit();
}
