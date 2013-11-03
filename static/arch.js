
function page_projects()
{
    var firmid = location.pathname.match(/\/(.*?)\//)[1];
    var projects;
    var current_classification = 'all';

    this.main = function main() {
        $.getJSON( '/api/project/' + firmid + '/',
            function onProjectsJson(_projects) {
                projects = _projects;
                update_projects();
                update_filter('all');
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
        $('.single-well').empty().show();
        var projid = $(this).data('projid');
        $.getJSON(
            '/api/project/' + firmid + '/' + projid,
            function (proj) {
                update_single(proj);
            }
        );

        return false;
    }

    function update_single(proj) {
        window.location.hash = 'proj=' + proj.id;
        $('.single-well').append( $('<div>' + proj.id + '</div>') );
        $('.single-well').append( $('<img src="' + proj.images[0].url + '">') );
    }
}