<template>
    <div class="custom-container">
        <div class="add-section-form">
            <form @submit.prevent="updateSection">
                <label for="sectionName" class="my-4">Section Name:</label>
                <input v-model="sectionName" type="text" id="sectionName" required>
                <div class="row mt-4">
                    <div class="col-6 d-flex align-items-center justify-content-center">
                        <button class="btn btn-secondary" type="submit">Update</button>
                    </div>
                    <div class="col-6 d-flex align-items-center justify-content-center">
                        <router-link class="btn btn-danger" to="/librarian-home">Cancel</router-link>
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            sectionName: '',
        };
    },
    mounted() {
        this.fetchSection();
    },
    methods: {
        async fetchSection() {
            const sectionId = this.$route.params.sectionId;
            console.log(sectionId)
            const apiUrl = `http://127.0.0.1:5000/get-section/${sectionId}`;

            try {
                const response = await fetch(apiUrl, {
                    headers: {
                        Authorization: `Bearer ${sessionStorage.getItem('token')}`
                    }
                });
                const data = await response.json();

                if (response.ok) {
                    this.sectionName = data.name;
                } else {
                    console.error('Failed to fetch section data');
                }
            } catch (error) {
                console.error('Error fetching section data:', error);
            }
        },
        updateSection() {
            const sectionId = this.$route.params.sectionId;
            const putData = {
                name: this.sectionName,
            };
            const token = sessionStorage.getItem("token");

            axios.put(`http://127.0.0.1:5000/update-section/${sectionId}`, putData, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            })
                .then(response => {
                    console.log(response.data.message);
                    this.$router.push('/librarian-home');
                })
                .catch(error => {
                    console.error('Error updating section:', error.response ? error.response.data : error.message);
                });
        },
    },
};
</script>
  
<style scoped>
.custom-container {
    width: 400px;
    color: white;
    position: fixed;
    text-align: center;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: rgba(0, 0, 0, 0.199);
    padding: 20px;
    border-radius: 1rem;
}

.can {
    margin-top: 23px;

}
</style>