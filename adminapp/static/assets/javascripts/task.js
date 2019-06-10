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
                        activePlanTab();
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

    $body.on('click', '.edit_assign_task', function () {
        var component_id = $(this).attr('data-component-id');
        var handworker_id = $(this).attr('data-handworker-id');
        var building_component_id = $(this).attr('data-id');
        var csrfToken = $('input[name=csrfmiddlewaretoken]').val();
        var data = {
            'component_id': component_id,
            'csrfmiddlewaretoken': csrfToken
        };
        var $button = $("#submit-handworker-assign");
        $button.prop("disabled", true);
        $('.loader').show();
        $.ajax({
            url: base_url + '/get-handworker-list/',
            type: 'POST',
            data: data,
            success: function (response) {
                if (response.success) {
                    $("#component-assigned-handwerker").html('').select2({data: response.handworkers});
                    if(isNotEmpty(handworker_id)){
                        $("#component-assigned-handwerker").select2("val", handworker_id);
                    }
                    $button.prop("disabled", false);
                    $button.attr("data-id", building_component_id);
                }
                $('.loader').hide();
            },
            error: function (e) {
                clog(e);
                $('.loader').hide();
            }
        });
    });

    $body.on('click', '#submit-handworker-assign', function () {
        var component_id = $(this).attr('data-id');
        var user_id = $("#component-assigned-handwerker").val();
        var csrfToken = $('input[name=csrfmiddlewaretoken]').val();
        var data = {
            'component_id': component_id,
            'user_id': user_id,
            'csrfmiddlewaretoken': csrfToken
        };
        $('.loader').show();
        $.ajax({
            url: base_url + '/assign-handworker/',
            type: 'POST',
            data: data,
            success: function (response) {
                if (response.success) {
                    var $elem = $(".edit_assign_task[data-id="+component_id+"]").closest(".td_assign_to");
                    if(response.handworker.avatar){
                        $elem.find(".assignee-handwerker-image").attr("src", response.handworker.avatar);
                    }
                    $elem.find(".assignee-handwerker-name").html(response.handworker.fullname);
                    $("#assignee-handwerker-modal").modal('hide');
                }
                $('.loader').hide();
            },
            error: function (e) {
                clog(e);
                $('.loader').hide();
            }
        });
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