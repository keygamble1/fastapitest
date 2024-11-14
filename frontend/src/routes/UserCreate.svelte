<script>
    import { push } from 'svelte-spa-router';
    import Error from '../components/Error.svelte';
    import fastapi from "../lib/api";
  
      
    let error={detail:[]}
    let username=''
    let password1=''
    let password2=''
    let email=''
    function post_user(event){
        event.preventDefault()
        let url='/api/user/create'
        let params={
            username:username,
            password1:password1,
            password2:password2,
            email:email
        }
        fastapi('post',url,params,
            (json)=>{
                 push('/user-login')
            },
            (json_error)=>{
                error=json_error
            }

        )
    }

</script>
<div
    class="container"
>
    <h5 class="my-3 border-bottom pb-2">회원가입</h5>
    <Error error={error}/>
    <form method="post">
        <div class="mb-3">
            <label for="username">사용자이름</label>
            <input type="text" name="username" id="username" class="form-control" bind:value="{username}">
            <!-- bindingvalue시 textare select input등의 값과 svelte의 변수를 연결가능
             즉 script의 값을 연결가능하다 -->
        </div>
        <div class="mb-3">
            <label for="password1">비밀번호</label>
            <input type="password" name="password1" id="password1" class="form-control" bind:value="{password1}">
            <!-- bindingvalue시 textare select input등의 값과 svelte의 변수를 연결가능
             즉 script의 값을 연결가능하다 -->
        </div>
        <div class="mb-3">
            <label for="password2">비밀번호 확인</label>
            <input type="password" name="password2" id="password2" class="form-control" bind:value="{password2}">
            <!-- bindingvalue시 textare select input등의 값과 svelte의 변수를 연결가능
             즉 script의 값을 연결가능하다 -->
        </div>
        <div class="mb-3">
            <label for="email">이메일</label>
            <input type="text" name="email" id="email" class="form-control" bind:value="{email}">
            <!-- bindingvalue시 textare select input등의 값과 svelte의 변수를 연결가능
             즉 script의 값을 연결가능하다 -->
        </div>
        <button type="submit" class="btn btn-primary" on:click="{post_user}">생성하기</button>
        <!-- push와 on:click연결시키는게맞음 -->
    </form>
</div>
