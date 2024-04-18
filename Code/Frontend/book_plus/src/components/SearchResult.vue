<template>
  <div class="custom-container">
    <section class="single-container">
      <div v-if="searchResults && searchResults.length > 0">
        <h3 class="mb-4">Content Results</h3>
        <!-- Display content cards -->
        <div class="slider-content">
          <content-card v-for="(result, index) in searchResults" :key="index" :content="result"
            :isIssued="result.isIssued" :isRequested="result.isRequested" :decodedImage="getDecodedImage(result)" :isRead="result.isRead"
            @content-updated="updatedContent"></content-card>
        </div>
      </div>
      <div v-else class="center">
        <h2>NO MATCH FOUND</h2>
      </div>
    </section>
  </div>
</template>

<script>
import ContentCard from './ContentCard.vue'
export default {
  components: {
    ContentCard,
  },
  data() {
    return {
      searchResults: null,
      results: [],
    };
  },
  async created() {
    await this.fetchSearchResults();
  },
  watch: {
    '$route'(to, from) { // eslint-disable-line no-unused-vars
      this.fetchSearchResults();
    }
  },
  methods: {
    updatedContent() {
      this.fetchSearchResults()
    },
    async fetchSearchResults() {
      const query = this.$route.params.query;
      try {
        let headers = {};
        const token = sessionStorage.getItem('token');
        if (token) {
          headers = {
            Authorization: `Bearer ${token}`
          };
        }

        const apiUrl = `http://127.0.0.1:5000/search-result?query=${query}`;
        const response = await fetch(apiUrl, {
          headers: headers,
        });

        if (!response.ok) {
          throw new Error(`Failed to fetch search results: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();
        this.searchResults = data.results;
      } catch (error) {
        console.error("Error fetching search results:", error);
      }
    },
    getDecodedImage(content) {
      const decodedImage = `data:image/${content.imageType};base64, ${content.image}`;
      return decodedImage;
    },
  },
};
</script>

<style scoped>
.custom-container {
  display: flex;
  flex-direction: column;
  row-gap: 2rem;
  align-items: center;
  padding-top: 2rem;
}

.single-container {
  color: white;
  background-color: rgba(0, 0, 0, 0.30);
  width: 85%;
  height: 100%;
  padding: 3rem;
  border-radius: 1rem;
  box-shadow: rgba(60, 64, 67, 0.3) 0px 1px 2px 0px, rgba(60, 64, 67, 0.15) 0px 2px 6px 2px;
}

.slider-content {
  overflow-x: scroll;
  scroll-snap-type: x mandatory;
  display: flex;
  column-gap: 2rem;
  width: 100%;
  padding-bottom: 1rem;
}

.slider-content::-webkit-scrollbar {
  display: none;
  width: 0;
}
</style>