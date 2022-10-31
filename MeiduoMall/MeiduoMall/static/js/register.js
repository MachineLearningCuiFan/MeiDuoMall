
// 创建 Vue 对象
var vm = new Vue({
    el:'#app',
    // 修改Vue读取变量的语法
    delimiters:['[[',']]'],

    // 数据对象
    data:{
        // v-model
        username:getCookie('username'),
        password:'',
        password2:'',
        mobile:'',
        allow:'',
        image_code_url:'',
        uuid:'',
        image_code:'',
        sms_code:'',   // 手机验证码
        sms_code_tip:'获取短信验证码',

        // v-show
        error_name:false,
        error_password:false,
        error_password2:false,
        error_mobile:false,
        error_allow:false,
        error_image_code:true,
        error_sms_code:false,
        send_flag: false, // 类比上厕所，send_flag就是锁，false表示门开，true表示门关
        // error_message
        //error_password_message:'',
        error_name_message:'',
        error_mobile_message:'',
        error_image_code_message:'',
        error_sms_code_message:'',
    },
    // Vue 生命周期 :页面刷新的时候更新图形验证码
    created(){
        // 生成图形验证码
        this.generate_image_code();
    },

    // 事件响应方法
    methods:{
        // 发送手机验证码
        send_sms_code(){
            if (this.send_flag == true) { // 先判断是否有人正在上厕所
                return; // 有人正在上厕所，退回去
            }
            this.send_flag = true; // 如果可以进入到厕所，立即关门

            let url = '/sms_codes/' + this.uuid + '/?image_code=' + this.image_code ;
            axios.get(url,{responseType:'json'})
            .then(response=>{
                // 手机验证码发送成功
                if(response.data.code == '0'){
                 // 展示60秒倒计时
                 let num = 60;
                 // setInterval(’执行内容‘，时间（毫秒）)回调函数
                 let t = setInterval(()=>{
                    if (num == 1) { // 倒计时即将结束
                        clearInterval(t); // 停止回调函数的执行
                        this.send_flag = false;
                        this.sms_code_tip = '获取短信验证码'; // 还原sms_code_tip的提示文字
                        this.generate_image_code(); // 重新生成图形验证码
                    } else { // 正在倒计时
                        num -= 1; // num = num - 1;
                        this.sms_code_tip = num + '秒';
                    }
                 },1000)
                }else{
                 if (response.data.code == '4001') { // 图形验证码错误
                        this.error_image_code_message = response.data.errmsg;
                        this.error_image_code = true;
                        this.generate_image_code();
                        }
                 this.send_flag = false;
                }
            })
            .catch(error=>{
               console.log(error.response);
            })

        },

        // 验证手机验证码
        check_sms_code(){
            if(this.sms_code.length != 6){
                this.error_sms_code=true;
                this.error_sms_code_message='请输入图形验证码！';
            }else{
                this.error_sms_code=false;
                this.error_sms_code_message='';
            }
        },


        // 验证图形验证码
        check_image_code(){
            if(this.image_code.length != 4){
                this.error_image_code_message="请输入图形验证码！";
                this.error_image_code=true;
            }else{
                this.error_image_code=false;
            }
        },

        // 生成图形验证码的方法
        generate_image_code(){
            this.uuid = generateUUID();
            this.image_code_url = '/image_codes/'+this.uuid+'/';

        },
        // 校验 用户名是否合法和重复
        check_username(){
        let re = /^[a-zA-Z0-9_-]{5,20}$/;
        if (re.test(this.username)) {
            this.error_name = false;
        } else {
            this.error_name_message = '请输入5-20个字符的用户名';
            this.error_name = true;
        }

        // 判断用户是否重复注册
        if (this.error_name == false){
            let url = "/"+this.username+"/count/";
            axios.get(url,{responseType:'json'})
            .then(response=>{
                if(response.data.count==1){
                    // 用户名已经存在
                    this.error_name_message='用户名已经存在';
                    this.error_name=true;
                }
             })
            .catch(error=>{
                console.log(error.response);
            })
        }

        },

        // 校验 输入的密码是否合规
        check_password(){
        let re = /^[0-9A-Za-z]{8,20}$/;
        if (re.test(this.password)) {
            this.error_password = false;
        } else {
            this.error_password = true;
        }
        },

        // 校验两次输入的密码是否一样
        check_password2(){
        if(this.password != this.password2) {
            this.error_password2 = true;
        } else {
            this.error_password2 = false;
        }
        },

        // 校验手机号
        check_mobile(){
        let re = /^1[3-9]\d{9}$/;
        if(re.test(this.mobile)) {
            this.error_mobile = false;
        } else {
            this.error_mobile_message = '您输入的手机号格式不正确';
            this.error_mobile = true;
        }
        },

        // 校验用户是否勾选使用协议
        check_allow(){
        if(!this.allow) {
        this.error_allow = true;
        } else {
            this.error_allow = false;
        }
        },

           // 监听表单提交事件
        on_submit(){
        this.check_username();
        this.check_password();
        this.check_password2();
        this.check_mobile();
        this.check_allow();

        if(this.error_name == true || this.error_password == true || this.error_password2 == true
            || this.error_mobile == true || this.error_allow == true) {
            // 禁用表单的提交
            window.event.returnValue = generate_image_code;
        }
        }
    }
})