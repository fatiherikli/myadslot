/**
 * Author: Fatih Erikli
 * Date: 26.12.2011
 * ---------------------
 * Google Visualization jQuery Implemention
 */

(function ($) {

    $.fn.build_chart = function (_settings) {
        var settings = $.extend({
            // default options
            "width" : 800,
            "height" : 250,
            "title" : '',
            "v_axis" : 'Count',
            "h_axis" : 'Time'
        }, _settings || {});

        var data = new google.visualization.DataTable();
        $(settings.columns).each(function () {
            data.addColumn(this[0], this[1]);
        })
        data.addRows(settings.rows);

        var options = {
            width: settings.width, height: settings.height,
            title: settings.title,
            is3D : true,
            vAxis: { title: settings.v_axis },
            hAxis: { title: settings.h_axis }

        };

        this.each(function () {
            var chart = new google.visualization.ColumnChart(this);
            chart.draw(data, options);
        })
    }

})(jQuery)





