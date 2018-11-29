 document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.sidenav');
    var instances = M.Sidenav.init(elems, options);
  });

function ConsultaClick(row) {              
    console.log(row.children[0].innerHTML);
    document.location.href = "consulta_autuacao/" + row.children[0].innerHTML;
}

function AlteraConsultaClick(row) {              
    console.log(row.children[0].innerHTML);
    document.location.href = "altera_autuacao/" + row.children[0].innerHTML;
}

