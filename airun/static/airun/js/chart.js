function displayResize() {
    // var main_container = document.getElementById('content' + id).getElementsByClassName('svg-container')
    // var all_container = document.getElementsByClassName('main-svg');
    // var max_width = 0;
    // var max_height = 0;

    // Array.prototype.forEach.call(all_container, function(item) {
    //     if (max_width < item.width.baseVal.value) { max_width = item.width.baseVal.value; }
    //     if (max_height < item.height.baseVal.value) { max_height = item.height.baseVal.value; }
    // });

    // Array.prototype.forEach.call(main_container, function(item) {
    //     item.style.width = max_width + 'px';
    //     item.style.height = max_height + 'px';
    // });
    // svg_container.style.height = content_height + 'px';
    // Plotly.Plots.resize(gd);

    // var main_container = document.getElementById('content' + id).getElementsByClassName('svg-container')
    // var all_container = document.getElementsByClassName('main-svg');
    // var max_width = 0;
    // var max_height = 0;

    // Array.prototype.forEach.call(all_container, function(item) {
    //     if (max_width < item.width.baseVal.value) { max_width = item.width.baseVal.value; }
    //     if (max_height < item.height.baseVal.value) { max_height = item.height.baseVal.value; }
    // });

    var max_width = window.innerWidth - 250;

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