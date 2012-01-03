
    $(function () {
        $("#id_start_date, #id_end_date").datepicker({"dateFormat":'yy-mm-dd 00:00:00'} );
        $("#id_title").slugify("#id_slot");
        //todo: these functions should be at add_slot.html and add_advertisement.html


    })

