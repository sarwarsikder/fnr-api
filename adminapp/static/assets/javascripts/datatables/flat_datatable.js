$(document).ready(function () {
    var show_entries = $('#show_entries').val();
    var sorted_column = $('#sorted_column_stand').val();
    var sorting_order = $('#sorting_order_stand').val();
    var csrf_token = $('input[name=csrfmiddlewaretoken]').val();
    var data = {
        csrfmiddlewaretoken: csrf_token
    };
    var $dataTableContainer = $('#flats-table');
    $dataTableContainer.show();
    $('body .loader').show();
    var flats_table = $dataTableContainer.DataTable({
        "bAutoWidth": true,
        "language": dt_language,
        "order": [
            [ sorted_column, sorting_order ]
        ],

        "lengthMenu": [
            [10, 25, 50, 100],
            [10, 25, 50, 100]
        ],
        "iDisplayLength": show_entries,
        "sDom": '<"dt_top" <"dt_left"f><"dt_right"l><"clear">>rt<"dt_bottom" <"dt_left"i><"dt_right"p><"clear">>',
        "createdRow": function (row, data, index) {
            $(row).attr('data-id', data[0]);
        },
        "columnDefs": [
            {
                "orderable": false,
                "searchable": false,
                "className": "",
                "targets": 5,
                'render': function (data, type, full, meta) {
                    var updateUrl = base_url+"/flats/update/"+full[0]+"/";
                    var actions = '<a href="'+updateUrl+'" class="btn btn-primary btn-lil flat-info" data-toggle="tooltip" data-placement="top" title="Edit Wohnung" data-original-title="Edit"><i class="fa fa-edit"></i></a>'+
                                  '<a href="tasks-flat.php" class="btn btn-info btn-lil" data-toggle="tooltip" data-placement="top" title="Tasks"><i class="fa fa-list"></i></a>'+
                                  '<button class="btn btn-danger btn-lil delete-flat" data-id="'+full[0]+'" data-toggle="tooltip" data-placement="top" title="Delete Wohnung" data-original-title="Delete"><i class="fa fa-times-circle"></i></button>';
                    return actions;
                }
            }
        ],
        "searching": true,
        "processing": true,
        "serverSide": true,
        "responsive": true,
        "destroy": true,
        "ajax": {
            'type': 'POST',
            'url': FLAT_LIST_JSON_URL,
            'data': data
        },
        "initComplete": function () {
            $('body .loader').hide()
        }
    });
});