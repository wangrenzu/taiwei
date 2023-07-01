import http from "../utils/http"
import {reactive, ref} from "vue"

const home = reactive({
    data_list: [],      //订单数据带分页
    all_data_list: [],   //不带分页的订单数据
    page: 1,           //显示页数
    size: 10,           //显示条数
    count: 0,           //总条数
    search_date: null,  //搜索的日期
    order_status: "请选择订单状态",     //订单状态
    is_show_table: true,              //是否显示订单表格
    user_data_list: [],          //存放汇总数据带分页
    nwe_user_data_list: [],          //存放汇总数据带分页
    show_update: false,          //是否显示上传订单数据窗口
    show_update_user: false,     //是否显示上传用户数据窗口
    show_update_goods: false,     //是否显示上传货品窗口
    show_update_materials: false,     //是否显示上传辅助材料购买窗口
    show_update_size: false,     //  是否显示上传尺寸表窗口
    show_update_commodity: false,   // 是否显示上传全量表窗口
    show_update_stock: false,       //是否显示上传多仓库表窗口
    all_user_data_list: [],      //  不带分页的用户汇总数据
    is_show_search3_table: false,       // 千川订单的表格
    is_show_search4_table: false,       // 客户信息的表格
    is_show_search5_table: false,       // 款号信息的表格
    is_show_search6_table: false,       // 选款库存大于5的表格
    is_show_search7_table: false,       // 热销款的表格
    is_show_search8_table: false,       // 滞销款的表格
    is_show_search9_table: false,       // 最近几天热卖的表格
    is_show_search10_table: false,       // 库存1-5的表格
    is_show_search11_table: false,       // 30天全量表汇总的表格
    is_show_search12_table: false,       // 爆款的表格
    is_show_report_table: false,       // 每日报表的表格
    loading: true,                      // 是否显示加载状态
    query1_results: [],                 // 待发款号信息
    query2_results: [],                  // 取消款号信息
    query3_results: [],                  // 在途款号信息
    query4_results: [],                 // 成功款号信息
    query5_results: [],                 // 退回款号信息
    searchKeyword: [],                  // 用户名称用于客户信息排名搜索用户
    report_list: [],                    // 每日报表数据
    report_data: null,                  // 报表日期
    report_data_history: null,          // 历史报表日期
    buttonType1: 'primary',
    buttonType2: 'primary',
    buttonType3: 'primary',
    buttonType4: 'primary',
    buttonType5: 'primary',
    buttonType6: 'primary',
    buttonType7: 'primary',
    buttonType9: 'primary',
    buttonType10: 'primary',
    buttonType11: 'primary',
    buttonType12: 'primary',
    buttonType13: 'primary',
    buttonType14: 'primary',
    new_user_list2: [],               // 存放在客户信息中的在线观众
    show_update_SalesRecord: false,        // 上传档口销量表
    create_time: null,                      // 货品档案中的创建日期
    season: null,                       // 获取档案中的季节
    show_update_StockIn: false,         // 上传档口调拨表
    tracking_data: [],                  // 货品跟踪的数据
    addCode: '',                        // 货品档案中要添加的款号
    code_list: [],                      // 获取档案中所有的款号
    show_update_onecommodity: false,      // 上传每日全量表
    category: null,                     // 货品档案中的品类
    day: 3,                                // 库存1-5条件中的 最近几天的数据
    close: true,                        // 关闭websocket连接
    open: false,                        // 打开websocket连接
    new_user_list: [],                  // 所有的客户信息
    new_user_list3: [],                 // 不在客户信息中的在线观众
    update_status: [],                  // 上传excel的最后日期
    vipUser_list: [],                   // 所有的vip用户
    searchCode: null,                   // 要搜索的款号
    barrage: [],                         // 弹幕信息
    show_update_repeat_order: false,      // 上传下单简报
    show_update_fabric: false,            // 上传面料表
    show_update_factory: false,            // 上传工厂表
    style_status_list: [],              // 新款状态的数据
    style_page: 1,           //新款状态的页数
    style_size: 10,           //新款状态的每页条数
    style_count: 0,          // 新款状态的总条数
    // 获取带分页的订单数据
    show() {
        return http.get(`/home/?page=${this.page}&size=${this.size}`)
    },
    // 获取带搜索条件并且分页的订单数据
    search() {
        return http.get("/home/search",
            {
                params: {
                    search_date: this.search_date,
                    order_status: this.order_status,
                    page: this.page,
                    size: this.size,
                }
            })
    },
    // 获取带分页的汇总数据
    summary() {
        return http.get("/home/summary", {
            params: {
                search_date: this.search_date,
                order_status: this.order_status,
                page: this.page,
                size: this.size,
                create_time: this.create_time,
                season: this.season,
                category: this.category,
                day: this.day,
                code: this.searchCode,
            }
        })
    },
    // 获取不带分页的汇总数据
    userAll() {
        return http.get("/home/userAll/", {
            params: {
                search_date: this.search_date,
                order_status: this.order_status,
                create_time: this.create_time,
                season: this.season,
                category: this.category
            }
        })
    },

    /**
     * 获取改该用户的商品信息
     * @param {string} name - 用户名
     * @param {string} search_date - 搜索日期
     * @returns {Promise} 返回一个Promise对象
     */
    getUserInfo(name, search_date) {
        return http.get("/home/userInfo/", {
            params: {
                name: name,
                search_date: search_date

            }
        })
    },
    /**
     * 获取商品信息
     * @param {string} submit_time - 订单提交时间
     * @returns {Promise} 返回一个Promise对象
     */
    getCodeInfo(submit_time) {
        return http.get("/home/codeInfo/" + submit_time)
    },
    /**
     * 获取每日报表
     * @returns {Promise} 返回一个Promise对象
     */
    getReportList() {
        return http.get("/home/getReportList", {
            params: {
                report_data: this.report_data,
                report_data_history: this.report_data_history,
                page: this.page,
                size: this.size,
            }
        })
    },
    /**
     * 获取所有客户信息
     * @returns {Promise} 返回一个Promise对象
     */
    roomAll() {
        return http.get("/home/userAll/", {
            params: {
                order_status: "客户信息排名",
            }
        })
    },
    //获取订单跟踪信息
    getTrakcing() {
        return http.get('/home/orderTracking/')
    },
    /**
     * 删除订单跟踪信息
     * @param {number} id - 跟踪信息ID
     * @returns {Promise} 返回一个Promise对象
     */
    delTrakcing(id) {
        return http.delete('/home/orderTracking/', {
            params: {
                id: id
            }
        })
    },
    /**
     * 添加订单跟踪信息
     * @returns {Promise} 返回一个Promise对象
     */
    addTracking() {
        return http.post('/home/orderTracking/', {
            code: this.addCode
        })
    },
    /**
     * 刷新订单跟踪信息
     * @returns {Promise} 返回一个Promise对象
     */
    refreshTracking() {
        return http.patch('/home/orderTracking/', {
            code_list: this.code_list
        })
    },
    /**
     * 获取excel最后的上传日期
     * @returns {Promise} 返回一个Promise对象
     */
    getUpdateStatus() {
        return http.get("/home/updateStatus/")
    },
    /**
     * 更新excel最后的上传日期
     * @param {number} id - 状态信息ID
     * @returns {Promise} 返回一个Promise对象
     */
    putUpdateStatus(id) {
        return http.put("/home/updateStatus/", {id})
    },
    /**
     * 添加VIP用户
     * @param {string} name - 用户名
     * @returns {Promise} 返回一个Promise对象
     */
    addVipUser(name) {
        return http.post("/home/vipUser/", {
            name: name
        })
    },
    // 获取所有vip用户
    getVipUser() {
        return http.get("/home/vipUser/")
    },
    /**
     * 删除VIP用户
     * @param {string} name - 用户名
     * @returns {Promise} 返回一个Promise对象
     */
    delVipUser(name) {
        return http.delete('/home/vipUser/', {
            params: {
                name: name
            }
        })
    },
    /**
     * 获取全量表款号信息
     * @param {string} code - 款号
     * @param {string} data_time - 开始时间
     * @returns {Promise} 返回一个Promise对象
     */
    searchCodeInfo(code, data_time) {
        return http.get("/home/searchCode/", {
            params: {
                code: code,
                data_time: data_time
            }
        })
    },
    /**
     * 获取新款状态
     * @param {string} code - 款号
     * @param {string} tags - 标签
     * @param {string} date_time - 上传日期
     * @param {boolean} is_all - 是否获取全部信息
     * @returns {Promise} 返回一个Promise对象
     */
    getStyleStatus(code, tags, date_time, is_all) {
        return http.get("/home/StyleStatusView", {
            params: {
                page: this.style_page,
                size: this.style_size,
                code: code,
                tags: tags,
                date_time: date_time,
                is_all: is_all,
            }
        })
    },

    /**
     * 更新新款状态的标签和备注信息
     * @param {number} id - id
     * @param {string} tags - 标签
     * @param {string} remarks - 备注
     * @returns {Promise} 返回一个Promise对象
     */
    uptStyleStatusTags(id, tags, remarks) {

        return http.patch('/home/StyleStatusView/', {
            id: id,
            tags: tags,
            remarks: remarks,
        })
    }
})


export default home;