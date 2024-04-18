<!-- BorrowBook.vue -->
<template>
    <div class="container">
        <h2>Borrow Book</h2>
        <form @submit.prevent="submitForm">
            <div class="form-group">
                <label for="bookId">Book ID</label>
                <input v-model="bookId" type="number" class="form-control" id="bookId" required>
            </div>
            <button type="submit" class="btn btn-primary">Borrow Book</button>
        </form>
    </div>
</template>
  
<script>
export default {
    data() {
        return {
            bookId: null,
        };
    },
    methods: {
        async submitForm() {
            try {
                // Your API call to the borrow book route here
                const response = await this.$axios.post(`/borrow/${this.bookId}`);

                // Handle the response accordingly
                console.log(response.data);
            } catch (error) {
                // Handle errors
                console.error(error.response.data);
            }
        },
    },
};
</script>
  
<style scoped>
/* Add your custom styles or Bootstrap classes here */
.container {
    max-width: 400px;
    margin: auto;
    padding: 20px;
    margin-top: 50px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    border-radius: 5px;
}

.form-group {
    margin-bottom: 20px;
}

label {
    display: block;
    margin-bottom: 8px;
    font-weight: bold;
}

input {
    width: 100%;
    padding: 10px;
    font-size: 16px;
    border: 1px solid #ccc;
    border-radius: 5px;
}

button {
    display: block;
    width: 100%;
    padding: 10px;
    font-size: 16px;
    background-color: #007bff;
    color: #fff;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

button:hover {
    background-color: #0056b3;
}
</style>  