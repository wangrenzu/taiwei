import {h, reactive} from "vue";
import http from "../utils/http.js";


export const design = reactive({
    getDesign(cart_name, cart_codes) {
        return http.get("script/", {
            params: {
                cart_name: cart_name,
                cart_codes: cart_codes
            }
        })
    },
    getTags(design_id) {
        return http.get("script/tags/", {
            params: {
                design_id: design_id
            }
        })
    },
    delTag(tag_id) {
        return http.delete('script/tags/', {
            params: {
                tag_id: tag_id
            }
        })
    },
    addTags(name, design_id) {
        return http.post("script/tags/", {
            name: name,
            design_id: design_id
        })
    },
    getSize(tags_id) {
        return http.get("script/size/", {
            params: {
                tags_id: tags_id
            }
        })
    },
    updateSize(tags_id, condition, content) {
        return http.patch("script/size/", {
            tags_id: tags_id,
            condition: condition,
            content: content,
        })
    },
    delSize(size_id) {
        return http.delete('script/size/', {
            params: {
                size_id: size_id
            }
        })
    },
    addSize(tags_id) {
        return http.post("script/size/", {
            tags_id: tags_id
        })
    },
    getScript(tags_id) {
        return http.get("script/script/", {
            params: {
                tags_id: tags_id,
            }
        })
    },
    updateScript(id, original, gpt_original) {
        return http.patch("script/script/", {
            id: id,
            original: original,
            gpt_original: gpt_original,
        })
    },
    delScript(id) {
        return http.delete('script/script/', {
            params: {
                id: id
            }
        })
    },
    addScript(tags_id) {
        return http.post("script/script/", {
            tags_id: tags_id
        })
    },
    checkCode(code) {
        return http.get(`script/checkCode/${code}`)
    },
    getCollocation(tags_id) {
        return http.get("script/collocation/", {
            params: {
                tags_id: tags_id,
            }
        })
    },
    updateCollocation(id, notes) {
        return http.patch("script/collocation/", {
            id: id,
            notes: notes,
        })
    },
    addCollocation(tags_id, design_code) {
        return http.post("script/collocation/", {
            tags_id: tags_id,
            design_code: design_code,
        })
    },
    delCollocation(id, file_name) {
        return http.delete('script/collocation/', {
            params: {
                id: id,
                file_name: file_name
            }
        })
    },
    reply(content) {
        return http.get("script/reply/", {
            params: {
                content: content
            }
        })
    },
    context_reply(content) {
        return http.get("script/context_reply/", {
            params: {
                content: content
            }
        })
    },
    processGETRequest(text) {
        return http.get("script/processGETRequest/", {
            params: {
                text: text,
            }
        })
    },
    getDesign2(code) {
        return http.get("script/design2/", {
            params: {
                code: code
            }
        })
    },
    moveImg(data_list, name) {
        return http.get(`/home/movetodapei/`, {
            params: {
                data_list: JSON.stringify(data_list),
                name: name
            }
        })
    },
    getDesign4(type, name) {
        return http.get("script/design4/", {
            params: {
                type: type,
                name: name
            }
        })
    },
    delImg(name, type, user_name) {
        return http.get("script/delimg/", {
            params: {
                name: name,
                type: type,
                user_name: user_name,
            }
        })
    },
    exportCode(name, type) {
        return http.get("script/exportcode/", {
            params: {
                name: name
            }
        })
    },
    updateNotes(id, notes) {
        return http.get("script/updatenotes/", {
            params: {
                id: id,
                notes: notes,
            }

        })
    },
    getDesigner() {
        return http.get("script/getdesigner/")
    },
    getDesignerCode(designer, time_count) {
        return http.get("script/Designer/", {
            params: {
                designer: designer,
                time_count: time_count
            }
        })
    },
    postDesignerCode(designer, time_count) {
        return http.post("script/Designer/", {
            designer: designer,
            time_count: time_count
        })
    },
    getCodeInfo(code) {
        return http.get("script/getcodeinfo/",{
            params: {
                code: code
            }
        })
    },
    getSearchCode(code) {
        return http.get("script/getsearchcode/", {
            params: {
                code: code,
            }
        })
    },
})