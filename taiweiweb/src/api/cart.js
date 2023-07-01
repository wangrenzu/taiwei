import http from "../utils/http"
import {reactive, ref} from "vue"


const cart = reactive({
    cart_list: [],  // 购物车信息
    code_list: {},  // 购物车所有的款号
    cart_code: null,    // 款号用于加入购物车
    /**
     * 加入购物车
     * @param code 款号
     * @param cart_name 购物车名称
     * @param source    来源
     * @returns {Promise<axios.AxiosResponse<any>>}
     */
    addCart(code, cart_name, source) {
        return http.post('cart/', {
            code: code,
            cart_name: cart_name,
            source: source
        })
    },
    /**
     * 获取购物车信息
     * @param cart_name - 购物车名称
     * @returns {Promise<axios.AxiosResponse<any>>}
     */
    getCart(cart_name) {
        return http.get('cart/', {
            params: {
                cart_name: cart_name
            }
        })
    },
    /**
     * 从购物车中删除商品
     * @param id
     * @returns {Promise<axios.AxiosResponse<any>>}
     */
    delCart(id) {
        return http.delete('cart/', {
            params: {
                id: id
            }
        })
    },
    /**
     * 刷新购物车数据
     * @returns {Promise<axios.AxiosResponse<any>>}
     */
    refreshCart() {
        return http.patch('cart/', {
            code_list: this.code_list
        })
    },
})


export default cart;
