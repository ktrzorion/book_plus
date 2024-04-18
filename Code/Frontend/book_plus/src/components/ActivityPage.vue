<template>
    <div class="custom-container">
        <div class="data d-flex justify-content-between">
            <h2>Current Reader Count: {{ currentReaderCount }}</h2>
            <h2>Total Reader Count: {{ totalReaderCount }}</h2>
            <h2>Wishlist Count: {{ wishlistCount }}</h2>
        </div>
        <table class="table table-striped table-bordered">
            <thead class="thead-dark">
                <tr>
                    <th>Content ID</th>
                    <th>Title</th>
                    <th>Username</th>
                    <th>Section Name</th>
                    <th>Borrow Date</th>
                    <th>Returned</th>
                    <th>Return Date</th>
                    <th>Reissue Count</th>
                    <th>Revoke</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(row, index) in tableData" :key="index">
                    <td>{{ row.content_id }}</td>
                    <td>{{ row.title }}</td>
                    <td>{{ row.username }}</td>
                    <td>{{ row.section_name }}</td>
                    <td>{{ row.borrow_date }}</td>
                    <td>{{ row.returned }}</td>
                    <td>{{ row.last_return_date }}</td>
                    <td>{{ row.reissue_count }}</td>
                    <td><button class="btn btn-danger btn-sm"
                            @click="revokeAccess(row.content_id, row.user_id)">Revoke</button></td>
                </tr>
            </tbody>
        </table>
        <BottomHome />
    </div>
</template>

<script>
import axios from 'axios';
import BottomHome from './BottomHome.vue';

export default {
    components: {
        BottomHome,
    },
    data() {
        return {
            contentId: null,
            tableData: [],
            currentReaderCount: 0,
            totalReaderCount: 0,
            wishlistCount: 0
        };
    },
    mounted() {
        this.fetchData();
        this.fetchCounts();
    },
    methods: {
        revokeAccess(contentId, userId) {
            axios.post('http://127.0.0.1:5000/revoke-access', { contentId, userId },{
                headers:{
                    Authorization: `Bearer ${sessionStorage.getItem('token')}`
                }
            })
                .then(response => {
                    this.fetchCounts()
                    this.fetchData()
                    console.log(response.data);
                })
                .catch(error => {
                    console.error(error);
                });
        },
        fetchData() {
            const contentId = this.$route.params.contentId;
            const apiUrl = `http://127.0.0.1:5000/activity-data/${contentId}`;

            axios.get(apiUrl, {
                headers: {
                    Authorization: `Bearer ${sessionStorage.getItem('token')}`,
                }
            })
                .then(response => {
                    this.tableData = response.data;
                })
                .catch(error => {
                    console.error('Error fetching data:', error);
                });
        },
        fetchCounts() {
            const contentId = this.$route.params.contentId;

            // Fetch current reader count
            axios.get(`http://127.0.0.1:5000/current-reader-count/${contentId}`, {
                headers: {
                    Authorization: `Bearer ${sessionStorage.getItem('token')}`,
                }
            })
                .then(response => {
                    this.currentReaderCount = response.data.currentReaderCount;
                })
                .catch(error => {
                    console.error('Error fetching current reader count:', error);
                });

            // Fetch total reader count
            axios.get(`http://127.0.0.1:5000/total-reader-count/${contentId}`, {
                headers: {
                    Authorization: `Bearer ${sessionStorage.getItem('token')}`,
                }
            })
                .then(response => {
                    this.totalReaderCount = response.data.totalReaderCount;
                })
                .catch(error => {
                    console.error('Error fetching total reader count:', error);
                });

            // Fetch wishlist count
            axios.get(`http://127.0.0.1:5000/wishlist-count/${contentId}`, {
                headers: {
                    Authorization: `Bearer ${sessionStorage.getItem('token')}`,
                }
            })
                .then(response => {
                    this.wishlistCount = response.data.wishlistCount;
                })
                .catch(error => {
                    console.error('Error fetching wishlist count:', error);
                });
        },
    },
};
</script>

<style scoped>
.custom-container {
    margin: 20px;
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

.data {
    margin: auto;
    text-align: center;
    width: 80%;
    color: white;
}
</style>