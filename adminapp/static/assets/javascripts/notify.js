var notify_badge_class;
var notify_menu_class;
var notify_api_url;
var notify_fetch_count;
var notify_unread_url;
var notify_mark_all_unread_url;
var notify_refresh_period = 15000;
var consecutive_misfires = 0;
var registered_functions = [];

function fill_notification_badge(data) {
    var badges = document.getElementsByClassName(notify_badge_class);
    if (badges) {
        for(var i = 0; i < badges.length; i++){
            badges[i].innerHTML = data.unread_count;
        }
    }
}

function fill_notification_list(data) {
    var menus = document.getElementsByClassName(notify_menu_class);
    if (menus) {
        var messages = data.unread_list.map(function (item) {
            console.log(item.description)
            var message = "";
            var target_url = "";
            var id = item.id;
            if(typeof item.actor !== 'undefined'){
                if(item.description == '' || item.description == null){
                    item.description = base_url+"/static/assets/images/avatar5.png";
                }
                message = "<img src='"+item.description+"' class='img-circle img-sm' alt='User Image'/>";
            }
            if(typeof item.verb !== 'undefined'){
                message = message + " " + item.verb;
            }
            if(typeof item.target !== 'undefined'){
                target_url = base_url+"/tasks/"+item.target+"/";
            }
            if(typeof item.timestamp !== 'undefined'){
                // message = message + " " + item.timestamp;
                var date = new Date(item.timestamp);
                var delta = Math.round((+new Date - date) / 1000);

                var minute = 60,
                    hour = minute * 60,
                    day = hour * 24,
                    week = day * 7;

                var fuzzy;

                if (delta < 30) {
                    fuzzy = 'just then.';
                } else if (delta < minute) {
                    fuzzy = delta + ' seconds ago.';
                } else if (delta < 2 * minute) {
                    fuzzy = 'a minute ago.'
                } else if (delta < hour) {
                    fuzzy = Math.floor(delta / minute) + ' minutes ago.';
                } else if (Math.floor(delta / hour) == 1) {
                    fuzzy = '1 hour ago.'
                } else if (delta < day) {
                    fuzzy = Math.floor(delta / hour) + ' hours ago.';
                } else if (delta < day * 2) {
                    fuzzy = 'yesterday';
                }
                message = message +
                    '<span class="float-right text-muted text-sm">' + fuzzy+'</span>';
            }
            var notificationElem = '<div class="dropdown-divider"></div>'+
                                        '<a href="'+target_url+'" class="dropdown-item">' + message +
                                       '</a>'
            return notificationElem;
        }).join('')

        for (var i = 0; i < menus.length; i++){
            menus[i].innerHTML = messages;
        }
    }
}

function register_notifier(func) {
    registered_functions.push(func);
}

function fetch_api_data() {
    if (registered_functions.length > 0) {
        //only fetch data if a function is setup
        var r = new XMLHttpRequest();
        r.addEventListener('readystatechange', function(event){
            if (this.readyState === 4){
                if (this.status === 200){
                    consecutive_misfires = 0;
                    var data = JSON.parse(r.responseText);
                    registered_functions.forEach(function (func) { func(data); });
                }else{
                    consecutive_misfires++;
                }
            }
        })
        r.open("GET", notify_api_url+'?max='+notify_fetch_count, true);
        r.send();
    }
    if (consecutive_misfires < 10) {
        setTimeout(fetch_api_data,notify_refresh_period);
    } else {
        var badges = document.getElementsByClassName(notify_badge_class);
        if (badges) {
            for (var i = 0; i < badges.length; i++){
                badges[i].innerHTML = "!";
                badges[i].title = "Connection lost!"
            }
        }
    }
}

setTimeout(fetch_api_data, 1000);
// <button id="markread" class="btn btn-link" style="float: right" data-id="'+item.id+'">Mark As Read</button>