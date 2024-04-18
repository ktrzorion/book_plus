<template>
    <div class="custom-container">
        <footer class="d-flex flex-wrap justify-content-between align-items-center py-3 my-4 border-top">
            <div class="col-md-4 d-flex align-items-center">
                <a href="/" class="mb-3 me-2 mb-md-0 logo-m text-decoration-none lh-1">
                    <img src="../assets/logo/only_logo.png" height="50px" width="60px" alt="">
                </a>
                <span class="mb-3 mb-md-0 text-body-light"><b>&copy; 2024 BookPlus Pvt.</b></span>
            </div>
            <ul class="nav col-md-4 justify-content-end list-unstyled d-flex">
                <li class="ms-3"><a class="text-muted" href="#"><i class="fa-brands fa-twitter" style="color: #ffffff;"></i></a></li>
                <li class="ms-3"><a class="text-muted" href="#"><i class="fa-brands fa-instagram" style="color: #ffffff;"></i></a></li>
                <li class="ms-3"><a class="text-muted" href="#"><i class="fa-brands fa-facebook" style="color: #ffffff;"></i></a></li>
            </ul>
        </footer>
    </div>
</template>

<script>

</script>

<style scoped>
.custom-container {
    position: fixed;
    margin: auto;
    color: white;
    width: 100%;
    height: 110px;
    background-color: rgba(0, 0, 0, 0.223);
}

.list-unstyled{
    margin-right: 40px;
}

.list-unstyled li a i{
    font-size:x-large;
}

.logo-m{
    margin-left: 40px;
}
</style>