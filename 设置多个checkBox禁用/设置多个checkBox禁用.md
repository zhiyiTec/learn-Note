# 话不多说直接看例子：
``` html
<body>
		  <input type="checkbox" id="check" name="scales">2
		  <input type="checkbox" id="check" name="scales">3
		  <input type="checkbox" id="check" name="scales">4
		  <input type="checkbox" id="check" name="scales">5
		  <button id="btn">点击</button>
		 <!-- jQuery文件。务必在bootstrap.min.js 之前引入 -->
    <script src="http://cdn.bootcss.com/jquery/1.11.1/jquery.min.js"></script>
		 <script>
		$("#btn").click(function(){
		
		  var checkbox =$('input:checkbox');
   checkbox.attr("disabled","disabled");
		})

   
		 </script>
</body>
```