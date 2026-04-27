<template>
    <div class="main-container">
        <p class="title">Image segmentation using distance aggregation</p>
        <div class="set-container">
            <div class="container">
                <img :src="preview" alt="preview" class="img-preview"  v-if="preview">
                <img v-else src="@/assets/no-image-icon.png" alt="preview error" class="img-preview">
            </div>
            <div class="side-container">
                <div class="p-container">
                    <div class="param-row" v-for="(val, key) in params" :key="key">
                        <p class="name-param">{{ labels[key] || key }}</p>
                        <select v-if="key === 'accuracy'" v-model.number="params.accuracy" class="param-input">
                            <option :value="0.1">0.1</option>
                            <option :value="0.01">0.01</option>
                            <option :value="0.001">0.001</option>
                            <option :value="0.0001">0.0001</option>
                            <option :value="0.00001">0.00001</option>
                        </select>
                        <input v-else
                            class="param-input" 
                            v-model.number="params[key]" 
                            type="number" 
                            :min="constraints[key]?.min"
                            :max="constraints[key]?.max"
                            :step="constraints[key]?.step || 1"
                            
                        />
                    </div>
                        
                    <div class="seg-btn-container">
                        <button class="seg-btn btn" @click="segmentImage" :disabled="isLoading || !file">
                            <p v-if="!isLoading">Run Segmentation</p>
                            <img v-else src="@/assets/loading.gif" id="loader" />
                        </button>
                        <button v-if="!file"  class="seg-btn btn" @click="$router.push('/')" :disabled="isLoading">
                            <p>Add image</p>        
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { useImageStore } from '@/stores/imageStore'

export default {
    data() {
        const imageStore = useImageStore();
        return {
            file: imageStore.file,
            preview: imageStore.previewUrl,
            isLoading: false,
            params: {
                n_clusters: 2,
                f_coefficient: 2,
                accuracy: 0.01,
                maxIterations: 100,
                colorDistance: 0.5
            },
            constraints: {
                n_clusters: { min: 2, max: 7, step: 1 },
                f_coefficient: { min: 1.1, max: 5.0, step: 0.1 },
                accuracy: { min: 0.00001, max: 1, step: 0.1 },
                maxIterations: { min: 10, max: 500, step: 10 },
                colorDistance: { min: 0, max: 1.0, step: 0.05}
            },
            labels: {
                n_clusters: 'Clusters count',
                f_coefficient: 'Fuzziness',
                accuracy: 'Accuracy threshold',
                maxIterations: 'Max iterations',
                colorDistance: 'Color sensitivity'
            }
        }
    },
    
  
    methods: {
    async segmentImage() {
        const imageStore = useImageStore();
        const formData = new FormData();
        formData.append('image', this.file);
        Object.keys(this.params).forEach(key => formData.append(key, this.params[key]));
        
        this.isLoading = true;
        try {
        const res = await axios.post('http://localhost:8000/segment-image', formData, { responseType: 'blob' });
        const url = URL.createObjectURL(res.data);
        imageStore.result = url;
        this.$router.push({ name: 'result', state: { resultUrl: url } });
        } catch (err) {
            alert("Error!");
        } finally { this.isLoading = false; }
    }
    }
}
</script>