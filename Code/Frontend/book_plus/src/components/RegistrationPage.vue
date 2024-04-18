<template>
    <div class="custom-container margin-top text-center mb-2">
        <!-- Bootstrap alert for success or error messages -->
        <div v-if="successMessage" class="alert alert-success" role="alert">
            {{ successMessage }}
        </div>
        <div v-if="errorMessage" class="alert alert-danger" role="alert">
            {{ errorMessage }}
        </div>
        <h2 class="mb-4">Register</h2>
        <form @submit.prevent="registerUser">
            <!-- First row -->
            <div class="row">
                <div class="col-md-3 mb-3">
                    <label for="firstname" class="form-label">First Name:</label>
                    <input v-model="userData.firstname" type="text" class="form-control" required />
                </div>
                <div class="col-md-3 mb-3">
                    <label for="lastname" class="form-label">Last Name:</label>
                    <input v-model="userData.lastname" type="text" class="form-control" required />
                </div>
                <div class="col-md-3 mb-3">
                    <label for="username" class="form-label">Username:</label>
                    <input v-model="userData.username" type="text" class="form-control" required />
                </div>
                <div class="col-md-3 mb-3">
                    <label for="phoneNumber" class="form-label">Phone Number:</label>
                    <input v-model="userData.phoneNumber" type="tel" class="form-control" required />
                </div>
            </div>

            <!-- Second row -->
            <div class="row">
                <div class="col-md-3 mb-3">
                    <label for="gender" class="form-label">Gender:</label>
                    <select v-model="userData.gender" class="form-select" required>
                        <option value="male">Male</option>
                        <option value="female">Female</option>
                        <option value="other">Other</option>
                    </select>
                </div>
                <div class="col-md-3 mb-3">
                    <label for="city" class="form-label">City:</label>
                    <input v-model="userData.city" type="text" class="form-control" required />
                </div>
                <div class="col-md-3 mb-3">
                    <label for="email" class="form-label">Email:</label>
                    <input v-model="userData.email" type="email" class="form-control" required />
                </div>
                <div class="col-md-3 mb-3">
                    <label for="password" class="form-label">Password:</label>
                    <input v-model="userData.password" type="password" class="form-control" required />
                </div>
            </div>

            <!-- Third row -->
            <div class="row">
                <div class="col-md-4 mb-3">
                    <label for="state" class="form-label">State:</label>
                    <input v-model="userData.state" type="text" class="form-control" required />
                </div>
                <div class="col-md-4 mb-3">
                    <label for="zip" class="form-label">ZIP Code:</label>
                    <input v-model="userData.zip" type="text" class="form-control" required />
                </div>
                <div class="col-md-4 mb-3">
                    <label for="address" class="form-label">House Number:</label>
                    <input v-model="userData.address" type="text" class="form-control" required />
                </div>
            </div>

            <!-- Fifth row -->
            <div class="row">
                <div class="mb-3">
                    <label for="role" class="form-label">Role:</label>
                    <div class="btn-group visibility col-12 pt-3 px-2 py-2" role="group"
                        aria-label="Basic radio toggle button group">
                        <input v-model="userData.role" type="radio" class="btn-check" name="btnradio" id="btnradio1"
                            value="READER">
                        <label class="btn btn-outline-primary" for="btnradio1"><b>READER</b></label>

                        <input v-model="userData.role" type="radio" class="btn-check" name="btnradio" id="btnradio2"
                            value="LIBRARIAN">
                        <label class="btn btn-outline-success" for="btnradio2"><b>LIBRARIAN</b></label>

                        <input v-model="userData.role" type="radio" class="btn-check" name="btnradio" id="btnradio3"
                            value="ADMIN" disabled>
                        <label class="btn btn-outline-danger" for="btnradio3"><b>ADMIN</b></label>
                    </div>
                </div>
            </div>

            <!-- Submit button -->
            <button type="submit" class="btn btn-primary">Register</button>
        </form>
        <div class="mt-3 text-center">
            Existing User?
            <router-link to="/login" class="btn btn-sm btn-dark">LOGIN</router-link>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            userData: {
                firstname: '',
                lastname: '',
                username: '',
                phoneNumber: '',
                gender: '',
                city: '',
                email: '',
                password: '',
                state: '',
                zip: '',
                address: '',
                role: 'READER'
            },
            validationErrors: {},
            successMessage: '',
            errorMessage: ''
        };
    },
    methods: {
        async registerUser() {
            this.validationErrors = {};
            this.successMessage = '';
            this.errorMessage = '';
            console.log(this.validationErrors)
            // Perform validations
            if (this.userData.username.length > 20) {
                this.validationErrors.username = "Username must be at most 20 characters long.";
            }
            // Password validation
            const passwordRegex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()-_+=]).{8,}$/;
            if (!passwordRegex.test(this.userData.password)) {
                this.validationErrors.password = "Password must be at least 8 characters long and contain at least one lowercase letter, one uppercase letter, one digit, and one special character.";
            }

            // State validation
            const stateRegex = /^[a-zA-Z\s]*$/;
            if (!stateRegex.test(this.userData.state)) {
                this.validationErrors.state = "State name can only contain alphabets and spaces.";
            }

            // Check if there are any validation errors
            if (Object.keys(this.validationErrors).length > 0) {
                return; // Stop form submission if there are validation errors
            }

            try {
                // Assuming you are using axios for making HTTP requests
                const response = await this.$axios.post('http://127.0.0.1:5000/register', this.userData);
                console.log(response);
                // Check if the response status is OK (2xx)
                if (response.status === 201) {
                    // Handle success, you may want to redirect to a different page
                    this.successMessage = response.data.message;
                    console.log(response.data.message);
                    this.$nextTick(() => {});
                    this.clearForm();
                    this.$router.push('/login')
                } else {
                    // Handle other status codes, show an alert or toast message
                    console.error('Registration failed:', response.data.error, response.data.details);
                    this.$nextTick(() => {});
                }
            } catch (error) {
                // Handle error, show an alert or toast message
                console.error('Registration failed:', error.response.data.error, error.response.data.details);
                this.$nextTick(() => {});
            }
        },
        clearForm() {
            // Reset all form fields to their initial values
            this.userData = {
                firstname: '',
                lastname: '',
                username: '',
                phoneNumber: '',
                gender: '',
                city: '',
                email: '',
                password: '',
                state: '',
                zip: '',
                address: '',
                role: ''
            };
        }

    }
};
</script>

<style scoped>
.custom-container {
    border-radius: 1rem;
    max-width: 900px;
    margin: auto;
    background-color: rgba(0, 0, 0, 0.3);
    color: #fff;
    padding: 15px
}

.margin-top {
    margin-top: 90px;
}

.form-label {
    font-weight: bold;
}

.form-control,
.form-select {
    margin-bottom: 15px;
}

.btn-primary {
    width: 100%;
}

.btn {
    border-radius: 15px;
}
</style>