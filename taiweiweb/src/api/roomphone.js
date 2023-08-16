import {reactive} from "vue";
import http from "../utils/http.js";

const roomphone = reactive({
    vip_user_list: [],
    new_user_list: [],
    new_user_list2: [],
    barrage: [],
    getUser(code) {
        return http.get('/phone/get_user_name/', {
            params: {
                code: code,
            }
        })
    },
    addUser(user_info) {
        return http.post('/phone/douyinuser/', user_info)
    },
    addLiveDouyinUser() {
        return http.get('/phone/getdouyinuser/')
    }
})
export default roomphone;