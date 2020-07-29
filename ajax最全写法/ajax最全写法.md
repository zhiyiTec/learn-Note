``` js
  $.ajax({
        url: url,
        data: data,
        dataType: "json",
        type: "post",
        async: false, //异步请求处理
        processData: false, // 告诉jQuery不要去处理发送的数据
        contentType: false, // 告诉jQuery不要去设置Content-Type请求头
        //加上这句话,允许浏览器向服务器跨域请求时携带cookie
        xhrFields: {
          withCredentials: true
        },
        crossDomain: true,
        success: function(data) {
          }
        },
        error: function(data) {}
      });
```