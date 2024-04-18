<template>
    <div>
        <h2>About Us</h2>
        <p>Welcome to Book Plus, your one-stop solution for managing your library!</p>

        <section>
            <h3>Our Mission</h3>
            <p>
                At Book Plus, our mission is to provide an efficient and user-friendly library management system that meets
                the needs of librarians and book enthusiasts alike.
            </p>
        </section>

        <section>
            <h3>Team</h3>
            <ul>
                <li><strong>Priyanshu Katiyar</strong> - Full Stack Developer</li>
                <!-- Add more team members as needed -->
            </ul>
        </section>

        <section>
            <h3>Contact Us</h3>
            <p>If you have any questions or feedback, feel free to reach out to us:</p>
            <p>Email: contact@bookplus.com</p>
        </section>
    </div>
</template>
  
<script>
export default {
    name: 'AboutUs',
};
</script>
  
<style scoped>
div {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

/* Heading styles */
h2 {
    font-size: 2em;
    color: #333;
    margin-bottom: 20px;
}

h3 {
    font-size: 1.5em;
    color: #555;
    margin-bottom: 10px;
}

/* Paragraph styles */
p {
    line-height: 1.6;
    color: #666;
}

/* List styles */
ul {
    list-style-type: none;
    padding: 0;
    margin: 0;
}

li {
    margin-bottom: 8px;
}

/* Contact section styles */
section {
    margin-bottom: 30px;
}

/* Footer styles */
footer {
    margin-top: 50px;
    text-align: center;
    color: #888;
}
</style>  