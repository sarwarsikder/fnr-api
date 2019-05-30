$(function () {
    var $body = $('body');
    getPendingComponents();

    $body.on('click', '#nav-done-task-tab', function () {
        var url = window.location.pathname.split("/");
        var csrfToken = $('input[name=csrfmiddlewaretoken]').val();
        var data = {
            'csrfmiddlewaretoken': csrfToken
        };
        if (url[1] == 'buildings') {
            data['building_id'] = url[2];
        } else {
            data['flat_id'] = url[2];
        }
        $('.loader').show();
        $.ajax({
            url: base_url + '/get-done-components/',
            type: 'POST',
            data: data,
            success: function (response) {
                if (response.success) {
                    $("#nav-done-task").html(response.components_list);
                }
                $('.loader').hide();
            },
            error: function (e) {
                clog(e);
                $('.loader').hide();
            }
        });
    });

    $body.on('click', '#nav-all-task-tab', function () {
        var url = window.location.pathname.split("/");
        var csrfToken = $('input[name=csrfmiddlewaretoken]').val();
        var data = {
            'csrfmiddlewaretoken': csrfToken
        };
        if (url[1] == 'buildings') {
            data['building_id'] = url[2];
        } else {
            data['flat_id'] = url[2];
        }
        $('.loader').show();
        $.ajax({
            url: base_url + '/get-all-components/',
            type: 'POST',
            data: data,
            success: function (response) {
                if (response.success) {
                    $("#nav-all-task").html(response.components_list);
                }
                $('.loader').hide();
            },
            error: function (e) {
                clog(e);
                $('.loader').hide();
            }
        });
    });

    $body.on('click', '.pending-component-accordion', function () {
        var $this = $(this);
        var id = $this.attr('data-id');
        var url = window.location.pathname.split("/");
        var csrfToken = $('input[name=csrfmiddlewaretoken]').val();
        var type = $this.closest('.nav-task-list').attr('data-type');
        var data = {
            'id': id,
            'csrfmiddlewaretoken': csrfToken,
            'type': type
        };
        if (url[1] == 'buildings') {
            data['building_id'] = url[2];
        } else {
            data['flat_id'] = url[2];
        }
        if ($('#pending-component-' + id).find('.task-list').find('a').length == 0) {
            $('.loader').show();
            $.ajax({
                url: base_url + '/get-component-tasks/',
                type: 'POST',
                data: data,
                success: function (response) {
                    if (response.success) {
                        $('#pending-component-' + id).find('.task-list').html(response.tasks_list);
                    }
                    $('.loader').hide();
                },
                error: function (e) {
                    clog(e);
                    $('.loader').hide();
                }
            });
        }
    });

    $body.on('click', '.done-component-accordion', function () {
        var $this = $(this);
        var id = $this.attr('data-id');
        var url = window.location.pathname.split("/");
        var csrfToken = $('input[name=csrfmiddlewaretoken]').val();
        var type = $this.closest('.nav-task-list').attr('data-type');
        var data = {
            'id': id,
            'csrfmiddlewaretoken': csrfToken,
            'type': type
        };
        if (url[1] == 'buildings') {
            data['building_id'] = url[2];
        } else {
            data['flat_id'] = url[2];
        }
        if ($('#done-component-' + id).find('.task-list').find('a').length == 0) {
            $('.loader').show();
            $.ajax({
                url: base_url + '/get-component-tasks/',
                type: 'POST',
                data: data,
                success: function (response) {
                    if (response.success) {
                        $('#done-component-' + id).find('.task-list').html(response.tasks_list);
                    }
                    $('.loader').hide();
                },
                error: function (e) {
                    clog(e);
                    $('.loader').hide();
                }
            });
        }
    });

    $body.on('click', '.all-component-accordion', function () {
        var $this = $(this);
        var id = $this.attr('data-id');
        var url = window.location.pathname.split("/");
        var csrfToken = $('input[name=csrfmiddlewaretoken]').val();
        var type = $this.closest('.nav-task-list').attr('data-type');
        var data = {
            'id': id,
            'csrfmiddlewaretoken': csrfToken,
            'type': type
        };
        if (url[1] == 'buildings') {
            data['building_id'] = url[2];
        } else {
            data['flat_id'] = url[2];
        }
        if ($('#all-component-' + id).find('.task-list').find('a').length == 0) {
            $('.loader').show();
            $.ajax({
                url: base_url + '/get-component-tasks/',
                type: 'POST',
                data: data,
                success: function (response) {
                    if (response.success) {
                        $('#all-component-' + id).find('.task-list').html(response.tasks_list);
                    }
                    $('.loader').hide();
                },
                error: function (e) {
                    clog(e);
                    $('.loader').hide();
                }
            });
        }
    });
});

function getPendingComponents() {
    var url = window.location.pathname.split("/");
    var csrfToken = $('input[name=csrfmiddlewaretoken]').val();
    var data = {
        'csrfmiddlewaretoken': csrfToken
    };
    if (url[1] == 'buildings') {
        data['building_id'] = url[2];
    } else {
        data['flat_id'] = url[2];
    }
    $('.loader').show();
    $.ajax({
        url: base_url + '/get-pending-components/',
        type: 'POST',
        data: data,
        success: function (response) {
            if (response.success) {
                $("#nav-pending-task").html(response.components_list);
            }
            $('.loader').hide();
        },
        error: function (e) {
            clog(e);
            $('.loader').hide();
        }
    });
}