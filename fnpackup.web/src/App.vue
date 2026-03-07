<template>
    <template v-if="showApp">
        <div class="flex flex-column flex-nowrap h-100 absolute">
            <div class="head" v-if="showHead">
                <Head></Head>
            </div>
            <div class="body flex-1 relative">
                <Body></Body>
            </div>
        </div>
    </template>
    <template v-else>
        <el-dialog width="300" model-value="true" center title="登录检查" :close-on-click-modal="false" :show-close="false">
            <div class="t-c">
                <p>
                    <img :src="state.img" alt="" height="100">
                </p>
                <p>{{ state.checkMsg }}</p>
            </div>
        </el-dialog>
    </template>
</template>

<script>
import Head from './components/Head.vue';
import Body from './components/Body.vue';
import { computed, reactive, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { fetchSystemSignIn, fetchSystemVersion } from './api/api';
export default {
    name: 'App',
    components: {Head,Body},
    setup() {

        const state = reactive({
            checkMsg:'正在登录检查',
            img:'loading.gif'
        });

        const router = useRouter();
        const route = useRoute();
        const showHead = computed(()=>window.self === window.top);
        const showApp = ref(false);

        const checkSignIn = ()=>{
            state.img = 'loading.gif';
            state.checkMsg = '正在登录检查';
            fetchSystemSignIn().then((res)=>{
                if(res == 'OK'){
                    fetchSystemVersion().then((_res)=>{
                        showApp.value = true;
                        state.checkMsg =  res ;
                        state.img = 'loading.gif';
                    }).catch(()=>{});
                }else{
                    showApp.value = false;
                    state.checkMsg = '登录检查失败，可能未登录飞牛';
                    state.img = 'fail.jpg';
                }
                setTimeout(checkSignIn,5000);
            }).catch(()=>{
                showApp.value = false;
                state.checkMsg = '登录检查失败';
                state.img = 'fail.jpg';
                setTimeout(checkSignIn,5000);
            }); 
        };

        router.isReady().then(()=>{
            for(let key in route.query){
                document.cookie = `${key}=${decodeURIComponent(route.query[key])}; path=/;`;
                localStorage.setItem(key,decodeURIComponent(route.query[key]));
            }
            if(route.query['fnos-theme']){
                window.location = `/?t=${Date.now()}`;
            }
            checkSignIn();
            
        });

        return {showHead,showApp,state}
    },
}
</script>

<style lang="stylus">
</style>
