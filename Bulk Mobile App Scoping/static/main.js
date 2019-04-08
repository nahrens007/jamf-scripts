$("#checkAll").click(function() {
  $(".check").prop('checked', $(this).prop('checked'));
});

function categorySelect() {
  var category=$("#catsel").val();
  $("tr.approw").each(function(index, element) {
    // console.log(element.childNodes[9].innerText);
    var rowcat = element.childNodes[9].innerText; // get td with category
    if (category == rowcat) {
      element.childNodes[1].childNodes[1].setAttribute("checked", true);
    } else {
      element.childNodes[1].childNodes[1].removeAttribute("checked");
    }
  });
}
