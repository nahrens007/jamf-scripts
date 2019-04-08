$("#checkAll").click(function() {
  $(".check").prop('checked', $(this).prop('checked'));
});

function categorySelect() {
  var category=$("#catsel").val();
  console.log(category);
  $("tr.approw").each(function(index, element) {
    var rowcat = $(element).children("td.catname").text().trim(); // get td with category
    if (category == rowcat) {
      $(element).children().get(0).children(0).prop("checked", true); // set the checkbox to checked
    }
  });
}
