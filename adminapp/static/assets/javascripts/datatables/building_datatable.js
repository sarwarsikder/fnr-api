$(document).ready(function () {
    var show_entries = $('#show_entries').val();
    var sorted_column = $('#sorted_column_stand').val();
    var sorting_order = $('#sorting_order_stand').val();
    var csrf_token = $('input[name=csrfmiddlewaretoken]').val();
    var data = {
        csrfmiddlewaretoken: csrf_token
    };
    var $dataTableContainer = $('#buildings-table');
    $dataTableContainer.show();
    $('body .loader').show();
    var buildings_table = $dataTableContainer.DataTable({
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
                "targets": 4,
                'render': function (data, type, full, meta) {
                    var flat_url = base_url+"/buildings/"+full[0]+"/flats/";
                    var updateUrl = base_url+"/buildings/update/"+full[0]+"/";
                    var qr_url = base_url+"/buildings/qr/"+full[0]+"/";
                    var actions = '<a href="'+updateUrl+'" class="btn btn-primary btn-lil building-info" data-toggle="tooltip" data-placement="top" title="Edit Hause" data-original-title="Edit"><i class="fa fa-edit"></i></a>'+
                                  '<a href="'+flat_url+'" class="btn btn-primary btn-lil building-flats" data-toggle="tooltip" data-placement="top" title="Hause Whonung"><i class="fas fa-door-closed"></i></a>'+
                                  '<a href="tasks-building.php" class="btn btn-info btn-lil" data-toggle="tooltip" data-placement="top" title="Tasks"><i class="fa fa-list"></i></a>'+
                                  '<a href="'+qr_url+'" class="btn btn-primary btn-lil building-qr" target="_blank" data-toggle="tooltip" data-placement="top" title="Preview QR" data-original-title="Edit"><i class="fa fa-qrcode"></i></a>'+
                                  '<button class="btn btn-danger btn-lil delete-building" disabled data-id="'+full[0]+'" data-toggle="tooltip" data-placement="top" title="Delete Hause" data-original-title="Delete"><i class="fa fa-times-circle"></i></button>';
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
            'url': BUILDING_LIST_JSON_URL,
            'data': data
        },
        "initComplete": function () {
            $('body .loader').hide()
        }
    });
});