<script>
  import moment from 'moment/min/moment-with-locales';
  import { link } from 'svelte-spa-router';
  import fastapi from "../lib/api";
  import { is_login, keyword, page } from '../lib/store';
 moment.locale('ko')

// {이게다 전역변수로 넘겨버린다는뜻 :link든 $page든}
    let question_list=[]
    let size=10
    let total=0
    let kw=''
    // 위에것들을 다 function에서 가져올거 function안에는 fastapi가있고 , 이건 다 json
    // 백엔드에 들어가있는걸 가져오는거
    $: total_page=Math.ceil(total/size);
    // $: 반응형 선언

    function get_question_list(){
        let params={
            page:$page,
            size:size,
            keyword:$keyword,
        }
        fastapi('get','/api/question/list',params,(json)=>{
            question_list=json.question_list
          
            total=json.total
            kw=$keyword
        })
                // then->then->ㅇ렇게계속감 뒤로 돌아가는 if문처럼 실행되지않음
                // then은 콜백함수로 실행되고 차례차례 비동기로 실행된다고봐야함
                // 최종적으로 백엔드에있는 reponse를 json으로 고쳐서 quesiton_list에 넣는거
    }
    $:$page,$keyword, get_question_list($page)
    // $: 이걸로 html에서 쓸수있음
</script>
<div class="container">
    <div class="row my-3">
        <div class="col-6">
        
        <a use:link href="/question-create" class="btn btn-primary {$is_login ? '' : 'disabled'}">질문등록</a>
    </div>
    <div class="col-6">
        <div class="input-group">
            <input type="text" class="form-control" bind:value="{kw}">
            <button class="btn btn-sm btn-secondary" on:click={()=>{$keyword=kw,$page=0}}>찾기</button>
        </div>
    </div>
    </div>
    <table class="table">
        <thead>
            <tr class="table-dark text-center">
                <th >번호</th>
                <th style="width:50%">제목</th>
                <th>글쓴이</th>
                <th>작성일시</th>
            </tr>
        </thead>
        <tbody>
            {#each question_list as question,i}
            <tr class="text-center">
                <td>{total-($page*size)-i}</td>
                <td class="text-start">
                    <a use:link href="/detail/{question.id}">{question.subject}</a>
                    {#if question.answers.length > 0}
                    <span class="text-danger small mx-2">{question.answers.length}</span>
                {/if}
                </td>
                <td>{ question.user ? question.user.username : "" }</td>
                <td>
                    {moment(question.create_date).format('YYYY년 MM월 DD일 hh:mm a')}
                </td>
            </tr>
            {/each}

        </tbody>
    </table>

    <!-- 페이징시작 -->
        <ul
            class="pagination  justify-content-center"
        >
            <li class="page-item {$page<=0 && 'disabled'}">
                <!-- javascript에서 &&는 if임 -->
                <button class="page-link" on:click="{()=>get_question_list($page--)}">이전</button>
            </li>
            {#each Array(total_page) as _,loop_page }
            {#if loop_page >=$page-5 && loop_page <=$page+5}
            
   
            <!-- 항목,loop_page가맞긴하지만 빈걸원하기때문에 그냥 _로 퉁침 undefiend임 -->
             <li class="page-item {loop_page === $page && 'active'}">
                <!-- page-item class와  띄워줘야함{} -->
                <button class="page-link" on:click="{()=>$page=loop_page}">{loop_page+1}</button>

             </li>
             {/if}
            {/each}
            <li class="page-item {$page>=total_page-1 && 'disabled'}">
                <!-- javascript에서 &&는 if임 -->
                <button class="page-link" on:click="{()=>$page++}">다음</button>
            </li>
            
            
        </ul>
     

  
    <!-- HREF안들어가있으면 자기한테 링크가됨 -->
</div>
<ul>

</ul>