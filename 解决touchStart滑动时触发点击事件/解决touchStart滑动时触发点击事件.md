> 由于我们在将点击事件委托到div,span,font,p等元素标签上时会导致移动端的ios设备无法识别这个点击事件（一般指click事件），
> 此时我们一般会使用touchstart来替换click事件，但是使用touchstart来代替click事件的弊端就立刻显示出来，每当我们滑动屏幕时就会立刻出发点击事件
> 此时加入我这个封装的方法，这个弊端就会迎刃而解
``` js
function tap(el,fn){
    var startPoint = {};
    el.addEventListener('touchstart', function(e) {
        startPoint = {
            x: e.changedTouches[0].pageX,
            y: e.changedTouches[0].pageY
        };
    });
    el.addEventListener('touchend', function(e) {
        var nowPoint = {
            x: e.changedTouches[0].pageX,
            y: e.changedTouches[0].pageY
        };
        if(Math.abs(nowPoint.x - startPoint.x) < 5
            &&Math.abs(nowPoint.y - startPoint.y) < 5) {
            fn&&fn.call(el,e)
        }
    });
}
```
# 下面顺便讲一下当使用touchstart来替换click时，必须要记住一点：一定不要忘了添加 event.preventDefault();
> 但是问题又来了，添加 event.preventDefault();浏览器就会报错，
### 解决办法：
* 1、注册处理函数时，用如下方式，明确声明为不是被动的
> window.addEventListener('touchmove', func, { passive: false })
* 2、应用 CSS 属性 touch-action: none; 这样任何触摸事件都不会产生默认行为，但是 touch 事件照样触发。
``` css
.sortable-handler {
            touch-action: none;
        }
```