<template>
    <div class="custom-container d-flex">
        <div class="graph">
            <h2>Reader Count Per Section</h2>
            <img ref="sectionChart" class="section-chart" alt="Section Reader Count">
        </div>
        <div class="graph">
            <h2>Reader Count Male vs Female</h2>
            <img ref="genderChart" class="gender-chart" alt="Reader Count Male vs Female">
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            sectionData: [],
            sectionNames: [],
            readerCounts: [],
        };
    },
    methods: {
        async fetchReaderCountPerSection() {

            try {
                const response = await fetch('http://127.0.0.1:5000/reader_count_per_section', {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${sessionStorage.getItem('token')}`,
                    }
                });

                if (!response.ok) {
                    throw new Error('Failed to fetch data');
                }

                const blob = await response.blob();
                const url = URL.createObjectURL(blob);
                this.$refs.sectionChart.src = url;
                console.log('Section Chart loaded');
                setTimeout(() => {
                    this.fetchReaderCountGender();
                }, 0);
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        },
        async fetchReaderCountGender() {
            try {
                const response = await fetch('http://127.0.0.1:5000/user_count_gender', {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${sessionStorage.getItem('token')}`,
                    }
                });

                if (!response.ok) {
                    throw new Error('Failed to fetch data');
                }

                const blob = await response.blob();
                const url = URL.createObjectURL(blob);
                this.$refs.genderChart.src = url;
                console.log('Gender Chart loaded');
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        },
    },
    created() {
        this.fetchReaderCountPerSection();
    },
};
</script>

<style scoped>
.custom-container {
    margin: 60px auto;
    color: white;
    column-gap: 12rem;
    align-items: center;
    justify-content: center;
}

h2 {
    font-size: 1.5rem;
    margin-bottom: 10px;
    text-align: center;
}

.section-chart,
.gender-chart {
    border-radius: 5px;
    height: 400px;
    width: 400px;
}

.graph {
    box-shadow: rgba(0, 0, 0, 0.17) 0px -23px 25px 0px inset, rgba(0, 0, 0, 0.15) 0px -36px 30px 0px inset, rgba(0, 0, 0, 0.1) 0px -79px 40px 0px inset, rgba(0, 0, 0, 0.06) 0px 2px 1px, rgba(0, 0, 0, 0.09) 0px 4px 2px, rgba(0, 0, 0, 0.09) 0px 8px 4px, rgba(0, 0, 0, 0.09) 0px 16px 8px, rgba(0, 0, 0, 0.09) 0px 32px 16px;
}
</style>
