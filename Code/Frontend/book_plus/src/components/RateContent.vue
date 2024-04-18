<template>
    <div class="custom-container">
        <h2><u>Rate Content</u></h2>
        <div>
            <div class="stars">
                <span v-for="star in 5" :key="star" @click="rateContent(star)"
                    :class="{ 'rated': star <= selectedRating }">&#9733;</span>
            </div>
        </div>
        <div>
            <textarea v-model="comment" placeholder="Add your comment" style="width: 500px; height: 100px;"></textarea>
        </div>
        <div class="row cus-btn mb-2">
            <button class="col-4 btn btn-success" @click="submitRating()">Submit Rating</button>
            <router-link class="col-4 btn btn-danger" to="/reader-home">Cancel</router-link>
        </div>
    </div>
</template>

<script>
export default {
    props: ['id'],
    data() {
        return {
            selectedRating: 0,
            comment: '',
            contentId: null
        };
    },
    created() {
        // Fetch contentId from route parameters
        this.contentId = this.$route.params.contentId;

        // Fetch previous rating and comment
        this.fetchPreviousRating();
    },
    methods: {
        async fetchPreviousRating() {
            try {
                const response = await this.$axios.get(`http://127.0.0.1:5000/get_previous_rating/${this.contentId}`, {
                    headers: {
                        Authorization: `Bearer ${sessionStorage.getItem('token')}`,
                    },
                });
                const { rating, comment } = response.data;

                // Set the data properties with the fetched values
                this.selectedRating = rating;
                this.comment = comment;
            } catch (error) {
                console.error('Error fetching previous rating:', error);
            }
        },
        rateContent(star) {
            this.selectedRating = star;
        },
        async submitRating() {
            try {
                // Assuming you have a server-side route for rating content
                await this.$axios.post(`http://127.0.0.1:5000/rate_content/${this.contentId}`, {
                    rating: this.selectedRating,
                    comment: this.comment
                }, {
                    headers: {
                        Authorization: `Bearer ${sessionStorage.getItem('token')}`,
                    },
                });
                this.$router.push({ name: 'ReaderHome' }); 

            } catch (error) {
                console.error('Error rating content:', error);
            }
        }
    }
};
</script>

<style scoped>
.custom-container {
    color: white    ;
    margin: 120px auto;
    display: flex;
    flex-direction: column;
    text-align: center;
    row-gap: 2rem;
    align-items: center;
    padding-top: 2rem;
    background-color: rgba(0, 0, 0, 0.207);
}
.rated {
    color: gold;
}
.all-center{
    align-items: center;
    justify-content: center;
    align-items: center;
}
.cus-btn{
    justify-content: center;
    column-gap: 2rem;
}
.custom-container .cus-btn .btn {
  width: 150px;
}
.stars{
    font-size: xx-large;
}
</style>