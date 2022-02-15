<template>
    <div class="container">
        <header class="jumbotron">
            <h3>
                <strong>{{currentUser.username}}</strong>
            </h3>
        </header>
        <p>
            <strong>Token:</strong>
            {{currentUser.access_token.substring(0,20)}} ... {{currentUser.access_token.substr(currentUser.access_token.length - 20)}}
        </p>
        <p>
            <strong>Refresh Token:</strong>
            {{currentUser.refresh_token.substring(0,20)}} ... {{currentUser.refresh_token.substr(currentUser.refresh_token.length - 20)}}
        </p>
    </div>
</template>
<script>
export default {
    name: 'Profile',
    computed: {
        currentUser() {
            return this.$store.state.auth.user;
        }
    },
    mounted() {
        if (!this.currentUser) {
            this.$router.push("/login");
        }
    }
};
</script>