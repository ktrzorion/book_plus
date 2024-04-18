<template>
    <div class="custom-container">
        <h2>Details</h2>
        <p><strong>Username:</strong> {{ userDetails.username }}</p>
        <p><strong>Content Name:</strong> {{ contentDetails.contentName }}</p>
        <p><strong>Section Name:</strong> {{ contentDetails.sectionName }}</p>
        <div class="d-flex">
            <button class="btn btn-success mx-4" @click="acceptRequest(contentId, userId)">Accept</button>
            <button class="btn btn-danger mx-4" @click="rejectRequest(contentId, userId)">Reject</button>
            <router-link :to="{ name: 'RequestList'}" class="btn btn-primary mx-4"><i class="fa-solid fa-angles-left"></i></router-link>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            userDetails: {},
            contentDetails: {},
            contentId: null,
            userId: null
        }
    },
    methods: {
        async viewDetails() {
            try {
                this.contentId = this.$route.params.contentId;
                this.userId = this.$route.params.userId;

                const response = await this.$axios.get(`http://127.0.0.1:5000/detail_view/${this.contentId}/${this.userId}`, {
                    headers: {
                        Authorization: `Bearer ${sessionStorage.getItem('token')}`
                    }
                });

                this.userDetails = response.data;
                this.contentDetails = response.data;
                console.log(response.data)
            } catch (error) {
                console.error('Error fetching details:', error);
            }
        },
        async acceptRequest(contentId, userId) {
            try {
                this.contentId = this.$route.params.contentId;
                this.userId = this.$route.params.userId;

                await this.$axios.post(`http://127.0.0.1:5000/accept_request/${contentId}/${userId}`, null, {
                    headers: {
                        Authorization: `Bearer ${sessionStorage.getItem('token')}`,
                    },
                });
                this.$router.push('/request-list')
                console.log('Issue Request Accepted');
            } catch (error) {
                console.error('Error issuing content:', error);
            }
        },
        async rejectRequest(contentId, userId) {
            try {
                this.contentId = this.$route.params.contentId;
                this.userId = this.$route.params.userId;

                await this.$axios.post(`http://127.0.0.1:5000/reject_request/${contentId}/${userId}`, null, {
                    headers: {
                        Authorization: `Bearer ${sessionStorage.getItem('token')}`,
                    },
                });
                this.$router.push('/request-list')
                console.log('Issue Request Rejected');
            } catch (error) {
                console.error('Error issuing content:', error);
            }
        },
    },
    mounted() {
        this.viewDetails();
    }
}
</script>

<style scoped>
.custom-container {
    padding: 15px;
    margin: 70px auto;
    width: 40%;
    border-radius: 2rem;
    background-color: rgba(0, 0, 0, 0.315);
    color: white;
    display: flex;
    flex-direction: column;
    row-gap: 2rem;
    align-items: center;
    padding-top: 2rem;
}

.modal-content {
    background-color: #fefefe;
    margin: 10% auto;
    padding: 20px;
    border: 1px solid #888;
    width: 80%;
}

.close {
    color: #aaa;
    float: right;
    font-size: 28px;
    font-weight: bold;
}

.close:hover,
.close:focus {
    color: black;
    text-decoration: none;
    cursor: pointer;
}
</style>