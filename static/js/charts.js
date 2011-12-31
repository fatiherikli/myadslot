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
            "type" : "column",
            "width" : 800,
            "height" : 250,
            "title" : '',
            "v_axis" : 'Count',
            "h_axis" : 'Time',
            "is3D" : true,
            "chart_data" : {
                "rows" : [],
                "columns" : []
            }
        }, _settings || {});

//        chart_type = {
//            "column" : google.visualization.ColumnChart
//        }[settins.type]

        var prepare_chart = function (dom_element) {
            chart_type = {
                "column" : google.visualization.ColumnChart,
                "line" : google.visualization.LineChart,
                "area" : google.visualization.AreaChart,
                "pie" : google.visualization.PieChart,
                "gauge" : google.visualization.Gauge,
                "bar" : google.visualization.BarChart
            }
            return new chart_type[settings.type](dom_element)
        }

        var data = new google.visualization.DataTable();
        $(settings.chart_data.columns).each(function () {
            data.addColumn(this[0], this[1]);
        })
        data.addRows(settings.chart_data.rows);

        var options = {
            width: settings.width, height: settings.height,
            title: settings.title,
            is3D : settings.is3D,
            vAxis: { title: settings.v_axis },
            hAxis: { title: settings.h_axis }

        };


        this.each(function () {
            var chart = prepare_chart(this);
            chart.draw(data, options);
        })
    }

})(jQuery)





