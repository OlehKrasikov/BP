import { defineStore } from 'pinia'

export const useImageStore = defineStore('image', {
  state: () => ({
    file: null,
    previewUrl: null,
    result:null
  }),
  actions: {
    setImage(file) {
      this.file = file
      this.previewUrl = URL.createObjectURL(file)
    },
    getResult(){
        return this.result
    }
  }
})