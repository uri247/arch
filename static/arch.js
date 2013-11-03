
function page_projects()
{
    var firmid = location.pathname.match(/\/(.*?)\//)[1];
    var projects;
    var filter;

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
            var $elem = $('<div class="nav-menu-item" data-cls="' + cls_ndx + '">' + cls.he + '</div>');
            $elem.click(onFilterClick);
            $('.a-pane').append($elem)
        });
    }

    function update_filter(_filter) {
        // remove class from previous selection
        $('.nav-menu-item-selected').removeClass('nav-menu-item-selected');

        // set class to current selection
        filter = _filter;
        $('.nav-menu-item[data-cls=' + filter + ']').addClass('nav-menu-item-selected');
        $('.plural-well').empty();

        // go through all projects in this specific class
        classifications[filter].p.forEach( function(proj) {
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
        $('.single-well').hide();
        $('.plural-well').show();
        update_filter( $(this).data('cls') );
    };

    function onProjectClick() {
        $('.plural-well').hide();
        $('.single-well').show();
        update_single($(this).data('projid'));
        //return false;
    }

    function update_single(projid) {
        $('.single-well').append( $('<div>' + projid + '</div>') );
    }
}