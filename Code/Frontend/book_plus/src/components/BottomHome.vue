<template>
    <div class="position-fixed bottom-0 end-0 p-3">
        <div class="btn-group dropend">
            <router-link to="/librarian-home" class="btn btn-light custom-btn">
                <i class="fa-solid fa-house"></i>
            </router-link>
        </div>
    </div>
</template>

<script>
export default{

}
</script>

<style scoped>
.dropdown-menu{
    margin-bottom: 45px !important;
    right: -130px !important;
    background-color: transparent;
}

.dropdown-menu li{
    display: grid;
    width: 77%;
    margin-top: 10px;
}
</style>