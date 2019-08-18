$(function () {
    var previous_status;
    var $body = $('body');
    getPendingComponents();

    $body.on('change', '#task-status-list', function (e) {
        var $this = $(this);
        var task_id = $this.attr('task-id');
        var status = $(this).children("option:selected").val();
        previous_status = $(this).attr('task-value');
        console.log(status);
        console.log(previous_status);
        changeTaskStatus($this, task_id, status, previous_status);
    });

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
                    if (isNotEmpty(handworker_id)) {
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
                    var $elem = $(".edit_assign_task[data-id=" + component_id + "]").closest(".td_assign_to");
                    if (response.handworker.avatar) {
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

    $body.on('click', '#save-task-description', function () {
        var url = window.location.pathname.split("/");
        var task_id = url[2];
        var description = $.trim($("#task-description").val());
        var csrfToken = $('input[name=csrfmiddlewaretoken]').val();
        var data = {
            'task_id': task_id,
            'description': description,
            'csrfmiddlewaretoken': csrfToken
        };
        $('.loader').show();
        $.ajax({
            url: base_url + '/save-task-description/',
            type: 'POST',
            data: data,
            success: function (response) {
                if (response.success) {
                    $("#task-description-text").html(description);
                    $.growl.notice({message: response.message});
                } else {
                    $.growl.error({message: response.message});
                }
                $('.loader').hide();
            },
            error: function (e) {
                clog(e);
                $('.loader').hide();
            }
        });
    });

    $body.on('click', '#save-task-followers', function () {
        var url = window.location.pathname.split("/");
        var task_id = url[2];
        var followers_data = $("#task-followers").select2('data');
        var followers = [];
        for (var i = 0; i < followers_data.length; i++) {
            followers.push({"id": followers_data[i].id, "name": followers_data[i].text});
        }
        var csrfToken = $('input[name=csrfmiddlewaretoken]').val();
        var data = {
            'task_id': task_id,
            'followers': JSON.stringify(followers),
            'csrfmiddlewaretoken': csrfToken
        };
        if(followers.length > 0){
            bootbox.confirm("Are you sure you want to add followers?", function (result) {
                if (result) {
                    $('.loader').show();
                    $.ajax({
                        url: base_url + '/add-task-followers/',
                        type: 'POST',
                        data: data,
                        success: function (response) {
                            if (response.success) {
                                $.growl.notice({message: response.message});
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
        }
    });


    $("#task-status").focus(function (e) {
        previous_status = $(this).val();
    }).change(function (e) {
        var url = window.location.pathname.split("/");
        var task_id = url[2];
        var status = $(this).val();
        changeTaskStatus($(this), task_id, status, previous_status);
    });

    /* var previous_status;
    $("#task-status").focus(function (e) {
        previous_status = $(this).val();
    }).change(function (e) {
        var url = window.location.pathname.split("/");
        var task_id = url[2];
        var status = $(this).val();
        var csrfToken = $('input[name=csrfmiddlewaretoken]').val();
        var data = {
            'task_id': task_id,
            'status': status,
            'csrfmiddlewaretoken': csrfToken
        };
        var changeConfirmation = confirm("Are you sure you want to change the status?");
        // bootbox.confirm("Are you sure you want to change the status?", function (result) {
        if (changeConfirmation) {
            $('.loader').show();
            $.ajax({
                url: base_url + '/change-task-status/',
                type: 'POST',
                data: data,
                success: function (responseText) {
                    var response = responseText;
                    $('.loader').hide();
                    if (response.success) {
                        $.growl.notice({message: response.message});
                    } else {
                        $.growl.error({message: response.message});
                    }
                },
                error: function (e) {
                    clog(e);
                    $('.loader').hide();
                }
            });
        } else {
            $("#task-status").val(previous_status);
        }
    }); */
    // });

    $('body').on('click', '#show-more-comments', function () {
        var page_number = $(this).attr('data-page-number');
        var url = window.location.pathname.split("/");
        var task_id = url[2];
        var csrf_token = $('input[name=csrfmiddlewaretoken]').val();
        $('.loader').show();
        var $this_button = $(this);
        $this_button.attr('disabled', true);
        $.ajax({
            url: base_url + '/get-more-comments/',
            type: "POST",
            data: {
                page_number: page_number,
                task_id: task_id,
                csrfmiddlewaretoken: csrf_token
            },
            success: function (result) {
                $this_button.attr('disabled', false);
                $('.loader').hide();
                if (result.success) {
                    $('.loader').hide();
                    if (result.total_comments > 0) {
                        $('#show-more-comments').attr('data-page-number', result.next_page_number);
                        $('#comments-list').append(result.new_lists);
                    }
                    if (!result.more_btn_visible) {
                        $this_button.hide();
                    }
                }
            },
            error: function (e) {
                $this_button.attr('disabled', false);
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

function changeTaskStatus($this, task_id, status, previous_status) {
    console.log('changing task status');
    var task_id = task_id;
    var csrfToken = $('input[name=csrfmiddlewaretoken]').val();
    var data = {
        'task_id': task_id,
        'status': status,
        'csrfmiddlewaretoken': csrfToken
    };
    var changeConfirmation = confirm("Are you sure you want to change the status?");
    // bootbox.confirm("Are you sure you want to change the status?", function (result) {
    if (changeConfirmation) {
        $('.loader').show();
        $.ajax({
            url: base_url + '/change-task-status/',
            type: 'POST',
            data: data,
            success: function (responseText) {
                var response = responseText;
                $('.loader').hide();
                if (response.success) {
                    $.growl.notice({ message: response.message });
                } else {
                    $.growl.error({ message: response.message });
                }
            },
            error: function (e) {
                clog(e);
                $('.loader').hide();
            }
        });
    } else {
        $this.val(previous_status);
    }

}