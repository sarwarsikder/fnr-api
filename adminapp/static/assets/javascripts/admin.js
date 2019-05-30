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
        var project_id = $this.val(),
            csrfToken = $('input[name=csrfmiddlewaretoken]').val();
        $.ajax({
            url: base_url + '/current-buildings/',
            type: 'POST',
            data: {
                'project_id': project_id,
                'change_project': true,
                'csrfmiddlewaretoken': csrfToken
            },
            success: function (responseText) {
                var response = responseText;
                if (response.success) {
                    window.location.href  = base_url + '/current-project-buildings/';
                    // var current_buildings = "";
                    // current_buildings = addSidebarBuildingOrFlats(response.current_buildings, 'building', current_buildings);
                    // $("#current-buildings").html(current_buildings);
                    // $(".content-wrapper").html(response.building_list_tab);
                }
            },
            error: function (e) {
                clog(e);
            }
        });
    });

    $body.on('click', '#current-project-buildings', function () {
        window.location.href  = base_url + '/current-project-buildings/';
    });

    $body.on('click', '#current-project-flats', function () {
        window.location.href  = base_url + '/current-project-flats/';
    });

    $body.on('click', '#current-project-plan-list', function () {
        var csrfToken = $('input[name=csrfmiddlewaretoken]').val();
        $('.loader').show();
        $.ajax({
            url: base_url + '/project-plans/',
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrfToken
            },
            success: function (responseText) {
                var response = responseText;
                if (response.success) {
                    $("#current-plan-list-tab").html(response.plan_list_tab);
                }
                $('.loader').hide();
            },
            error: function (e) {
                clog(e);
                $('.loader').hide();
            }
        });
    });

    $body.on('click', '#current-building-plan-list', function () {
        var csrfToken = $('input[name=csrfmiddlewaretoken]').val();
        $('.loader').show();
        $.ajax({
            url: base_url + '/building-plans/',
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrfToken
            },
            success: function (responseText) {
                var response = responseText;
                if (response.success) {
                    clog(response.plan_list_tab)
                    $("#current-plan-list-tab").html(response.plan_list_tab);
                }
                $('.loader').hide();
            },
            error: function (e) {
                clog(e);
                $('.loader').hide();
            }
        });
    });

    $body.on('click', '#nav-building-plan-list-tab', function () {
        var csrfToken = $('input[name=csrfmiddlewaretoken]').val();
        var url = window.location.pathname.split("/");
        var building_id = url[2];
        $('.loader').show();
        $.ajax({
            url: base_url + '/building-plans/',
            type: 'POST',
            data: {
                'building_id': building_id,
                'csrfmiddlewaretoken': csrfToken
            },
            success: function (responseText) {
                var response = responseText;
                if (response.success) {
                    clog(response.plan_list_tab)
                    $("#current-plan-list-tab").html(response.plan_list_tab);
                }
                $('.loader').hide();
            },
            error: function (e) {
                clog(e);
                $('.loader').hide();
            }
        });
    });

    $body.on('click', '#nav-flat-plan-list-tab', function () {
        var csrfToken = $('input[name=csrfmiddlewaretoken]').val();
        var url = window.location.pathname.split("/");
        var flat_id = url[2];
        $('.loader').show();
        $.ajax({
            url: base_url + '/flat-plans/',
            type: 'POST',
            data: {
                'flat_id': flat_id,
                'csrfmiddlewaretoken': csrfToken
            },
            success: function (responseText) {
                var response = responseText;
                if (response.success) {
                    clog(response.plan_list_tab)
                    $("#current-plan-list-tab").html(response.plan_list_tab);
                }
                $('.loader').hide();
            },
            error: function (e) {
                clog(e);
                $('.loader').hide();
            }
        });
    });

    $body.on('click', '.delete-project-plan', function () {
        var $this = $(this);
        var id = $this.data('id'),
            csrfToken = $('input[name=csrfmiddlewaretoken]').val();
        bootbox.confirm("Are you sure you want to delete this Plan?", function (result) {
            if (result) {
                $.ajax({
                    url: base_url + '/project-plan/delete/',
                    type: 'POST',
                    data: {
                        'id': id,
                        'csrfmiddlewaretoken': csrfToken
                    },
                    success: function (responseText) {
                        var response = responseText;
                        if (response.success) {
                            $.growl.notice({message: response.message});
                            $this.closest('.plan-div').remove();
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

    $body.on('click', '.delete-building-plan', function () {
        var $this = $(this);
        var id = $this.data('id'),
            csrfToken = $('input[name=csrfmiddlewaretoken]').val();
        bootbox.confirm("Are you sure you want to delete this Plan?", function (result) {
            if (result) {
                $.ajax({
                    url: base_url + '/building-plan/delete/',
                    type: 'POST',
                    data: {
                        'id': id,
                        'csrfmiddlewaretoken': csrfToken
                    },
                    success: function (responseText) {
                        var response = responseText;
                        if (response.success) {
                            $.growl.notice({message: response.message});
                            $this.closest('.plan-div').remove();
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

    $body.on('click', '.delete-flat-plan', function () {
        var $this = $(this);
        var id = $this.data('id'),
            csrfToken = $('input[name=csrfmiddlewaretoken]').val();
        bootbox.confirm("Are you sure you want to delete this Plan?", function (result) {
            if (result) {
                $.ajax({
                    url: base_url + '/flat-plan/delete/',
                    type: 'POST',
                    data: {
                        'id': id,
                        'csrfmiddlewaretoken': csrfToken
                    },
                    success: function (responseText) {
                        var response = responseText;
                        if (response.success) {
                            $.growl.notice({message: response.message});
                            $this.closest('.plan-div').remove();
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

});

function getAllCurrentBuildingsByProject($this) {
    var project_id = $this.val(),
        csrfToken = $('input[name=csrfmiddlewaretoken]').val();
    $('.loader').show();
    $.ajax({
        url: base_url + '/current-buildings/',
        type: 'POST',
        data: {
            'project_id': project_id,
            'change_project': false,
            'csrfmiddlewaretoken': csrfToken
        },
        success: function (responseText) {
            var response = responseText;
            if (response.success) {
                var current_buildings = "";
                current_buildings = addSidebarBuildingOrFlats(response.current_buildings, 'building', current_buildings);
                $("#current-buildings").html(current_buildings);
                activePlanTab();
                activeSubMenu();
            }
            $('.loader').hide();
        },
        error: function (e) {
            clog(e);
            $('.loader').hide();
        }
    });
}

function getAllCurrentFlatsByBuilding() {
    var csrfToken = $('input[name=csrfmiddlewaretoken]').val();
    $('.loader').show();
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
                current_flats = addSidebarBuildingOrFlats(response.current_flats, 'flat', current_flats);
                $("#current-flats").html(current_flats);
                activeSubMenu();
            }
            $('.loader').hide();
        },
        error: function (e) {
            clog(e);
            $('.loader').hide();
        }
    });
}

function addSidebarBuildingOrFlats(data, type, sidebarElem) {
    $.map(data, function (elementArray, indexArray) {
        var task_url = base_url+"/buildings/"+elementArray.id+"/tasks/";
        if(type == "flat"){
            task_url = base_url+"/flats/"+elementArray.id+"/tasks/";
        }
        var elem = '<li class="nav-item">' +
            '<a href="'+task_url+'" class="nav-link">' +
            '<i class="fa fa-chevron-right nav-icon"></i>' +
            '<p>' + elementArray.number + '</p>' +
            '</a>' +
            '</li>';
        sidebarElem += elem;
    });
    return sidebarElem;
}

function activeSubMenu() {
    var url = window.location.pathname;
    if(url != "/") {
        $('.has-treeview').removeClass('menu-open');
        $("a[href$='" + url + "']").closest('li.has-treeview').addClass("menu-open");
        $('.has-treeview').find("a[href$='" + url + "']").addClass("active");
    }

}

function activePlanTab(){
    var current_url = window.location.href;
    var activeTab = current_url.substring(current_url.indexOf("#") + 1);
    if (activeTab == "plans") {
        $('a[href="#current-plan-list-tab"]').trigger('click');
    }
}