import {reactive} from "vue";
import http from "../utils/http.js";

const room = reactive({
    date_time: null,      // 直播日期
    session: null,        // 场次
    room_list: [],         // 直播间商品信息
    editingRow: null,      // 是否显示修改款号对话框
    room_id: null,          // room_id
    message: [],        // 直播间信息抓取状态
    integration: [],        // 整合表信息
    banner: [],            // 弹幕信息
    show_input1: false,      // 是否显示修改款号对话框
    show_input2: false,      // 是否显示修改库存对话框
    sale_text_list: ["备注1", "备注2", "备注3", "备注4"],                        //库存信息备注
    salesArray: [],         // 库存信息
    result: [],             // 客户购买商品信息
    live_data: {},          // 正在讲解的商品信息
    add_dict: {},            // 本讲解商品信息的增量信息
    live_code: '',         // 本次讲解商品的款号
    // 屏蔽的用户
    not_name: ['S姐助理', '小虎牙啦啦', '杭州S姐 高端女装', '舔10个酸奶盖盖', '月亮湾', '爱穿裙子的小熊妹妹', '慢慢莱', '野兔', '小梦啊', '小胖也可以仙女'],
    // 屏蔽的内容
    not_content: ['福袋', '自动回复', '主播我', '月亮湾', '杭州S姐', '悦仓'],
    room_live_code: '',  // 本次讲解商品的款号 用于修改
    inp_room_live_code: false,      // 是否显示本次讲解修改款号对话框
    sale_text: '备注',                // 备注
    product_info: [],       //商品讲解数据
    room_time: 1,        //讲解时间
    product_info_add_dict: {},    //本讲解商品信息的增量信息
    // 开始抓取直播间内容
    run(room_name) {
        return http.post('/room/roomInfo/', {
            room_name: room_name,
            room_id: this.room_id,
        })
    },
    /**
     * 获取直播间信息
     * @param {string} room_name - 直播间名称
     * @returns {Promise} 返回一个Promise对象
     */
    getRoomInfo(room_name) {
        return http.get('/room/roomInfo/', {
            params: {
                room_name: room_name,
                date_time: this.date_time,
                session: this.session,
                room_live_code: this.room_live_code,
            }
        })
    },
    /**
     * 修改款号
     * @param {number} id - ID
     * @param {string} code - 款号
     * @returns {Promise} 返回一个Promise对象
     */
    editCode(id, code) {
        return http.patch('/room/roomInfo/', {
            id: id,
            code: code
        })
    },
    /**
     * 修改直播价
     * @param {string} code - 款号
     * @param {number} price - 价格
     * @returns {Promise} 返回一个Promise对象
     */
    editOrderPrice(code, price) {
        return http.patch('/room/Integration/', {
            code: code,
            price: price
        })
    },
    /**
     * 获取弹幕信息
     * @param {string} room_name - 直播间名称
     * @returns {Promise} 返回一个Promise对象
     */
    Barrage(room_name) {
        return http.get('/room/Barrage/', {
            params: {
                room_name: room_name,
                room_id: this.room_id,
            }

        })
    },
    /**
     * 添加本次讲解信息
     * @param room_name
     * @returns {Promise<axios.AxiosResponse<any>>}
     * @constructor
     */
    ProductInfo(room_name) {
        return http.post('/room/productInfo/', {
            room_name: room_name,
            info: this.product_info_add_dict,
        })
    },
    /**
     * 获取商品讲解信息
     * @param room_name
     * @returns {Promise<axios.AxiosResponse<any>>}
     */
    getProductInfo(room_name) {
        return http.get('/room/productInfo/', {
            params: {
                room_name: room_name,
                date_time: this.date_time,
                session: this.session,
                room_live_code: this.room_live_code,
            }
        })
    }
})

export default room;

