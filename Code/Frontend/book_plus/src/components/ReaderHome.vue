<template>
    <div class="custom-container">
        <section class="single-container">
            <div class="wrapper" v-for="section in sections" :key="section.id">

                <h2 class="my2">{{ section.name }}</h2>

                <div class="slider-content">
                    <content-card v-for="content in filteredContents(section.id)" :key="content.id" :content="content"
                        :decodedImage="content.decodedImage" :isRead="content.isRead" :isRequested="content.isRequested"
                        @content-updated="updatedContent"></content-card>
                </div>
            </div>
        </section>
    </div>
</template>

<script>
import ContentCard from './ContentCard.vue'
export default {
    components: {
        ContentCard,
    },
    data() {
        return {
            contents: [],
            sections: [],
            selectedSection: null,
            selectedContent: null,
            isCreatingSection: true,
            loadingSectionContent: false,
            cardWidthPercentage: 20,
        };
    },
    mounted() {
        this.fetchContents();
        this.fetchSections();
    },
    methods: {
        updatedContent(){
            this.fetchContents()
        },
        filteredContents(sectionId) {
            return this.contents
                .filter((content) => content.section === sectionId)
                .map((content) => {
                    const decodedImage = this.getDecodedImage(content);
                    return { ...content, decodedImage };
                });
        },
        async fetchContents() {
            const token = sessionStorage.getItem('token');
            const decodedToken = this.$jwtDecode(token);
            const userId = decodedToken.id;
            try {
                const response = await this.$axios.get(`http://127.0.0.1:5000/user/fetch-content/${userId}`);
                this.contents = response.data.contents;
            } catch (error) {
                console.error('Error fetching user contents:', error);
            }
        },
        async fetchSections() {
            this.loadingSectionContent = true;
            try {
                const response = await this.$axios.get('http://127.0.0.1:5000/fetch-sections');
                this.sections = response.data.sections;
            } catch (error) {
                console.error('Error fetching sections:', error);
            } finally {
                this.loadingSectionContent = false;
            }
        },
        getDecodedImage(content) {
            const decodedImage = `data:image/${content.imageType};base64, ${content.image}`;
            return decodedImage;
        },
        handleImageError(event) {
            console.error("Error loading image:", event);
        }
    },
};
</script>

<style scoped>
.custom-container {
    display: flex;
    flex-direction: column;
    row-gap: 2rem;
    align-items: center;
    padding-top: 2rem;
}

.single-container {
    background-color: rgba(0, 0, 0, 0.30);
    width: 85%;
    height: 100%;
    padding: 3rem;
    border-radius: 1rem;
    box-shadow: rgba(60, 64, 67, 0.3) 0px 1px 2px 0px, rgba(60, 64, 67, 0.15) 0px 2px 6px 2px;
}

.wrapper {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    width: 100%;
    overflow: hidden;
}

.wrapper h2 {
    font-size: 30px;
    line-height: 44px;
    color: white;
    font-weight: 700;
    font-family: Arial, Helvetica, sans-serif;
    border-bottom: 2px solid lightgray;
}

.slider-content {
    overflow-x: scroll;
    scroll-snap-type: x mandatory;
    display: flex;
    column-gap: 2rem;
    width: 100%;
    padding-bottom: 1rem;
}

.slider-content::-webkit-scrollbar {
    display: none;
    width: 0;
}
</style>
