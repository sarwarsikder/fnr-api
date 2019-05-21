$(document).ready(function () {
    var show_entries = $('#show_entries').val();
    var sorted_column = $('#sorted_column_stand').val();
    var sorting_order = $('#sorting_order_stand').val();
    var csrf_token = $('input[name=csrfmiddlewaretoken]').val();
    var data = {
        csrfmiddlewaretoken: csrf_token
    };
    var $dataTableContainer = $('#projects-table');
    $dataTableContainer.show();
    $('body .loader').show();
    var projects_table = $dataTableContainer.DataTable({
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
                "orderable": true,
                "searchable": true,
                "className": "",
                "targets": 4,
                'render': function (data, type, full, meta) {
                    var start_date = moment(full[4]).format("Do MMM,YYYY");
                    return start_date;
                }
            },
            {
                "orderable": true,
                "searchable": true,
                "className": "",
                "targets": 5,
                'render': function (data, type, full, meta) {
                    var end_date = moment(full[5]).format("Do MMM,YYYY");
                    return end_date;
                }
            },
            {
                "orderable": false,
                "searchable": false,
                "className": "",
                "targets": 6,
                'render': function (data, type, full, meta) {
                    var building_url = base_url+"/projects/"+full[0]+"/buildings/";
                    if(full[6] == 'False'){
                        var actions = '<a href="'+building_url+'" class="btn btn-primary btn-lil project-buildings" data-toggle="tooltip" data-placement="top" title="Project Hauser"><i class="fa fa-building"></i></a>';
                        return actions;
                    }else{
                        var updateUrl = base_url+"/projects/update/"+full[0]+"/";
                        var actions = '<a href="'+updateUrl+'" class="btn btn-primary btn-lil project-info" data-toggle="tooltip" data-placement="top" title="Edit Project" data-original-title="Edit"><i class="fa fa-edit"></i></a>'+
                                      '<a href="'+building_url+'" class="btn btn-primary btn-lil project-buildings" data-toggle="tooltip" data-placement="top" title="Project Hauser"><i class="fa fa-building"></i></a>'+
                                      '<button class="btn btn-danger btn-lil delete-project" data-id="'+full[0]+'" data-toggle="tooltip" data-placement="top" title="Delete Project" data-original-title="Delete"><i class="fa fa-times-circle"></i></button>';
                        return actions;
                    }
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
            'url': PROJECT_LIST_JSON_URL,
            'data': data
        },
        "initComplete": function () {
            $('body .loader').hide()
        }
    });
});