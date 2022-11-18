$(document).ready(function(){
    var modal = '<div id="myModal" class="modal fade" tabindex="-1">';
        modal += '<div class="modal-dialog modal-lg">';
        modal += '<div class="modal-content">';

        modal += '<div class="modal-header">';
        modal += '<h5 class="modal-title">Compressed file content</h5>';
        modal += '<button type="button" class="close" data-dismiss="modal">&times;</button>';
        modal += '</div>'; //header

        modal += '<div class="modal-body" id="modal-body">';
        // return jquery.request here!
        modal += '</div>'; // body

        modal += '<div class="modal-footer">';
        modal += '<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>';
        modal += '</div>'; //footer

        modal += '</div>'; //content
        modal += '</div>'; //dialog
        modal += '</div>'; //myModal
    $('#content').append(modal);

    /* when clicked button 'show!'
     * 1 request URL from API and return a HTML code
     * 2 open modal for display compressed content of file */
    $(".btn").click(function(){
        id = this.id;
        search = $('input#searchbar').val();
        // empty
        if (search == ''){
            search = 'None';
        }
        // build modal
        $.get('/api/' + id + '/' + search + '/',
            function(data){
                $('#modal-body').html(data)
            }
        );
        // open modal
        $("#myModal").modal('show');
    });

}) // document
