$(function () {
    var $body = $('body');

    $body.on('click', '.delete-staff', function () {
        var $this = $(this);
        var id = $this.data('id'),
            csrfToken = $('input[name=csrfmiddlewaretoken]').val();
        bootbox.confirm("Are you sure you want to delete this Staff?", function (result) {
            if (result) {
                $.ajax({
                    url: base_url + '/staffs/delete/',
                    type: 'POST',
                    data: {
                        'id': id,
                        'csrfmiddlewaretoken': csrfToken
                    },
                    success: function (responseText) {
                        var response = responseText;
                        if (response.success) {
                            $.growl.notice({message: response.message});
                            var table = $('#staffs-table').DataTable();
                            table.row($this.closest('tr')).remove().draw();
                        } else {
                            $.growl.error({message: response.message});
                        }
                    },
                    error: function (e) {
                        clog(e);
                    }
                });
            }
        });
    });

    // $body.on('change', '.inquiry_status', function () {
    //     var $this = $(this);
    //     var status = 0;
    //     if ($this.is(':checked')) {
    //         status = 1;
    //     }
    //     var id = $this.data('id'),
    //         csrfToken = $('input[name=csrfmiddlewaretoken]').val();
    //     $.ajax({
    //         url: admin_url + '/inquiries/change-status/',
    //         type: 'POST',
    //         data: {
    //             'id': id,
    //             'status': status,
    //             'csrfmiddlewaretoken': csrfToken
    //         },
    //         success: function (responseText) {
    //             var response = responseText;
    //             if (response.success) {
    //                 $.growl.notice({message: response.message});
    //             } else {
    //                 $.growl.error({message: response.message});
    //             }
    //         },
    //         error: function (e) {
    //             clog(e);
    //         }
    //     });
    // });

});