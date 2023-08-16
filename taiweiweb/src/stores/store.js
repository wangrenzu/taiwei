import { defineStore } from 'pinia'
export const useCounterStore = defineStore('storeId', {
    state: () => ({
        code_list: [],
    }),
})