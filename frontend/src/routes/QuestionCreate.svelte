<script>
  import { push } from "svelte-spa-router";
  import Error from "../components/Error.svelte";
  import fastapi from "../lib/api";
  
    // hashurl되있고 push해서 변경하는거
        // (json)한다고 응답무조건 받는건아닌듯, succescallback해서 return만받아도 되는듯?
    
    let error={detail:[]}
    let subject=''
    let content=''
    function post_question(event){
        // html에서 이벤트를 첫매개변수로 전달함
        event.preventDefault()
        let url="/api/question/create"
        let params={
            subject:subject,
            content:content
        }
        fastapi('post',url,params,
            (json)=>{
                push("/")
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
    <h5 class="my-3 border-bottom pb-3">질문등록</h5>
    <Error error={error} />
    <form class="my-3" method="post">
        <div class="mb-3">
            <label for="subject">제목</label>
            <input type="text" class="form-control" bind:value="{subject}">

        </div>
        <div class="mb-3">
            <label for="content">내용</label>
            <textarea class="form-control" rows="10" bind:value="{content}"></textarea>
        </div>
        <button class="btn btn-primary" on:click="{post_question}">저장하기</button>
    </form>
</div>
