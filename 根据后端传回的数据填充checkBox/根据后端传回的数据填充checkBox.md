# 直接看代码吧，看不懂，或者感觉我写有错误直接在下面提示我，谢谢!!!!
* html代码：
```html
        <input type="checkbox" value='D、40' /><span>1</span>
        <input type="checkbox" value="B、20" /><span>2</span>
        <input type="checkbox" value="C、30" /><span>3</span>
        <input type="checkbox" value="B、20" /><span>4</span>
        <input type="checkbox" /><span>5</span>
        <input type="checkbox" /><span>6</span>
        <button id='btn'>上一题</button>
```
* js代码：
``` html
 $("#btn").click(function() {
            var preparameter = 1 + '-' + 1 + "-" + 1074 + "-" + 156;
            $.ajax({
                url: "http://localhost/hongsong/getPreProblem",
                data: "preparameter=" + preparameter,
                type: "post",
                success: function(data) {
                    console.log(data);

                    if (data.qR.indexOf(",") == -1) {
                        $('input:checkbox').each(function() {

                            if ($(this).val() == data.qR) {
                                $(this).attr("checked", true)
                            }
                        })
                    } else {
                        var re = new Array();
                        re = data.qR.split(",");

                        console.log(re)
                        $.each(re, function(index, item) {
                            $('input:checkbox').each(function() {
                                if ($(this).val() == item) {
                                    $(this).attr("checked", true)
                                }
                            })
                        })
                    }




                },
                error: function() {

                }
            });
        })
```