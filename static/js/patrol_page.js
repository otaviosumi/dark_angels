 document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.sidenav');
    var instances = M.Sidenav.init(elems, options);
  });

function trClick(row) {              
    console.log(row.children[0].innerHTML);
    document.location.href = "patrol_page/" + row.children[0].innerHTML;
}

