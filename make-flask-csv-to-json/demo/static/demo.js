'use strict';

// CSV取込ボタン押下処理
function import_csv(){
    let form = document.getElementsByTagName("form")[0];
    let csv_file = document.getElementById("csv_file").value
    if(!csv_file){
        alert("取り込むCSVファイルを選択してください");
        return;
    }
    if(csv_file.substr(-4).toLowerCase() != ".csv"){
        alert("ファイルの拡張子がCSVファイルでありません");
        return;
    }
    let csv_file_obj = document.getElementById("csv_file").files[0];
    if(csv_file_obj.size == 0){
        alert("CSVファイルが空になっています");
        return;
    }
    form.action="/import-csv";
    form.method="post";
    form.submit();
}
