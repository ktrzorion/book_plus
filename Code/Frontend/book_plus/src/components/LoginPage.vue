<template>
    <div class="containerr">
        <h2>Login</h2>
        <form @submit.prevent="submitForm">
            <div class="form-group">
                <label for="input">Email/Username</label>
                <input v-model="input" type="text" class="form-control" id="input" required>
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input v-model="password" type="password" class="form-control" id="password" required>
            </div>
            <button type="submit" class="btn btn-primary">Login</button>
        </form>
        <div class="mt-3 text-center">
            New User?
            <router-link to="/register" class="btn btn-sm btn-dark">REGISTER</router-link>
        </div>
    </div>
</template>
  
<script>
export default {
    data() {
        return {
            input: "",
            password: "",
        };
    },
    methods: {
        submitForm() {
            const formData = {
                input: this.input,
                password: this.password
            };

            this.$axios.post("http://127.0.0.1:5000/login", formData)
                .then(response => {
                    const token = response.data.token;
                    if (token) {
                        sessionStorage.setItem("token", token);
                        const user = this.$jwtDecode(token);
                        if (user && user.role === "ADMIN") {
                            this.$router.push("/admin-home").then(() => {
                                window.location.reload();
                            });
                        } else if (user && user.role === "LIBRARIAN") {
                            this.$router.push("/librarian-home").then(() => {
                                window.location.reload();
                            });
                        } else if (user && user.role === "READER") {
                            this.$router.push("/reader-home").then(() => {
                                window.location.reload();
                            });
                        }
                    } else {
                        console.error("Token not present in the response:", response);
                    }
                })
                .catch(error => {
                    console.error("Login failed:", error.response.data.error);
                }
                );
        }
    }
};
</script>
  
<style scoped>
.containerr {
    margin: 190px auto;
    max-width: 400px;
    padding: 20px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    background-color: rgba(0, 0, 0, 0.3);
    color: #fff;
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