<template>
    <div class="main-container" ref="resultBox">
        <p class="title">Image segmentation using distance aggregation</p>
        <div class="container res-container" >
            <div class="btn-container">
                <img src="@/assets/dl.png" class="s-btn btn" @click="downloadImage"/>
                <img src="@/assets/us.png" class="s-btn btn" @click="scaleImage"/>
            </div>
            <img :src="resultUrl" alt="segmented" class="img-segmented" />
            <button class="btn seg-btn" @click="$router.push('/')">Back to Upload</button>
            <button class="btn seg-btn" @click="$router.push('/settings')">Back to settings</button>
            
        </div>
    </div>
</template>

<script>

import { useImageStore } from '@/stores/imageStore'
export default {
    data() {
        const imageStore = useImageStore();
        return { 
            resultUrl: imageStore.result,
            isScaled: false
        }
    },
    mounted() {
        if (!this.resultUrl) {
            this.$router.push('/');
        }
    },
    
    methods: {
        downloadImage() {
            if (!this.resultUrl) return;

            const link = document.createElement('a');
            link.href = this.resultUrl;
            
            link.download = `segmented_${Date.now()}.png`;
            
            document.body.appendChild(link);
            link.click();
            
            document.body.removeChild(link);
        },
        scaleImage() {
            
            const cont = this.$refs.resultBox;
            
            if (!this.isScaled) {   
                cont.style.transform = 'scale(1.8)'; 
                cont.style.zIndex = '100';         
                this.isScaled = true;
            } else {
                cont.style.transform = 'scale(1)';   
                cont.style.zIndex = '1';
                this.isScaled = false;
            }
        }
    }
}
</script>