function buildPagination() {
    $("#budget-expenses-table-wrapper").after('<div class="table-nav" id="nav"></div>');
    var rowsShown = 50;
    var rowsTotal = $('#expenses-table tbody tr').length;
    var numPages = rowsTotal / rowsShown;
    for (i = 0; i < numPages; i++) {
        var pageNum = i + 1;
        $('#nav').append('<button class="table-page-butt" href="#" rel="' + i + '">' + pageNum + '</button> ');
    }
    $('#expenses-table tbody tr').hide();
    $('#expenses-table tbody tr').slice(0, rowsShown).show();
    $('#nav button:first').addClass('active');
    $('#nav button:first').addClass('target');
    $('#nav button').bind('click', function () {

        $('#nav button').removeClass('active');
        $('#nav button').removeClass('target');
        $(this).addClass('active');
        $(this).addClass('target');
        var currPage = $(this).attr('rel');
        var startItem = currPage * rowsShown;
        var endItem = startItem + rowsShown;
        $('#expenses-table tbody tr').css('opacity', '0.0').hide().slice(startItem, endItem).
            css('display', 'table-row').animate({ opacity: 1 }, 300);
    });
};