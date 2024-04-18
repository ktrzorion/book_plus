<template>
  <nav class="navbar bg-dark border-bottom border-body" data-bs-theme="dark">
    <div class="container-fluid d-flex justify-content-between align-items-center">
      <div>
        <a class="navbar-brand">
          <img src="../assets/logo/wht_nbg.png" height="40px" alt="logo not available">
        </a>
        <router-link :to="{ name: 'LibrarianHome'}" v-if="loggedIn && role ==='LIBRARIAN'">
          <i class="fa-solid fa-house px-3 py-2 my-2 profile-link" style="color: #ffffff;"></i>
        </router-link>
        <router-link :to="{ name: 'ReaderHome'}" v-if="loggedIn && role ==='READER'">
          <i class="fa-solid fa-house px-3 py-2 my-2 profile-link" style="color: #ffffff;"></i>
        </router-link>
      </div>
      <div class="d-flex justify-content-center">
        <form class="d-flex" @submit.prevent="search">
          <div class="input-group position-relative">
            <input v-model="searchQuery" class="form-control me-2" type="search" placeholder="Search"
              aria-label="Search">
            <button class="btn btn-outline-success custom-btn" type="submit">Search</button>
          </div>
        </form>
      </div>
      <div class="profile d-flex">
        <div class="librarian mx-4" v-if="role === 'LIBRARIAN'">
          <router-link :to="{ name: 'RequestList'}" v-if="loggedIn">
            <i class="fa-regular fa-comment-dots px-3 py-2 profile-link" style="color: #ffffff;"></i>
          </router-link>
        </div>
          <router-link :to="{ name: 'ReaderWishlist', params: { userId: userId } }" v-if="loggedIn && role === 'READER'">
            <i class="fa-solid fa-clipboard-list px-3 py-2 profile-link" style="color: #ffffff;"></i>
          </router-link>
        <router-link :to="{ name: 'UserProfile', params: { userId: userId } }" v-if="loggedIn">
          <i class="fa-regular fa-user mx-4 px-2 py-2 profile-link" style="color: #ffffff;"></i>
        </router-link>
        <button v-if="loggedIn" @click="logout" class="btn btn-danger">Logout</button>
        <router-link v-else to="/login" class="btn btn-success">Login</router-link>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  data() {
    return {
      searchQuery: "",
      searchResults: [],
      loggedIn: false,
      userId: null,
      role: "",
    };
  },
  mounted() {
    this.checkAuthentication();
  },
  methods: {
    search() {
      if (this.searchQuery.trim() !== "") {
        this.$router.push({ name: 'searchResult', params: { query: this.searchQuery } });
      }
    },
    mounted() {
      this.checkAuthentication();
    },
    async logout() {
      sessionStorage.removeItem('token');
      this.$router.push('/login')
      await this.checkAuthentication();
    },
    async checkAuthentication() {
      const token = sessionStorage.getItem('token');
      if (token) {
        try {
          const response = await fetch('http://127.0.0.1:5000/verify', {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });

          const data = await response.json();

          if (data.authenticated) {
            console.log('User is authenticated:', data.user.username);
            this.loggedIn = true;
            this.userId = data.user.id;
            this.role = data.user.role;
          } else {
            console.log('User is not authenticated.');
            this.loggedIn = false;
          }
        } catch (error) {
          console.error('Error checking login status:', error);
        }
      } else {
        console.log('Token not found in session storage. User is not authenticated.');
        this.loggedIn = false;
      }
    },
  },
};
</script>

<style scoped>
nav {
  z-index: 2;
  position: sticky;
  top: 0;
}

.custom-btn {
  font-size: 0.8rem;
  padding: 0.25rem 0.5rem;
  width: 100px;
}

.search {
  margin-left: 20px;
}

.profile {
  align-items: center;
}

.profile-link {
  font-size: x-large;
}
</style>