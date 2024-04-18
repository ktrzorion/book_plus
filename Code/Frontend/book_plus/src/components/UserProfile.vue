<template>
    <div class="custom-container">
        <div class="details">
            <h3>User Details</h3>
            <div class="user-details-container" v-if="user">
                <div class="user-detail-row">
                    <div class="user-detail-column">
                        <p><strong class="c-wid">ID:</strong> {{ user.id }}</p>
                        <p><strong class="c-wid">First Name:</strong> {{ user.firstname }}</p>
                        <p><strong class="c-wid">Last Name:</strong> {{ user.lastname }}</p>
                        <p><strong class="c-wid">Username:</strong> {{ user.username }}</p>
                        <p><strong class="c-wid">Phone Number:</strong> {{ user.phoneNumber }}</p>
                        <p><strong class="c-wid">Email:</strong> {{ user.email }}</p>
                    </div>
                    <div class="user-detail-column">
                        <p><strong class="c-wid">Gender:</strong> {{ user.gender }}</p>
                        <p><strong class="c-wid">Address:</strong> {{ user.address }}</p>
                        <p><strong class="c-wid">City:</strong> {{ user.city }}</p>
                        <p><strong class="c-wid">State:</strong> {{ user.state }}</p>
                        <p><strong class="c-wid">Zip:</strong> {{ user.zip }}</p>
                        <p><strong class="c-wid">Role:</strong> {{ user.role }}</p>
                    </div>
                </div>
            </div>
            <div v-else>
                <p>Loading...</p>
            </div>
        </div>
    </div>
</template>

<style scoped>
.custom-container {
    width: 80%;
    background-color: rgba(0, 0, 0, 0.25);
    margin: 120px auto;
    border-radius: 1rem;
}

.details {
    border-radius: 8px;
    padding: 20px;
}

.user-details-container {
    display: flex;
    flex-direction: column;
}

.user-detail-row {
    display: flex;
}

.user-detail-column {
    flex: 1;
    margin-right: 20px;
}

.user-detail-column:last-child {
    margin-right: 0;
}

strong.c-wid {
    display: inline-block;
    width: 150px;
    border-radius: 1rem;
}

h3 {
    color: #ffffff;
    font-size: 24px;
    margin-bottom: 20px;
}

p {
    margin: 5px 0;
    font-size: 16px;
    color: #ffffff;
}

strong {
    font-weight: bold;
}
</style>


<script>
export default {
    data() {
        return {
            user: null
        };
    },
    mounted() {
        const userId = this.$route.params.userId;
        this.fetchUserDetails(userId);
    },
    methods: {
        async fetchUserDetails(userId) {
            try {
                const response = await fetch(`http://127.0.0.1:5000/user/${userId}`, {
                    headers: {
                        Authorization: `Bearer ${sessionStorage.getItem('token')}`,
                    },
                });
                const data = await response.json();
                this.user = data;
            } catch (error) {
                console.error('Error fetching user details:', error);
            }
        }
    }
};
</script>