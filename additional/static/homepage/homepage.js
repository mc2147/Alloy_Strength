// Register Sign-Up Modal Component
Vue.component('modal', {
    template: '#modal-template'
})

new Vue({
    el:'#sign-up',
    delimiters:['${', '}'], 
    data: {
        showModal: false,
        header: 'SIGN UP',
        name: 'Name',
        email: 'Email',
        password: 'Enter Password Here',
        confirm_password: 'Please Retype Password'
    }
})

new Vue({
    el:'#log-in',
    delimiters:['${', '}'], 
    data: {
        showModal: false,
        header: 'LOG IN',
        email: 'Email',
        password: 'Password',
    }
})