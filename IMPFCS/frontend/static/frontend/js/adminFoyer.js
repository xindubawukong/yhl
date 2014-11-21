
function requestListResources() {
    $.ajax({
        type: "GET",
        dataType: "json",
        url: "/api/resources/list",
        success: function(data) 
        {
            var list = $('#resources');
            $.each(data.resources, function(i, n) 
                { 
                    $.each(n, function(j, res)
                        {
                            list.append('<li class="in"><div class="message"><span class="arrow"></span><span class="name">' + res.name + '</span><span class="datetime"></span></div></li>');
                        }
                    );
                }
            );
        }
    });
}


function addResource() {
  $.ajax({
    type: "POST",
    url: "/api/resources/manage/add/",
    data:   { 
        'name': $('#addResourceName').val(), 
        'description': $('#addResourceDescription').val(),
        'dates': $('#addResourceDates').val(), 
            },
    success: function(data) {
      if (data.success == 1) {
        alert("添加资源成功!");
        location.reload();
      } else {
        alert("添加失败！" + data.error);
      }
    }
  });
}


requestListResources()
$('#addResourceBtn').click(addResource);