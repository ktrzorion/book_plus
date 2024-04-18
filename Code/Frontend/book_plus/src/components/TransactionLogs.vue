<template>
    <div class="custom-container">
        <h2>Transaction Logs</h2>
        <table class="table">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>User ID</th>
                    <th>Action</th>
                    <th>Timestamp</th>
                    <th>Content ID</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="log in transactionLogs" :key="log.id">
                    <td>{{ log.id }}</td>
                    <td>{{ log.user_id }}</td>
                    <td>{{ log.action }}</td>
                    <td>{{ formatDate(log.timestamp) }}</td>
                    <td>{{ log.content_id }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
import { format } from 'date-fns';

export default {
    data() {
        return {
            transactionLogs: [],
        };
    },
    mounted() {
        // Fetch transaction logs and set the initial value
        this.fetchTransactionLogs();
    },
    methods: {
        formatDate(dateString) {
            return format(new Date(dateString), 'yyyy-MM-dd HH:mm:ss');
        },
        async fetchTransactionLogs() {
            try {
                // Your API call to fetch transaction logs here
                const response = await this.$axios.get('http://127.0.0.1:5000/transaction_logs', {
                    headers: {
                        Authorization: `Bearer ${sessionStorage.getItem('token')}`
                    }
                });

                // Set the transaction logs in the component state
                this.transactionLogs = response.data.transaction_logs;
            } catch (error) {
                // Handle errors
                console.error(error.response.data);
            }
        },
    },
};
</script>

<style scoped>
.custom-container {
    color: white;
    margin: 50px auto;
    width: 80%;
}

.table {
    text-align: center;
    width: 100%;
    margin-bottom: 1rem;
    border-collapse: separate;
    border-spacing: 1rem;
}

th{
    background-color: rgba(0, 0, 0, 0.336);
}

td{
    background-color: rgba(0, 0, 0, 0.075);
}

th, td{
    color: white;
}
</style>