<template>
    <!-- Bottom Right Toggle Button -->
    <div class="bottomnav position-fixed p-3">
        <div class="btn-group dropup">
            <button type="button" class="btn btn-secondary dropdown-toggle custom-btn" data-bs-toggle="dropdown"
                aria-expanded="false">
                Actions
            </button>
            <ul class="dropdown-menu">
                <li>
                    <router-link class="btn btn-sm btn-warning drop" to="/create-section">+ Section</router-link>
                </li>
                <li>
                    <router-link class="btn btn-sm btn-warning drop" to="/transactionlogs">Transaction Logs</router-link>
                </li>
                <li>
                    <router-link class="btn btn-sm btn-warning drop" to="/summary-graph">Summary</router-link>
                </li>
            </ul>
        </div>
    </div>
</template>

<script>
export default{

}
</script>

<style scoped>
.bottomnav{
    right: 0;
    bottom: 100px;
}

.dropdown-menu{
    right: -45px !important;
    background-color: transparent;
    bottom: 150px
}

.dropdown-menu li{
    display: grid;
    width: 80%;
    margin-top: 10px;
}
</style>