var days = new Array("一", "二", "三", "四", "五", "六", "日");
function fillTable(msg) {
  $("#year").text(msg.year);
  $("#month").text(msg.month);
  var day = msg.first_day;
  $.each(msg.resources, function(i, n) {
    var r = "";
    $.each(n, function(j, m) {
      r += "<p><a href=\"javascript:void(0)\" onclick=\"viewResource('" + m.resource_id + "', '" + m.resource_one_id +"')\">" + m.name + "</a></p>";
    });
    $("#timeTable").append("<tr><td>" + (i+1) + "日</td><td>" +
        "星期" + days[day-1] + "</td><td>" + r + "</td></tr>");
    day ++;
    if (day > 7) {
      day = 1;
    }
  });
  $("#info").addClass("hidden");
  $("#time").removeClass("hidden");
  $("#timeTable").removeClass("hidden");
}

function viewResource(rid, roid) {
  $.ajax({
    type: "get",
    dataType: "json",
    url: "/api/resources/view?resource_id=" + rid,
    success: function(msg) {
      $("#resourceName").text(msg.name);
      $("#resourceDescription").text(msg.description);
      $.each(msg.resource_ones, function(i, n) {
        alert(n.resource_one_id);
        alert(roid);
        if (n.resource_one_id == roid) {
          $("#resourceDate").text(n.year + "年" + n.month + "月" + n.day + "日");
        }
      })
      $("#viewModal").modal();
    }
  })

}
