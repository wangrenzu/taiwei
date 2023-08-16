import {reactive} from "vue";
import http from "../utils/http.js";


export const tags = reactive({
    season: null,
    goods_info: [[], [], []],
    new_goods_info: [[], [], []],
    nums: [10, 10, 10],
    loadings: [false, false],
    getCategory(season) {
        return http.get(`/home/getCategory/${season}`)
    },
    getGoodsInfo(tag_list,search_code) {
        return http.post('home/getgoodsinfo/', {
            tag_list: tag_list,
            search_code: search_code,
        })
    },
    moveImg(data_list,name) {
        return http.get(`/home/movetodanping/`, {
            params: {
                data_list: JSON.stringify(data_list),
                name:name
            }
        })
    },

})