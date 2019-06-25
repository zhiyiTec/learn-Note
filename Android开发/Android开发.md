# 1.数据传递:

> 通过 Intent 对象来传递对应的数据，采用的是 key->value 的形式

```java
public void sendInfo(){
    Intent intent=new Intent(this,ShowActivity.class);//this表示是当前的对象，ShowActivity.class表示的是将数据传递的方向
    //将数据存到Internent对象
    intent.putExtra("name",et_name.getText());
    intent.putExtra("password",et_password.getText());
    startActivity(intent);
}
```

在 ShowActivity.java 这个类里面接收

```java
//获取Itent对象
Intent intent=getIntent();
//取值
String name=intent.getStringExtra("name");
String password=intent.getStringExtra("password");
//将取出的值放到文本框中
tv_name=(TextView)findViewById(R.id.tv_name);
tv_password=(TextView)findViewById(R.id.password);
tv_name.setText(name);
tv_password.setText(password);
```

# 2.数据回调

> 何为数据回调:
>
> 比如说有 a1,a2，a2 销毁时会把相关数据传回到 a1,具体如何调用参考下面的代码:

a2:

```java
  Intent intent=new Intent(this,a1.class);//this表示是当前的对象，ShowActivity.class表示的是将数据传递的方向
    //将数据存到Internent对象
    intent.putExtra("name",et_name.getText());
    intent.putExtra("password",et_password.getText());
    setResult(1,intent);/*此处解释一下：1：表示向a1返回的处理结果，一般用0或者1表示；intent:表示需要传递的Intent对象，里面包括你要传递的数据；setResult要与startActivityForResult()配合使用，而表示需要传递的Intent对象，里面包括你要传递的数据；setResult要与startActivityForResult是使用在要回调的类中，也就是说要使用在a1中*/

```

a1:

> startActivityForResult()方法启动 a2,在 a2 销毁时进行回调 a1 的 onActivityResult()方法，因此需要在 a1 中重写该方法来的得到返回的数据，代码如下：

```java
/*在a1中开启a2的入口*/
 Intent intent=new Intent(this,a2.class);/*this表示当前对象，a2.class表示数据来源于a2*/
 startActivityForResult(intent,1);/*1：请求码，输入一个唯一值即可，但是下面onActivityResult方法中要与之对应*/
 /*重写onActivityResult()方法*/
 protected void onActivityResult(requestCode,resultCode,data){
     if(requestCode==1){
         if(resultCode==1){
             String re=data.getStringExtra("password");
         }
     }
 }
```
