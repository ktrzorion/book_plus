<template>
    <div class="content">
        <button v-if="isLoggedIn()" class="btn btn-sm btn-light top-btn" @click="confirmPurchase(content.id)"><i
                class="fa-solid fa-download"></i></button>
        <img :src="decodedImage" alt="Content Image" @error="handleImageError" />
        <div class="body">
            <div class="title-holder">
                <p>Title</p>
                <h3>{{ content.title }}</h3>
            </div>
            <div class="bottom-area">
                <p>Author: {{ content.author }}</p>
                <p>Rating: {{ !content.rating || isNaN(content.rating) ? 'N/A' : `${content.rating.toFixed(2)} / 5` }}
                </p>
            </div>
            <div class="text-center" v-if="content.isRead">
                <router-link :to="{ name: 'RateContent', params: { contentId: content.id } }"
                    class="btn btn-warning btn-sm">Rate <i class="fa-regular fa-star"></i></router-link>
            </div>
            <div class="button-grid">
                <button v-if="!content.isIssued && !content.isRequested" class="btn btn-primary btn-sm" @click="createRequest(content.id)">
                    <i class="fa-solid fa-book"></i> Request
                </button>
                <div v-if="content.isRequested && !content.isIssued" class="btn btn-secondary btn-sm">
                    <i class="fa-solid fa-hourglass-start"></i> Waiting
                </div>
                <button v-show="content.isIssued" class="btn btn-primary btn-sm" @click="openContent(content.id)">
                    <i class="fa-brands fa-readme"></i> Read
                </button>
                <button v-show="content.isIssued" class="btn btn-danger btn-sm" @click="returnContent(content.id)">
                    <i class="fa-solid fa-rotate-left"></i> Return
                </button>
                <button class="btn btn-light btn-sm" @click="toggleWishlist(content.id, content.isWishlisted)"
                    :class="{ 'btn-danger': content.isWishlisted, 'btn-warning': !content.isWishlisted }">
                    <i class="fa-regular fa-heart" :class="{ 'fas': content.isWishlisted }"></i> Wishlist
                </button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            rating: null
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
        isRead: {
            type: Boolean,
            required: true,
        },
    },
    methods: {
        confirmPurchase(contentId){
            if (confirm("Are you sure you want to purchase/download this content?")) {
                this.buyDownload(contentId);
            }
        },
        async createRequest(contentId) {
            if (!this.isLoggedIn()) {
                this.$router.push('/login');
                return;
            }

            try {
                await this.$axios.post(`http://127.0.0.1:5000/create_request/${contentId}`, null, {
                    headers: {
                        Authorization: `Bearer ${sessionStorage.getItem('token')}`,
                    },
                });
                this.$emit('contentUpdated');
                console.log('Request created successfully.');
            } catch (error) {
                console.error('Error creating request:', error);
            }
        },
        async openContent(contentId) {
            try {
                const response = await fetch(`http://127.0.0.1:5000/get_pdf/${contentId}`, {
                    headers: {
                        Authorization: `Bearer ${sessionStorage.getItem('token')}`,
                    },
                });
                const blob = await response.blob();

                const pdfUrl = URL.createObjectURL(blob);

                window.open(pdfUrl, '_blank');
            } catch (error) {
                console.error('Error opening content:', error);
            }
        },
        async returnContent(contentId) {
            try {
                await this.$axios.post(`http://127.0.0.1:5000/return_content/${contentId}`, null, {
                    headers: {
                        Authorization: `Bearer ${sessionStorage.getItem('token')}`,
                    },
                });
                this.$emit('contentUpdated');
            } catch (error) {
                console.error('Error returning content:', error);
            }
        },
        async toggleWishlist(contentId, isInWishlist) {
            if (!this.isLoggedIn()) {
                this.$router.push('/login');
                return;
            }

            try {
                const endpoint = isInWishlist ? 'remove' : 'add';
                const response = await this.$axios.post(`http://127.0.0.1:5000/wishlist/${endpoint}/${contentId}`, null, {
                    headers: {
                        Authorization: `Bearer ${sessionStorage.getItem('token')}`,
                    },
                });

                this.$emit('contentUpdated');

                console.log(response.data);
            } catch (error) {
                console.error('Error toggling wishlist:', error);
            }
        },
        async buyDownload(contentId) {

            if (!this.isLoggedIn) {
                this.$route.push('/login');
                return;
            }

            try {
                const response = await this.$axios.get(`http://127.0.0.1:5000/download_purchase/${contentId}`, {
                    responseType: 'blob',
                    headers: {
                        Authorization: `Bearer ${sessionStorage.getItem('token')}`,
                    },
                });

                const blob = new Blob([response.data], { type: 'application/pdf' });
                const url = window.URL.createObjectURL(blob);

                const link = document.createElement('a');
                link.href = url;
                link.setAttribute('download', `${this.content.pdf_file_name}`);
                document.body.appendChild(link);
                link.click();

                window.URL.revokeObjectURL(url);
                document.body.removeChild(link);
            } catch (error) {
                console.error('Error purchasing and downloading content:', error);
            }
        },
        handleImageError(event) {
            console.error("Error loading image:", event);
        },
        isLoggedIn() {
            return !!sessionStorage.getItem('token');
        },
    }
};
</script>

<style scoped>
.content {
    position: relative;
    display: flex;
    flex-direction: column;
    row-gap: 0.5rem;
    background-color: rgb(243, 238, 238);
    border-radius: 0.5rem;
    border: 1px solid white;
    box-shadow: rgba(50, 50, 93, 0.25) 0px 50px 100px -20px, rgba(0, 0, 0, 0.3) 0px 30px 60px -30px, rgba(10, 37, 64, 0.35) 0px -2px 6px 0px inset;
    width: 210px;
    z-index: 1;
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

.text-center .btn {
    width: -moz-available;
}

.top-btn {
    position: absolute;
    top: 5px;
    right: 5px;
}
</style>