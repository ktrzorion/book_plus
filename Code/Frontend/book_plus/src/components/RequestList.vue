<template>
    <div class="custom-container">
        <table class="table">
            <thead>
                <tr>
                    <th>User ID</th>
                    <th>Content ID</th>
                    <th>Actions</th>
                    <th>Reject</th>
                    <th>Details</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="request in issueRequests" :key="request.id">
                    <td>{{ request.userId }}</td>
                    <td>{{ request.contentId }}</td>
                    <td>
                        <button class="btn btn-success"
                            @click="acceptRequest(request.contentId, request.userId,)">Accept</button>
                    </td>
                    <td>
                        <button class="btn btn-danger"
                            @click="rejectRequest(request.contentId, request.userId,)">Reject</button>
                    </td>
                    <td>
                        <router-link class="btn btn-warning" :to="{ name: 'DetailView', params: { contentId: request.contentId, userId: request.userId } }">
                            <i class="fa-solid fa-eye"></i>
                        </router-link>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>

export default {
    data() {
        return {
            issueRequests: []
        }
    },
    methods: {
        async acceptRequest(contentId, userId) {
            try {
                await this.$axios.post(`http://127.0.0.1:5000/accept_request/${contentId}/${userId}`, null, {
                    headers: {
                        Authorization: `Bearer ${sessionStorage.getItem('token')}`,
                    },
                });
                this.fetchIssueRequests()
                console.log('Issue Request Accepted');
            } catch (error) {
                console.error('Error issuing content:', error);
            }
        },
        async rejectRequest(contentId, userId) {
            try {
                await this.$axios.post(`http://127.0.0.1:5000/reject_request/${contentId}/${userId}`, null, {
                    headers: {
                        Authorization: `Bearer ${sessionStorage.getItem('token')}`,
                    },
                });
                this.fetchIssueRequests()
                console.log('Issue Request Rejected');
            } catch (error) {
                console.error('Error issuing content:', error);
            }
        },
        async fetchIssueRequests() {
            try {
                const response = await this.$axios.get('http://127.0.0.1:5000/fetch_issue_requests', {
                    headers: {
                        Authorization: `Bearer ${sessionStorage.getItem('token')}`
                    }
                });
                this.issueRequests = response.data;
            } catch (error) {
                console.error('Error fetching issue requests:', error);
            }
        },
        closeModal() {
            this.showModal = false;
        },
    },
    mounted() {
        this.fetchIssueRequests();
    }
}
</script>

<style scoped>
.custom-container {
    padding: 10px;
    background-color: rgba(0, 0, 0, 0.205);
    border-radius: 1rem;
    margin: 20px auto;
    width: 80%;
}

.table {
    text-align: center;
    width: 100%;
    border-collapse: separate;
    border-radius: 1rem;
    overflow: hidden;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
}

.table th,
.table td {
    padding: 12px;
    border: transparent;
}
</style>