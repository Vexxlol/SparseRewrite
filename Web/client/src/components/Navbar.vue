<template>
    <v-app-bar
            dark
            style="background: #262A3C; color: white;"
            elevate-on-scroll
            flat
    >
        <v-toolbar-title>
            <router-link to="/" style="color: white;">
                <v-avatar>
                    <img src="https://cdn.discordapp.com/avatars/665956547020587010/23faad7f847ee385f6577577d107b30e.webp">
                </v-avatar>
                Sparse
            </router-link>
        </v-toolbar-title>
        <v-spacer/>
        <v-btn text class="d-none d-sm-none d-md-flex">Leaderboard</v-btn>
        <v-menu open-on-hover v-model="opened" offset-y>
            <template v-slot:activator="{ on }">
                <v-btn
                        text
                        class="d-none d-sm-none d-md-flex"
                        v-on="on"
                        style="margin-right: 2rem;"
                >
                    Commands
                </v-btn>
            </template>
            <v-list dark>
                <v-list-item
                        v-for="category in categories"
                        :key="category"
                        :href="'/commands/' + category"
                >
                    {{ category }}
                </v-list-item>
            </v-list>
        </v-menu>
        <v-btn outlined @click="login()" v-if="!user.id" class="d-none d-sm-none d-md-flex"
               color="#7289DA"
        >Login
        </v-btn>
    </v-app-bar>
</template>
<script>
    export default {
        name: "Navbar",
        computed: {
            user() {
                return this.$store.state.user;
            }
        },
        data: () => ({
            opened: false,
            categories: [],
        }),
        methods: {
            login() {

            }
        },
        beforeCreate() {

        }
    }
</script>
<style scoped>

    a {
        text-decoration: none;
    }
</style>