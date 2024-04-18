<template>
    <div v-if="isVisible" class="alert" :class="[alertType]">
        <p>{{ message }}</p>
    </div>
</template>

<script>
export default {
    props: {
        message: {
            type: String,
            required: true
        },
        type: {
            type: String,
            default: 'error'
        }
    },
    data() {
        return {
            isVisible: true
        };
    },
    methods: {
        close() {
            this.isVisible = false;
        }
    },
    computed: {
        alertType() {
            return 'alert-' + this.type;
        }
    },
    mounted() {
        // setTimeout(() => {
        //     this.isVisible = false;
        // }, 5000);
    }
};
</script>

<style>
.alert {
    padding: 10px 20px;
    margin-bottom: 20px;
    border: 1px solid transparent;
    border-radius: 4px;
}

.alert-error {
    background-color: #f8d7da;
    border-color: #f5c6cb;
    color: #721c24;
}

</style>