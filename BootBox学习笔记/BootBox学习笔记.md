### 1.先引入bootBox.js
由于bootbox给予bootstrap,所以先引入bootstrap
```html
<link rel="stylesheet" 	href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css">
<script src="https://cdn.bootcss.com/jquery/3.3.1/jquery.js"></script>
 <script src="https://cdn.bootcss.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
<script src="http://www.veryhuo.com/uploads/Common/js/jQuery.md5.js"></script>
<script src="https://cdn.bootcss.com/bootbox.js/4.4.0/bootbox.js"></script>
```
具体用法只列举一个例子，其它的更多用法请参考官方文档 [点击此处查看官方文档](http://bootboxjs.com/getting-started.html)
直接看代码：
```html
<!DOCTYPE html>
<html lang="en" ng-app="myApp">
<head>
    <meta charset="UTF-8">
    <title>demo</title>
    <link rel="stylesheet" 	href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css">
    <script src="https://cdn.bootcss.com/jquery/3.3.1/jquery.js"></script>
    <script src="https://cdn.bootcss.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
    <script src="http://www.veryhuo.com/uploads/Common/js/jQuery.md5.js"></script>
    <script src="https://cdn.bootcss.com/bootbox.js/4.4.0/bootbox.js"></script>
</head>

<body ng-controller="myCtrl">
    <div class="box">
        <h2>confirm确认框</h2>
        <button type="button" class="btn btn-success" id="button">点我</button>
    </div>
    <script>
        // alert
        $("#button").click(function() {
            bootbox.confirm({
                message: "This is a confirm with custom button text and color! Do you like it?",
                buttons: {
                    confirm: {
                        label: 'Yes',
                        className: 'btn-success'
                    },
                    cancel: {
                        label: 'No',
                        className: 'btn-danger'
                    }
                },
                callback: function(result) {
                    if (result == true) {
                        var dialog = bootbox.dialog({
                            title: 'This custom dialog with init',
                            message: '<p><i class="fa fa-spin fa-spinner"></i> Loading...</p>'
                        });
                        dialog.init(function() {
                            setTimeout(function() {
                                dialog.find('.bootbox-body').html('I was loaded after the dialog was shown!');
                            }, 3000);
                        });
                        $.ajax({
                            url: "http://localhost:1234/order/add",
                            type: "GET",
                            data: "orderName=" + orderName,
                            success: function(data) {
                                Feng.success("添加成功!");
                                window.parent.Order.table.refresh();
                                OrderInfoDlg.close();
                            },
                            error: function() {
                                Feng.error("修改失败!" + data.responseJSON.message + "!");
                            }
                        });
                    } else {
                        bootbox.alert("您已经取消订单");
                    }
                }
            });
        });
    </script>
</body>
</html>
</script>
</body>
</html>
```