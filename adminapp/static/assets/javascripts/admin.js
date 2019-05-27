$(function () {
    var $body = $('body');
    getAllCurrentBuildingsByProject($("#current-project"));
    getAllCurrentFlatsByBuilding();

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

    $body.on('click', '.delete-worker', function () {
        var $this = $(this);
        var id = $this.data('id'),
            csrfToken = $('input[name=csrfmiddlewaretoken]').val();
        bootbox.confirm("Are you sure you want to delete this Handworker?", function (result) {
            if (result) {
                $.ajax({
                    url: base_url + '/companies/delete/',
                    type: 'POST',
                    data: {
                        'id': id,
                        'csrfmiddlewaretoken': csrfToken
                    },
                    success: function (responseText) {
                        var response = responseText;
                        if (response.success) {
                            $.growl.notice({message: response.message});
                            var table = $('#workers-table').DataTable();
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

    $body.on('click', '.delete-component', function () {
        var $this = $(this);
        var id = $this.data('id'),
            csrfToken = $('input[name=csrfmiddlewaretoken]').val();
        bootbox.confirm("Are you sure you want to delete this Component?", function (result) {
            if (result) {
                $.ajax({
                    url: base_url + '/components/delete/',
                    type: 'POST',
                    data: {
                        'id': id,
                        'csrfmiddlewaretoken': csrfToken
                    },
                    success: function (responseText) {
                        var response = responseText;
                        if (response.success) {
                            $.growl.notice({message: response.message});
                            $this.closest('.row').remove();
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

    $body.on('click', '.delete-project', function () {
        var $this = $(this);
        var id = $this.data('id'),
            csrfToken = $('input[name=csrfmiddlewaretoken]').val();
        bootbox.confirm("Are you sure you want to delete this Project?", function (result) {
            if (result) {
                $.ajax({
                    url: base_url + '/projects/delete/',
                    type: 'POST',
                    data: {
                        'id': id,
                        'csrfmiddlewaretoken': csrfToken
                    },
                    success: function (responseText) {
                        var response = responseText;
                        if (response.success) {
                            $.growl.notice({message: response.message});
                            var table = $('#projects-table').DataTable();
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

    $body.on('click', '.delete-building', function () {
        var $this = $(this);
        var id = $this.data('id'),
            csrfToken = $('input[name=csrfmiddlewaretoken]').val();
        bootbox.confirm("Are you sure you want to delete this Hause?", function (result) {
            if (result) {
                $.ajax({
                    url: base_url + '/buildings/delete/',
                    type: 'POST',
                    data: {
                        'id': id,
                        'csrfmiddlewaretoken': csrfToken
                    },
                    success: function (responseText) {
                        var response = responseText;
                        if (response.success) {
                            $.growl.notice({message: response.message});
                            var table = $('#buildings-table').DataTable();
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

    $body.on('click', '.delete-flat', function () {
        var $this = $(this);
        var id = $this.data('id'),
            csrfToken = $('input[name=csrfmiddlewaretoken]').val();
        bootbox.confirm("Are you sure you want to delete this Wohnung?", function (result) {
            if (result) {
                $.ajax({
                    url: base_url + '/flats/delete/',
                    type: 'POST',
                    data: {
                        'id': id,
                        'csrfmiddlewaretoken': csrfToken
                    },
                    success: function (responseText) {
                        var response = responseText;
                        if (response.success) {
                            $.growl.notice({message: response.message});
                            var table = $('#flats-table').DataTable();
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

    $body.on('change', '.user-status-checkbox', function () {
        var $this = $(this);
        var status = 0;
        if ($this.is(':checked')) {
            status = 1;
        }
        var id = $this.closest('tr').data('id'),
            csrfToken = $('input[name=csrfmiddlewaretoken]').val();
        $.ajax({
            url: base_url + '/change-user-status/',
            type: 'POST',
            data: {
                'id': id,
                'status': status,
                'csrfmiddlewaretoken': csrfToken
            },
            success: function (responseText) {
                var response = responseText;
                if (response.success) {
                    $.growl.notice({message: response.message});
                } else {
                    $.growl.error({message: response.message});
                }
            },
            error: function (e) {
                clog(e);
            }
        });
    });

    $body.on('change', '.project-status-checkbox', function () {
        var $this = $(this);
        var status = 1;
        if ($this.is(':checked')) {
            status = 0;
        }
        var id = $this.closest('tr').data('id'),
            csrfToken = $('input[name=csrfmiddlewaretoken]').val();
        $.ajax({
            url: base_url + '/change-project-status/',
            type: 'POST',
            data: {
                'id': id,
                'status': status,
                'csrfmiddlewaretoken': csrfToken
            },
            success: function (responseText) {
                var response = responseText;
                if (response.success) {
                    $.growl.notice({message: response.message});
                } else {
                    $.growl.error({message: response.message});
                }
            },
            error: function (e) {
                clog(e);
            }
        });
    });

    $body.on('change', '#current-project', function () {
        var $this = $(this);
        getAllCurrentBuildingsByProject($this);
    });

});

function getAllCurrentBuildingsByProject($this) {
    var project_id = $this.val(),
        csrfToken = $('input[name=csrfmiddlewaretoken]').val();
    $.ajax({
        url: base_url + '/current-buildings/',
        type: 'POST',
        data: {
            'project_id': project_id,
            'csrfmiddlewaretoken': csrfToken
        },
        success: function (responseText) {
            var response = responseText;
            if (response.success) {
                var current_buildings = "";
                $.map(response.current_buildings, function (elementArray, indexArray) {
                    var elem = '<li class="nav-item">' +
                        '<a href=\"tasks.php\" class=\"nav-link\">' +
                        '<i class=\"fa fa-chevron-right nav-icon\"></i>' +
                        '<p>' + elementArray.number + '</p>' +
                        '</a>' +
                        '</li>';
                    current_buildings += elem;
                });
                $("#current-buildings").html(current_buildings);
            }
        },
        error: function (e) {
            clog(e);
        }
    });
}

function getAllCurrentFlatsByBuilding() {
    var csrfToken = $('input[name=csrfmiddlewaretoken]').val();
    $.ajax({
        url: base_url + '/current-flats/',
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': csrfToken
        },
        success: function (responseText) {
            var response = responseText;
            if (response.success) {
                var current_flats = "";
                $.map(response.current_flats, function (elementArray, indexArray) {
                    var elem = '<li class="nav-item">' +
                        '<a href=\"tasks.php\" class=\"nav-link\">' +
                        '<i class=\"fa fa-chevron-right nav-icon\"></i>' +
                        '<p>' + elementArray.number + '</p>' +
                        '</a>' +
                        '</li>';
                    current_flats += elem;
                });
                $("#current-flats").html(current_flats);
            }
        },
        error: function (e) {
            clog(e);
        }
    });
}