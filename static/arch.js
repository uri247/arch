
function page_projects()
{
    var firmid = location.pathname.match(/\/(.*?)\//)[1];
    var projects;
    var current_classification = 'all';

    this.main = function main() {
        $.getJSON( '/api/project/' + firmid + '/',
            function onProjectsJson(projs) {
                projects = projs;
                current_classification = 'all';
                update_projects();
                update_filter();
            }
        );
    }

    function classify(proj, cls ) {
        if( cls != "" ) {
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
        $('.cat-img-well a').click( onProjectClick );
    }

    function onFilterClick() {
        current_classification = $(this).data('classification');
        window.location.hash = 'class=' + current_classification;
        $('.single-well').hide();
        $('.plural-well').empty().show();
        update_filter( );
    };

    function onProjectClick() {
        $('.plural-well').hide();
        $('.single-img').css('background-image', 'none');
        $('.transbox-value').empty();
        $('.single-well').show();
        var projid = $(this).data('projid');
        $.getJSON(
            '/api/project/' + firmid + '/' + projid,
            function (proj) {
                update_single(proj);
            }
        );

        return false;
    }

    function add_to_transbox(name, value) {
        $('.transbox').append( '<div><span class="transbox-name">' + name +
            '</span><span class="transbox-value">' + value + '</span></div>' );
    }

    function update_single(proj) {
        $('.single-img').css( 'background-image', 'url(' + proj.images[0].large_url + ')' );
        $('.single-title').text( proj.title_h );
        $('#address').text( proj.address_h );
        $('#classification').text( proj.classification);
        $('#plot_area').text( proj.plot_area );
        $('#built_area').text( proj.built_area );
        $('#units').text( proj.units );
        $('#year').text( proj.year );
        $('status').text( proj.status );
        $('client').text( proj.client_id );
        $('description').text( proj.description_h );
    }
}