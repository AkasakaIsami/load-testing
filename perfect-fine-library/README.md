运行脚本，在当前目录下执行

sh run.sh


NOTICE: 注册操作需要检查邮箱里的验证码,没法写自动脚本……所以要手动注册（账号：20212010138；密码：fdse123123）


admin-auth-service
33000


  name: admin-service
      nodePort: 33001


  name: book-service
      nodePort: 33002


  name: comment-service
      nodePort: 33003


  name: copy-service
      nodePort: 33004


  name: email-service
      nodePort: 33005


  name: order-service
      nodePort: 33006


  name: user-auth-service
      nodePort: 33007

  name: user-service
      nodePort: 33008