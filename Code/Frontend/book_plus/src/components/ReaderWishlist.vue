<template>
  <div class="custom-container">
    <section class="single-container">
      <h3 class="mb-4">Wishlist</h3>
      <div v-if="wishlist.length> 0">
        <div class="slider-content">
          <content-card v-for="(result, index) in wishlist" :key="index" :content="result" :isRequested="result.isRequested" :is-read="result.isRead" :isIssued="result.isIssued"
            :decodedImage="getDecodedImage(result)" @content-updated="updatedContent"></content-card>
        </div>
      </div>
      <div v-else>
        <p>No items in wishlist.</p>
      </div>
    </section>
  </div>
</template>

<script>
import ContentCard from './ContentCard.vue';
export default {
  components: {
    ContentCard,
  },
  data() {
    return {
      wishlist: []
    };
  },
  mounted() {
    const userId = this.$route.params.userId;
    this.fetchUserWishlist(userId);
  },
  methods: {
    updatedContent() {
      const userId = this.$route.params.userId;
      this.fetchUserWishlist(userId)
    },
    async fetchUserWishlist(userId) {
      try {
        const response = await fetch(`http://127.0.0.1:5000/wishlist/${userId}`, {
          headers: {
            Authorization: `Bearer ${sessionStorage.getItem('token')}`,
          },
        });
        const data = await response.json();
        this.wishlist = data.wishlist;
      } catch (error) {
        console.error('Error fetching wishlist:', error);
      }
    },
    getDecodedImage(content) {
      const decodedImage = `data:image/${content.imageType};base64, ${content.image}`;
      return decodedImage;
    },
  }
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