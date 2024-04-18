<!-- AddBook.vue -->
<template>
    <div class="container">
        <h2>Add New Book/Document</h2>
        <form @submit.prevent="submitForm">
            <div class="form-group">
                <label for="title">Title</label>
                <input v-model="title" type="text" class="form-control" id="title" required>
            </div>
            <div class="form-group">
                <label for="author">Author</label>
                <input v-model="author" type="text" class="form-control" id="author" required>
            </div>
            <div class="form-group">
                <label for="category">Category</label>
                <input v-model="category" type="text" class="form-control" id="category" required>
            </div>
            <div class="form-group">
                <label for="numberOfPages">Number of Pages</label>
                <input v-model="numberOfPages" type="number" class="form-control" id="numberOfPages" required>
            </div>
            <div class="form-group">
                <label for="publishYear">Publish Year</label>
                <input v-model="publishYear" type="number" class="form-control" id="publishYear" required>
            </div>
            <div class="form-group">
                <label for="quantityAvailable">Quantity Available</label>
                <input v-model="quantityAvailable" type="number" class="form-control" id="quantityAvailable" required>
            </div>
            <button type="submit" class="btn btn-primary">Add Book/Document</button>
        </form>
    </div>
</template>
  
<script>
export default {
    data() {
        return {
            title: '',
            author: '',
            category: '',
            numberOfPages: '',
            publishYear: '',
            quantityAvailable: '',
        };
    },
    methods: {
        async submitForm() {
            try {
                // Your API call to the add book route here
                const response = await this.$axios.post('/add_books', {
                    title: this.title,
                    author: this.author,
                    category: this.category,
                    numberOfPages: this.numberOfPages,
                    publishYear: this.publishYear,
                    quantityAvailable: this.quantityAvailable,
                });

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