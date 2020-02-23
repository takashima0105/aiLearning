function displayResize() {

    var max_width = window.innerWidth * 0.7;

    var graphDiv = document.getElementsByClassName('plotly-graph-div');

    var svg_container = document.getElementsByClassName('svg-container');

    Array.prototype.forEach.call(svg_container, function(svg) {
        svg.style.width = max_width;
    });

    Array.prototype.forEach.call(graphDiv, function(div) {
        Plotly.relayout(div, {
            width: max_width,
        });
    });

}

$(window).load(function() {
    displayResize();
});

var timer = false;
$(window).resize(function() {
    if (timer !== false) {
        clearTimeout(timer);
    }
    timer = setTimeout(function() {
        displayResize();
    }, 200);
});