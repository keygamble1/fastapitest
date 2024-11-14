import { writable } from "svelte/store";

// 화살표함수는 미리 변수가 정의되어있어야하고 그 이후에 호출가능
// function 기본함수선언은 함수가선언되기도전ㅇ네 변수를 호출을 할수있게해줌
// function은 최상단으로 끌어올려저서 어디서든쓸수있지만 화살표함수는 무조건 위쪽에 먼저선언되어야함
// const let은 스코프안에서만 유효하며, var은 함수스코프안에서만 유효 if while for은 상관없음
// {wirable} 블록스코프
const persist_storage=(key,initValue)=>{
    const storeValueStr=localStorage.getItem(key)
    const store=writable(storeValueStr != null ?JSON.parse(storeValueStr) : initValue)
    store.subscribe((val)=>{
        localStorage.setItem(key,JSON.stringify(val))

    })
    return store
}
// 뒤로가기해도 남아있게하려면 store변수에서해야함
export const page=persist_storage("page",0)
export const keyword=persist_storage("keyword","")
export const access_token=persist_storage("access_token","")
export const username=persist_storage("username","")
export const is_login=persist_storage("is_login",false)
// 이걸로 이제 svelte에서 $page로 전역변수 공유가능