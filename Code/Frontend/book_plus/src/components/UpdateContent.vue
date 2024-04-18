<template>
  <div class="container">
    <h2><b>Update Content</b></h2>
    <form @submit.prevent="submitForm">
      <div class="row">
        <!-- Image input in a separate column -->
        <div class="col-md-6">
          <div class="form-group">
            <label for="image">Image</label>
            <input type="file" ref="imageInput" @change="handleImageChange">
          </div>
        </div>
        <div class="col-md-6">
          <div class="form-group">
            <label for="pdfFile">PDF File</label>
            <input type="file" ref="pdfInput" @change="handlePdfChange">
          </div>
        </div>
      </div>

      <div class="row">
        <!-- Title, Author, and Category inputs in columns -->
        <div class="col-12">
          <div class="form-group">
            <label for="title">Title</label>
            <input v-model="content.title" type="text" class="form-control" id="title" required>
          </div>
        </div>
      </div>

      <div class="row">
        <div class="col-7">
          <div class="form-group">
            <label for="author">Author(s)</label>
            <input v-model="content.author" type="text" class="form-control" id="author" required>
          </div>
        </div>
        <!-- Number of Pages, Publish Year, and Quantity Available inputs in columns -->
        <div class="col-md-3">
          <div class="form-group">
            <label for="publishYear">Publish Year</label>
            <input v-model="content.publish_year" type="number" class="form-control" id="publishYear" required>
          </div>
        </div>
        <div class="col-md-2">
          <div class="form-group">
            <label for="price">Price (in Rs.)</label>
            <input v-model="content.price" type="number" class="form-control" id="price" required>
          </div>
        </div>
      </div>

      <div class="row">
        <!-- Submit button in a separate column -->
        <div class="col-8 d-flex align-items-center justify-content-center px-4 mx-4">
          <button type="submit" class="btn btn-primary">Update</button>
        </div>
        <div class="col-3 d-flex align-items-center justify-content-center">
          <router-link class="btn btn-danger" to="/librarian-home">Cancel</router-link>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      content: {
        title: '',
        author: '',
        number_of_pages: 0,
        publish_year: 0,
        price: 0,
        image: null,
        pdf: null,
        pdf_file_name: null
      },
      existingSection: '',
      oldImage: null,
      oldPdf: null
    };
  },
  mounted() {
    const contentId = this.$route.params.contentId;
    if (contentId) {
      this.fetchContentDetails(contentId);
    }
  },
  methods: {
    fetchContentDetails(contentId) {
      const token = sessionStorage.getItem('token');

      axios.get(`http://127.0.0.1:5000/fetch-content-details/${contentId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
        .then(response => {
          const contentDetails = response.data;
          this.content = {
            image: contentDetails.image,
            title: contentDetails.title,
            author: contentDetails.author,
            publish_year: contentDetails.publish_year,
            price: contentDetails.price,
            pdf: contentDetails.pdf,
            pdf_file_name: contentDetails.pdf_file_name,
          };
          this.existingSection = contentDetails.section;
          this.oldImage = contentDetails.image;
          this.oldPdf = contentDetails.pdf;
        })
        .catch(error => {
          console.error('Error fetching content details:', error);
        });
    },
    getUserIdFromToken() {
      const token = sessionStorage.getItem('token');
      const user = this.$jwtDecode(token);
      const userId = user.id;
      return userId;
    },
    handlePdfChange() {
      const file = this.$refs.pdfInput.files[0];
      this.content.pdf = file;
    },
    handleImageChange() {
      const file = this.$refs.imageInput.files[0];
      this.content.image = file;
    },
    submitForm() {
      const token = sessionStorage.getItem('token');
      const contentId = this.$route.params.contentId;

      const userId = this.getUserIdFromToken();

      const formData = new FormData();
      formData.append('title', this.content.title);
      formData.append('author', this.content.author);
      formData.append('number_of_pages', this.content.number_of_pages);
      formData.append('publish_year', this.content.publish_year);
      formData.append('price', this.content.price);

      if (!this.content.image && this.oldImage) {
        formData.append('image', this.oldImage);
      } else if (this.content.image) {
        formData.append('image', this.content.image);
      }

      if (!this.content.pdf && this.oldPdf) {
        // Append oldPdf only if a new PDF is not selected
        formData.append('pdf', this.oldPdf);
      } else if (this.content.pdf) {
        formData.append('pdf', this.content.pdf);
      }

      // Check if file is null and remove it from form data
      if (!this.content.pdf) {
        formData.delete('file');
      }

      axios.post(`http://127.0.0.1:5000/update-content/${contentId}/${userId}`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          Authorization: `Bearer ${token}`,
        },
      })
        .then(response => {
          console.log(response.data);
          this.$router.push('/librarian-home');
        })
        .catch(error => {
          console.error('Error:', error);
        });
    },
  },
};
</script>

<style scoped>
.container {
  color: #fff;
  background-color: #00000038;
  max-width: 900px;
  margin: 100px auto;
  padding: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 5px;
}

label {
  width: 150px;
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