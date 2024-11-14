<script>
  import { push } from 'svelte-spa-router';
  import Error from "../components/Error.svelte";
  import fastapi from "../lib/api";
 
  export let params={}
  
//   이 params는 다른파일 javascript에서 import {params}로 사용가능함
  const answer_id=params.answer_id
  let error={detail:[]}
  let question_id=0
  let content=''
  fastapi("get","/api/answer/detail/"+answer_id,{},
    (json)=>{
        question_id=json.question_id
        content=json.content
    }
  )
  function update_answer(event){
    event.preventDefault()
    let url="/api/answer/update"
    let params={
        answer_id:answer_id,
        content:content,
    }
    fastapi("put",url,params,
        (json)=>{
            push('/detail/'+question_id)
        },
        (json_error)=>{
            error=json_error
        }
    )
  }
//   일단 다 초기값으로 선언
//   이걸해야 일단 빈걸로 출력해서 html이나옴
  

// var는 함수외부에서 만접근안되고 함수안에서는 왔다갔다가능
// const let은 블록안에서만가능 for if 빠져나가면 못사용
</script>
<div
    class="container"
>   
    <h5 class="my-3 border-bottom pb-2">답변수정</h5>
    <Error error={error}/>
    <form method="post" class="my-3">
        <div class="mb-3">
            <label for="content">내용</label>
            <textarea class="form-control" rows="10" bind:value="{content}" ></textarea>
        </div>
        <button class="btn btn-primary" on:click={update_answer}>수정하기</button>
    </form>
</div>
