<template>
    <div class="content">
        <img :src="decodedImage" alt="Content Image" @error="handleImageError" />
        <div class="body">
            <div class="title-holder">
                <p>Title</p>
                <h3>{{ content.title }}</h3>
            </div>
            <div class="bottom-area">
                <p>Author: {{ content.author }}</p>
                <p>Rating: {{ isNaN(content.rating) ? 'N/A' : content.rating.toFixed(2) }} / 5</p>
            </div>
            <div class="button-grid">
                <button class="btn btn-primary btn-sm" @click="updateContent(content.id)">
                    <i class="fa-solid fa-pen"></i> Update
                </button>
                <router-link class="btn btn-success btn-sm" :to="'/activity-page/' + content.id">
                    <i class="fa-solid fa-chart-line"></i> Activity
                </router-link>
                <button class="btn btn-danger btn-sm" @click="confirmDelete(content.id)">
                    <i class="fa-solid fa-trash"></i> Delete
                </button>
            </div>
            <div v-if="showAlert" :class="[alertType, 'alert-dismissible', 'fade', 'show']" role="alert">
                {{ alertMessage }}
                <button type="button" class="btn-close" @click="hideAlert" aria-label="Close"></button>
            </div>
        </div>
        <!-- Alert banner -->
        <AlertTop v-if="showAlert" :message="alertMessage" :type="alertType" @close="hideAlert" />
    </div>
</template>

<script>
import AlertTop from './AlertTop.vue';
export default {
    components:{
        AlertTop,
    },
    data() {
        return {
            showAlert: false,
            alertType: 'success',
            alertMessage: '',
        };
    },
    props: {
        content: {
            type: Object,
            required: true,
        },
        decodedImage: {
            type: String,
            required: true,
        },
    },
    methods: {
        confirmDelete(contentId) {
            if (confirm("Are you sure you want to delete this content?")) {
                this.deleteContent(contentId);
            }
        },
        getDecodedImage(content) {
            const decodedImage = `data:image/${content.imageType};base64, ${content.image}`;
            return decodedImage;
        },
        handleImageError(event) {
            console.error("Error loading image:", event);
        },
        activityContent(contentId) {
            this.$route.push(`/activity-page/${contentId}`)
        },
        filteredContents(sectionId) {
            return this.contents
                .filter((content) => content.section === sectionId)
                .map((content) => {
                    const decodedImage = this.getDecodedImage(content);
                    const rating = this.getAverageRating(content.id);
                    return { ...content, decodedImage, rating };
                }
                );
        },
        updateContent(contentId) {
            this.$router.push({ name: 'UpdateContent', params: { contentId: contentId } });
        },
        deleteContent(contentId) {
            const token = sessionStorage.getItem('token');

            fetch(`http://127.0.0.1:5000/delete-content/${contentId}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
            })
                .then((response) => {
                    if (response.ok) {
                        this.showAlert = true;
                        this.alertType = 'success';
                        this.alertMessage = 'Content deleted successfully.';
                        return response.json();
                    } else {
                        throw new Error('Failed to delete content');
                    }
                })
                .then((data) => {
                    this.$emit('contentUpdated');
                    console.log(data.message);
                })
                .catch((error) => {
                    this.showAlert = true;
                    this.alertMessage = 'Failed to delete content.';
                    this.alertType = 'error'
                    console.error(error);
                });
        },
        hideAlert() {
            this.showAlert = false
        }
    }
};
</script>

<style scoped>
.content {
    display: flex;
    flex-direction: column;
    row-gap: 0.5rem;
    background-color: rgb(243, 238, 238);
    border-radius: 0.5rem;
    border: 1px solid white;
    box-shadow: rgba(50, 50, 93, 0.25) 0px 50px 100px -20px, rgba(0, 0, 0, 0.3) 0px 30px 60px -30px, rgba(10, 37, 64, 0.35) 0px -2px 6px 0px inset;
    width: 210px;
    scroll-snap-align: start;
}

.content img {
    height: 180px !important;
    border-radius: 0.5rem 0.5rem 0 0;
    width: auto;
}

.content .body {
    display: flex;
    flex-direction: column;
    row-gap: 0.5rem;
    padding: 0.5rem;
    height: 100%;
}

.title-holder {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    row-gap: 0.25rem;
    font-family: Arial, Helvetica, sans-serif;
}

.title-holder p {
    font-size: 14px;
    line-height: 18px;
    color: rgb(51, 51, 51);
    margin: unset;
}

.title-holder h3 {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    font-size: 20px;
    line-height: 30px;
    margin: unset;
    color: black;
    width: 200px;
}

.bottom-area {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    row-gap: 0.25rem;
    width: 100%;
}

.bottom-area p {
    font-size: 14px;
    line-height: 18px;
    color: rgb(51, 51, 51);
    margin: unset;
}

.button-grid {
    gap: 0.5rem;
    display: flex;
    justify-content: center;
    /* display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr)); */
    margin-top: auto;
}

.button-grid button {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.25rem;
    padding: 0.5rem;
    width: 100%;
}
</style>