<template>
    <div class="main-container">
        <p class="title">Image segmentation using distance aggregation</p>
        <div class="container main-section">
                
                <p class="subtitle">Nahrat obrazok</p>
                <input type="file" ref="fileInput" style="display: none" @change="handleFileChange" accept="image/*" />
                <button class="btn-upload btn" @click="$refs.fileInput.click()"></button>
        </div>
    </div>
</template>

<script>
import { useImageStore } from '@/stores/imageStore'
export default {
    methods: {
        handleFileChange(event) {
            const file = event.target.files[0];
            if (file) {
                const store = useImageStore();
                store.setImage(file);
                this.$router.push({ name: 'settings' });
            }
        }
    }
}
</script>