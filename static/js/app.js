function show_proposal_tabs(ev){
    ev.preventDefault();
    $(this).tab('show');
}

function vote_click(){
    var $this = $(this);
    $this.siblings('input').val($this.data().val);
    $this.siblings().addClass('btn-default').removeClass('btn-success btn-warning btn-danger');
    $this.addClass({'0':'btn-danger', '1':'btn-warning', '2': 'btn-success'}[$this.data().val])
    $this.removeClass('btn-default');
    $('#save').attr('disabled', $('#vote-form input[value=-1]').length > 0);
    nominate_status()
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


function save_vote(ev){
    ev.preventDefault();
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                var csrftoken = $("[name=csrfmiddlewaretoken]").val();
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    $.post('vote/', $('#vote-form').serialize(), null, 'html').then(function(data){
        $('#existing-votes-block').remove();
        $('#user-vote-block').replaceWith(data);
    });
}

function table_sorter($table, data_src, row_template, extra_column_functions){
    var data = data_src,
        $body = $table.find('tbody'),
        extra_column_functions = extra_column_functions?extra_column_functions:{};

    function handle_click(ev){
        ev.preventDefault();
        var $this = $(this);
        if($this.hasClass('warning')){
            data = data.reverse();
        }else{
            $this.siblings().removeClass('warning');
            $this.addClass('warning');
            var column = $this.data().column;
            var value_function = function(x){
                return x[column];
            }
            if(extra_column_functions[column]){
                value_function = extra_column_functions[column]($this);
            }
            if (column){
                data = _.sortBy(data, value_function);
                if($this.data().reverse){
                    data = data.reverse();
                }
            }
        }
        render();
    }

    function render(){
        var result = '';
        for(var i=0; i < data.length; ++i){
            result += row_template({e:data[i], index:i});
        }
        $body.html(result);
    }

    $table.find('thead th').on('click', handle_click);
    $table.on('rerender', render);
    render();
}

TEMPLATES = {};


$(document).ready(function(){
    $('script[type="underscore/template"]').each(function(){
        var $this = $(this);
        TEMPLATES[$this.attr("id")] = _.template($this.text());
    });

    //Batch
    $('#proposal-tabs a').click(show_proposal_tabs);
    $('#unranked li').on('click', batch_add);
    $('#accept').on('click', 'li', batch_rem);
    $('#proposal-tabs a').first().tab("show");

    //Screening
    $('#right-column').on('click', '.voting-stripe button', vote_click);
    $('#right-column').on('click', '#save', save_vote);
    
    $('.tab-button').on('click', function(ev){
        console.log('click', $(this));
        ev.preventDefault();$(this).tab('show')
    });
});
