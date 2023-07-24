import {h, reactive} from "vue";
import http from "../utils/http.js";


export const design = reactive({
    getDesign(cart_name) {
        return http.get("script/", {
            params: {
                cart_name: cart_name
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
    addTags(name,design_id) {
        return http.post("script/tags/", {
            name: name,
            design_id:design_id
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
    updateCollocation(id, codes,notes) {
        return http.patch("script/collocation/", {
            id: id,
            codes:codes,
            notes:notes,
        })
    },
    addCollocation(tags_id,design_code) {
        return http.post("script/collocation/", {
            tags_id: tags_id,
            design_code: design_code,
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
    designDetail(code) {
        return http.get("script/designDetail/", {
            params: {
                code: code
            }
        })
    },
})