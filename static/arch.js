
function page_projects()
{
    var firmid;
    var lang;
    var projects;
    var current_classification;
    var current_project;

    this.main = function main() {
        // global variables from URL
        var rx = location.pathname.match(/\/(.*?)\//);
        firmid = rx[1];
        lang = rx[2];

        // get list of projects.
        $.getJSON( '/api/project/' + firmid + '/',
            function onProjectsJson(projs) {
                projects = projs;
                current_classification = 'all';
                update_projects();
                update_filter();
            }
        );
    };

    function classify(proj, cls ) {
        if( cls && cls != "" ) {
            classifications[cls].p.push(proj);
        }
    }

    function update_projects() {
        /* Build the classifications global. This is a map that group all projects to
        the appropriate class (Office, Residential, etc.).
        */
        projects.forEach(function (proj) {
          classify(proj, proj.classification);
          classify(proj, proj.classification2);
          classify(proj, 'all');
        });
        classifications_order.forEach(function (cls_ndx) {
            var cls = classifications[ cls_ndx ];
            var $elem = $('<div class="nav-menu-item" data-classification="' + cls_ndx + '">' + cls.he + '</div>');
            $elem.click(onFilterClick);
            $('.a-pane').append($elem)
        });
    }

    function update_filter() {
        // change style for the classification a pane.
        $('.nav-menu-item-selected').removeClass('nav-menu-item-selected');
        $('.nav-menu-item[data-cls=' + current_classification + ']').addClass('nav-menu-item-selected');

        // go through all projects in this specific class
        classifications[current_classification].p.forEach( function(proj) {
            var $projElem = $('<div class="cat-img-well">' +
                '<a data-projid="' + proj.id + '" href="#proj=' + proj.id + '">' +
                '<img class="cat-img" src="' + proj.front_picture_url + '">' +
                '</a>' +
                '</div>\n');
            $('.plural-well').append($projElem);
        });
        $('.cat-img-well').filter(':nth-child(4n)').addClass('cat-img-well-eol');
        $('.cat-img-well a').click( function() { setSingleProject( $(this).data('projid') ); } );
    }

    function onFilterClick() {
        setClassification( $(this).data('classification') );
    }

    function setClassification(clsf) {
        current_classification = clsf;
        window.location.hash = 'class=' + current_classification;
        $('.single-well').hide();
        $('.plural-well').empty().show();
        update_filter( );
    }

    function setSingleProject(projid) {
        $('.plural-well').hide();
        $('.transbox-value').empty();
        $('.single-title').empty();
        $('#kar-well').empty();
        $('.single-well').show();
        $.getJSON(
            '/api/project/' + firmid + '/' + projid,
            function (proj) {
                update_single(proj);
            }
        );

        return false;
    }

    function update_single(proj) {
        current_project = proj;
        $('.single-title').text( proj.title_h );
        $('#address').text( proj.address_h );
        $('#classification').text( proj.classification);
        $('#plot_area').text( proj.plot_area );
        $('#built_area').text( proj.built_area );
        $('#units').text( proj.units );
        $('#year').text( proj.year );
        $('#status').text( proj.status );
        $('#client').text( proj.client_id );
        $('#description').text( proj.description_h );
        build_carousel( proj )
    }


    function build_carousel(proj) {

        $('.carousel').carousel('pause');

        // prepare the carousel well
        var innerHTML = '<div id="karusela" class="carousel slide"><div class="carousel-inner">';
        for (var i = 0; i < proj.images.length; ++i) {
            innerHTML += '<div class="item"><img src="' + proj.images[i].large_url + '" /></div>';
        }
        innerHTML += '</div>';
        innerHTML += '</div>';
        $('#kar-well').html(innerHTML);

        // prepare the indicators well
        innerHTML = '';
        for (var i = 0; i < proj.images.length; ++i) {
            innerHTML += '<div data-to="' + i.toString() + '"><span>' + (i + 1).toString() + '</a></div>';
        }
        $('#indicators').html(innerHTML);

        $('#karusela .item:first').addClass('active');
        $('#indicators div:first').addClass('active');

        $('#indicators div').click(function (q) {
          q.preventDefault();
          var clicked = $(this).data('to');
          $('#karusela').carousel(clicked);
        });

        $('#karusela').carousel({ interval: 5000 });

        $('.carousel').on('slide', function onSlide(evt) {
          $('#indicators div').removeClass('active');
        });

        $('.carousel').on('slid', function onSlid(evt) {
            var $k = $(evt.currentTarget);
            var $active = $k.find('.active');
            var $items = $active.parent().children();
            var index = $items.index($active);

            var $indicators = $('#indicators div');
            var ind_index = index;
            $($indicators[ind_index]).addClass('active');
        });

      }

    function findProjectInList( list, proj )
    {
        for( var index=0; index < list.length; ++index ) {
            if( list[index].id === proj.id ) {
                break;
            }
        }
        return index;
    }


    $('.arrow-left, .arrow-right').click( function() {
        var current_list = classifications[current_classification].p;
        var index = findProjectInList(current_list, current_project);

        var direction = $(this).data('direction')
        var next_index = index + direction;

        if( next_index >= 0 && next_index < current_list.length ) {
            var next_project = current_list[ index + direction ];
            setSingleProject( next_project.id );
        }
    })

    $('.arrow-up').click( function() {
        setClassification(current_classification);
    })


}
