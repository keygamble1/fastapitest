<script>

  import Router from "svelte-spa-router";

  import Navigation from "./components/Navigation.svelte";
  import AnswerModify from "./routes/AnswerModify.svelte";
  import Detail from "./routes/Detail.svelte";
  import Home from "./routes/Home.svelte";
  import QuestionCreate from "./routes/QuestionCreate.svelte";
  import QuestionModify from "./routes/QuestionModify.svelte";
  import UserCreate from "./routes/UserCreate.svelte";
  import UserLogin from "./routes/UserLogin.svelte";
  const routes={
    '/':Home,
    '/detail/:question_id':Detail,
    '/question-create':QuestionCreate,
    '/user-create':UserCreate,
    '/user-login':UserLogin,
    '/question-modify/:question_id':QuestionModify,
    '/answer-modify/:answer_id':AnswerModify,
    // 서버와통신안하고 spa 싱글로 javasscript로서 개인으로 처리하게하는걸
    // 프론트엔드라고 볼수도있음
  }
</script>
<Navigation/>
<Router {routes}/>

<!-- then은 promise를 받고 promise를 반환한다 then은 함수라서 끝에 세미콜른을붙임
첫번째 then은 응답을 받아서 json으로 변경하는 작업을 실행
두번째 then은 json데이터가준비될시 변환하는 작업을 실행
then은 json변환과 처리하는 작업을 같이한다
javascripㅅ에서 비동기작업은 바로 결과를 얻지않고 나중완료
 서버에서 데이터만 받고 ㅅ처리는 나중에
 이건 Promise객체를 받는데 이건 성공 or 실패함
 then()은 성공시 그결과를 받아 처리하는걸 정의하는 메서드
 한마디로 저장하고 성공시 then() 메서드로 처리함
Promise반환-> 데이터요청끝날때까지(pending)
->비동기작업 성공시 준비되면 (resolved)
->then에 전달! 된 함수실행 이때 그함수는 비동기작업의결과(promise) 를 인자로 받음
->실패시 catch 성공시 then
fetch(url).then((response)=>{
성공
return response.json() json반환})
.then((response)=>{
 console.localStorage(jsondata) 데터 성공
}); return 위에나오니까 ;를부팅ㅁ
.catch((error)=>{
conosle.Error('error',error)
});
첫번째 
 -->