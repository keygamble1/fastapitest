<!-- 골라쓰거나 navigation처럼 공용으로쓰는걸 component라함 -->
 <script>
    import { link } from 'svelte-spa-router';
    import { access_token, is_login, keyword, page, username } from '../lib/store';
</script>
 <nav
    class="navbar navbar-expand-lg navbar-light bg-light"
 >
    <div class="container-fluid">
        <a class="navbar-brand" href="/" on:click="{()=>{$keyword='',$page=0}}">Navbar</a>
        <button
            class="navbar-toggler d-lg-none"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#collapsibleNavId"
            aria-controls="collapsibleNavId"
            aria-expanded="false"
            aria-label="Toggle navigation"
        >
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="collapsibleNavId">
            <ul class="navbar-nav me-auto mt-2 mt-lg-0">
                {#if $is_login }
                    <li class="nav-item">
                        <a use:link href="/user-login" class="nav-link" on:click={() => {
                            $access_token=''
                            $username=''
                            $is_login=false
                        }}
                        >로그아웃({$username})</a>
                    </li>
                {:else}
                
                <li class="nav-item">
                    <a use:link class="nav-link" href="/user-create">회원가입</a>
                </li>
                <li class="nav-item">
                    <a use:link class="nav-link" href="/user-login">로그인</a>
                </li>
                {/if}
               
        </div>
    </div>
 </nav>
 