function csv2Array(str) {
    var csvData = [];
    var lines = str.split("\n");
    for (var i = 0; i < lines.length; ++i) {
        var cells = lines[i].split(",");
        csvData.push(cells);
    }
    return csvData;
}

window.onload = function() {
    var grhc = document.getElementById("chart").getContext("2d");
    var fp = document.getElementById("id_outputFilePath")
    graphdisplay(fp);
};

function graphdisplay() {

}

function main() {
    // 1) ajaxでCSVファイルをロード
    var req = new XMLHttpRequest();
    var filePath = 'media/outputs/output.csv';
    req.open("GET", filePath, true);
    req.onload = function() {
        // 2) CSVデータ変換の呼び出し
        data = csv2Array(req.responseText);
        // 3) chart.jsデータ準備、4) chart.js描画の呼び出し
        drawBarChart(data);
    }
    req.send(null);
}

main();